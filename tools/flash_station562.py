#!/usr/bin/env python3
"""Safe binary updater for official Station 562 badge releases."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "firmware" / "v6.3.0" / "manifest.json"


class UpdateError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def image_path(part: dict[str, Any]) -> Path:
    return REPO_ROOT / part["path"]


def verify_part(name: str, part: dict[str, Any]) -> None:
    path = image_path(part)
    if not path.is_file():
        raise UpdateError(f"missing release file: {path}")
    actual_size = path.stat().st_size
    if actual_size != part["size"]:
        raise UpdateError(
            f"size mismatch for {name}: expected {part['size']}, got {actual_size}"
        )
    actual_hash = sha256_file(path)
    if actual_hash != part["sha256"]:
        raise UpdateError(
            f"SHA-256 mismatch for {name}: expected {part['sha256']}, got {actual_hash}"
        )


def verify_release(manifest: dict[str, Any]) -> None:
    for target_name, target in manifest["targets"].items():
        verify_part(f"{target_name} update", target["update"])


def run_esptool(arguments: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-m", "esptool", *arguments]
    try:
        return subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=capture,
        )
    except FileNotFoundError as error:
        raise UpdateError("Python could not start esptool") from error


def ensure_esptool() -> None:
    result = run_esptool(["version"], capture=True)
    if result.returncode != 0:
        raise UpdateError(
            "esptool is unavailable; activate the virtual environment and run "
            "'python -m pip install -r requirements.txt'"
        )


def list_ports() -> int:
    try:
        from serial.tools import list_ports as serial_list_ports
    except ImportError as error:
        raise UpdateError(
            "pyserial is unavailable; run 'python -m pip install -r requirements.txt'"
        ) from error

    ports = sorted(serial_list_ports.comports(), key=lambda item: item.device)
    if not ports:
        print("No serial ports found.")
        return 1
    print("Available serial ports:")
    for port in ports:
        detail = " | ".join(value for value in (port.description, port.hwid) if value)
        print(f"  {port.device}" + (f"  {detail}" if detail else ""))
    return 0


def detect_target(port: str, manifest: dict[str, Any]) -> str:
    # Underscore operation names work on esptool 4.x and remain aliases in 5.x.
    result = run_esptool(["--port", port, "chip_id"], capture=True)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        raise UpdateError(f"could not connect to {port}:\n{output.strip()}")

    matches = [
        target_name
        for target_name, target in manifest["targets"].items()
        if target["chip"] in output
    ]
    if len(matches) != 1:
        raise UpdateError(
            "connected chip is not an approved Station 562 target; refusing to flash"
        )
    return matches[0]


def update_parts(manifest: dict[str, Any], target_name: str) -> list[dict[str, Any]]:
    return [manifest["targets"][target_name]["update"]]


def show_plan(port: str, manifest: dict[str, Any], target_name: str) -> None:
    target = manifest["targets"][target_name]
    print()
    print("STATION 562 UPDATE PLAN")
    print(f"  Release: {manifest['version']}")
    print(f"  Port:    {port}")
    print(f"  Target:  {target['name']}")
    print("  Mode:    normal owner update")
    print("  Writes:  official firmware + CTF update bundle")
    nvs = manifest["preserved_nvs"]
    print(f"  Preserves NVS: {nvs['offset']} + {nvs['size']}")
    print("  Factory reset: never")
    print()


def flash(port: str, manifest: dict[str, Any], target_name: str) -> None:
    parts = update_parts(manifest, target_name)
    arguments = [
        "--port",
        port,
        "write_flash",
        "--flash-mode",
        manifest["flash_mode"],
        "--flash-freq",
        manifest["flash_frequency"],
        "--flash-size",
        manifest["flash_size"],
    ]
    for part in parts:
        arguments.extend([part["offset"], str(image_path(part))])

    result = run_esptool(arguments)
    if result.returncode != 0:
        raise UpdateError("flash failed; reconnect the badge and retry")

    part = parts[0]
    print("Verifying installed update bundle...")
    result = run_esptool(
        ["--port", port, "verify_flash", part["offset"], str(image_path(part))]
    )
    if result.returncode != 0:
        raise UpdateError("post-write verification failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install official Station 562 firmware and CTF binaries safely."
    )
    parser.add_argument("--port", help="badge serial port, such as COM5 or /dev/cu.usbmodem1101")
    parser.add_argument("--list", action="store_true", help="list serial ports and exit")
    parser.add_argument("--dry-run", action="store_true", help="detect and print without writing")
    parser.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.list:
            return list_ports()
        if not args.port:
            raise UpdateError("provide --port or use --list")

        manifest = load_manifest()
        print(f"Verifying bundled {manifest['version']} release files...")
        verify_release(manifest)
        ensure_esptool()
        target_name = detect_target(args.port, manifest)
        show_plan(args.port, manifest, target_name)

        if args.dry_run:
            print("Dry run complete. Nothing was written.")
            return 0

        if not args.yes:
            confirmation = input("Type FLASH to continue: ").strip()
            if confirmation != "FLASH":
                print("Cancelled. Nothing was written.")
                return 1

        flash(args.port, manifest, target_name)
        print()
        print(f"SUCCESS: Station 562 {manifest['version']} and its CTF are installed.")
        print("Owner NVS was not erased. Reconnect at 115200 baud and run: version")
        return 0
    except UpdateError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
