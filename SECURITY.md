# Security And Safety

The updater must never:

- invoke whole-chip erase;
- write the NVS owner-data range;
- issue factory reset or Burn Handle;
- write eFuses;
- accept an unknown ESP32 target;
- bypass release hash verification.

CTF play is intentionally read-only. Follow the safety contract in the
[Hardware CTF Player Guide](docs/ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md).
