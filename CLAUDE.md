# 🔌 bambu-go2rtc — Camera Stream Bridge

> forge ❯ bambu ❯ **bg2r** · application
>
> **Archetype:** Stream bridge (pre-built binary + Python wrapper)
> **Language:** Go (pre-built) + Python 3
> **Interfaces:** MJPEG · RTSP · TLS socket (port 6000)
> **Shared rules:** `~/ai/forge/bambu/.claude/rules/bambu-ecosystem.md`

## Build / Validate

No build system, tests, or linting. Pre-built go2rtc binaries.

## Architecture

- go2rtc: pre-built Go binary (AlexxIT/go2rtc), YAML config
- `camera-stream.py`: TLS client → stdout pipe → go2rtc stdin exec
- Platform binaries: `go2rtc-mac` (ARM64), `go2rtc_linux_arm64`
- Config: `go2rtc.yaml`
- Outputs: `http://localhost:1984/api/stream.mjpeg?src=bambu_camera`, `rtsp://localhost:8554/bunamu_camera`

## Git Policy

Agent-managed. Full git lifecycle authorized: stage, commit, push.
