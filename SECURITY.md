# Security And Safety

Report updater integrity problems privately to the Station 562 owner before
publishing details.

The updater must never:

- invoke whole-chip erase;
- write the NVS owner-data range;
- issue factory reset or Burn Handle;
- write eFuses;
- accept an unknown ESP32 target;
- bypass release hash verification.

CTF play is intentionally read-only. This repository does not accept or
publish flags, operator solutions, private authority material, or decrypted
challenge stages.
