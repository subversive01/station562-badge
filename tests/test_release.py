import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "flash_station562.py"
SPEC = importlib.util.spec_from_file_location("station562_flasher", SCRIPT)
assert SPEC and SPEC.loader
FLASHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FLASHER)


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "firmware" / "v6.3.0" / "manifest.json").open(
            "r", encoding="utf-8"
        ) as handle:
            cls.manifest = json.load(handle)

    def test_all_release_hashes(self):
        FLASHER.verify_release(self.manifest)

    def test_default_update_preserves_nvs(self):
        nvs_start = int(self.manifest["preserved_nvs"]["offset"], 16)
        nvs_end = nvs_start + int(self.manifest["preserved_nvs"]["size"], 16)
        for target_name in self.manifest["targets"]:
            for part in FLASHER.update_parts(self.manifest, target_name):
                start = int(part["offset"], 16)
                end = start + part["size"]
                self.assertTrue(end <= nvs_start or start >= nvs_end)

    def test_public_package_has_only_opaque_update_payloads(self):
        binary_names = sorted(path.name for path in (ROOT / "firmware").rglob("*.bin"))
        self.assertEqual(
            binary_names,
            [
                "station562-v6.3.0-codecell-update.bin",
                "station562-v6.3.0-xiao-update.bin",
            ],
        )

    def test_no_firmware_source_or_private_keys(self):
        forbidden_suffixes = {".ino", ".elf", ".map", ".pem", ".key"}
        offending = [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file()
            and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
            and path.suffix.lower() in forbidden_suffixes
        ]
        self.assertEqual(offending, [])

    def test_detects_codecell_and_xiao(self):
        for chip_text, expected in (
            ("Chip type: ESP32-C3", "codecell"),
            ("Chip type: ESP32-C6", "xiao"),
        ):
            result = mock.Mock(returncode=0, stdout=chip_text, stderr="")
            with mock.patch.object(FLASHER, "run_esptool", return_value=result):
                self.assertEqual(
                    FLASHER.detect_target("TEST_PORT", self.manifest), expected
                )

    def test_rejects_unknown_target(self):
        result = mock.Mock(returncode=0, stdout="Chip type: ESP32-S3", stderr="")
        with mock.patch.object(FLASHER, "run_esptool", return_value=result):
            with self.assertRaises(FLASHER.UpdateError):
                FLASHER.detect_target("TEST_PORT", self.manifest)

    def test_target_detection_uses_version_appropriate_cli(self):
        result = mock.Mock(returncode=0, stdout="Chip type: ESP32-C3", stderr="")
        for major, operation in ((4, "chip_id"), (5, "chip-id")):
            with self.subTest(esptool_major=major):
                with mock.patch.object(
                    FLASHER, "run_esptool", return_value=result
                ) as run_esptool:
                    FLASHER.detect_target("TEST_PORT", self.manifest, major)
                self.assertIn(operation, run_esptool.call_args.args[0])

    def test_detects_supported_esptool_versions(self):
        for output, expected in (
            ("esptool.py v4.12.0", 4),
            ("esptool v5.2.0", 5),
        ):
            with self.subTest(output=output):
                result = mock.Mock(returncode=0, stdout=output, stderr="")
                with mock.patch.object(FLASHER, "run_esptool", return_value=result):
                    self.assertEqual(FLASHER.ensure_esptool(), expected)

    def test_rejects_unknown_esptool_version(self):
        result = mock.Mock(returncode=0, stdout="esptool v6.0.0", stderr="")
        with mock.patch.object(FLASHER, "run_esptool", return_value=result):
            with self.assertRaises(FLASHER.UpdateError):
                FLASHER.ensure_esptool()

    def test_flash_uses_version_appropriate_cli(self):
        cases = (
            (
                4,
                ("write_flash", "--flash_mode", "--flash_freq", "--flash_size"),
                "verify_flash",
            ),
            (
                5,
                ("write-flash", "--flash-mode", "--flash-freq", "--flash-size"),
                "verify-flash",
            ),
        )
        for major, write_tokens, verify_operation in cases:
            with self.subTest(esptool_major=major):
                result = mock.Mock(returncode=0, stdout="", stderr="")
                with mock.patch.object(
                    FLASHER, "run_esptool", return_value=result
                ) as run_esptool:
                    FLASHER.flash("TEST_PORT", self.manifest, "codecell", major)

                write_args = run_esptool.call_args_list[0].args[0]
                verify_args = run_esptool.call_args_list[1].args[0]
                for token in write_tokens:
                    self.assertIn(token, write_args)
                self.assertIn(verify_operation, verify_args)


if __name__ == "__main__":
    unittest.main()
