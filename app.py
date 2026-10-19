#!/usr/bin/env python3
"""Start Sweet Odyssey with one command: python app.py.

Only the standard library is imported before a private .venv is prepared.
Existing global Python packages, PATH and system configuration are untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import venv
import webbrowser

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"


def say(message: str) -> None:
    print(message, flush=True)


def load_environment() -> None:
    env_file = ROOT / ".env"
    if not env_file.is_file():
        return
    for raw in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if not key or not key.replace("_", "a").isalnum():
            continue
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key, value)


def prepare_python() -> Path:
    python = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        say("İlk açılış: oyun için özel Python ortamı hazırlanıyor…")
        venv.EnvBuilder(with_pip=True).create(VENV)
    use_postgres = os.environ.get("DATABASE_URL", "").startswith(("postgresql", "postgres://"))
    selected = ROOT / "backend" / ("requirements-postgres.txt" if use_postgres else "requirements.txt")
    contents = (ROOT / "backend" / "requirements.txt").read_bytes() + selected.read_bytes()
    fingerprint = hashlib.sha256(contents).hexdigest()
    marker = VENV / ".sweet-requirements.sha256"
    ready = marker.is_file() and marker.read_text(encoding="ascii").strip() == fingerprint
    if ready:
        probe = subprocess.run([str(python), "-c", "import fastapi, uvicorn, sqlalchemy, pydantic, alembic"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        ready = probe.returncode == 0
    if not ready:
        say("Gerekli paketler kuruluyor. İlk kurulumda internet bağlantısı gerekir.")
        result = subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(selected)], cwd=ROOT, check=False)
        if result.returncode:
            raise RuntimeError("Paketler kurulamadı. İnternet / kurum proxy ayarlarını kontrol edip tekrar çalıştır. Ayrıntılar yukarıda.")
        marker.write_text(fingerprint, encoding="ascii")
    return python


def port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if os.name == "nt" and hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        elif os.name != "nt":
            # Match Uvicorn: a recently closed game can leave TIME_WAIT sockets.
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def choose_port(requested: int | None) -> int:
    default = int(os.environ.get("SWEET_PORT", "8000"))
    candidates = [requested] if requested is not None else list(range(default, min(default + 11, 65536)))
    for port in candidates:
        if not 1024 <= port <= 65535:
            raise RuntimeError("Bağlantı noktası 1024–65535 arasında olmalı.")
        if port_available(port):
            return port
    raise RuntimeError("Bağlantı noktası kullanımda. Örnek: python app.py --port 8011")


def wait_until_ready(process: subprocess.Popen, url: str) -> bool:
    # Bypass system HTTP proxies for the local game health check.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + 30
    while process.poll() is None and time.monotonic() < deadline:
        try:
            with opener.open(url + "/api/health", timeout=1) as response:
                health = json.load(response)
                if health.get("status") == "ok" and health.get("app") == "sweet-odyssey":
                    return True
        except (urllib.error.URLError, OSError, ValueError):
            pass
        time.sleep(0.2)
    return False


def stop_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def main() -> int:
    # Turkish status messages also remain readable when output is redirected.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Sweet Odyssey oyununu başlatır.")
    parser.add_argument("--port", type=int, help="Yerel bağlantı noktası (varsayılan: 8000).")
    parser.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma.")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        say("Python 3.11 veya üzeri gerekiyor. Python 3.11 / 3.12 / 3.13 kullanabilirsin.")
        return 1
    os.chdir(ROOT)
    load_environment()
    if not (ROOT / "frontend" / "dist" / "index.html").is_file():
        say("Oyun dosyaları eksik. ZIP'in tamamını bir klasöre çıkarıp app.py dosyasını oradan çalıştır.")
        return 1
    process = None
    try:
        port = choose_port(args.port)
        python = prepare_python()
        url = f"http://127.0.0.1:{port}"
        say("\nSWEET ODYSSEY — Tatlı bir maceraya hazır mısın?")
        say("Oyun başlatılıyor…")
        process = subprocess.Popen([
            str(python), "-m", "uvicorn", "backend.app.main:app",
            "--host", "127.0.0.1", "--port", str(port),
            "--no-access-log", "--log-level", "warning",
        ], cwd=ROOT)
        if not wait_until_ready(process, url):
            stop_process(process)
            raise RuntimeError("Oyun başlatılamadı. Yukarıdaki hata mesajını kontrol et.")
        say(f"\nOyun hazır: {url}")
        say("Oynarken bu pencereyi açık bırak. Kapatmak için Ctrl+C.")
        if not args.no_browser:
            try:
                if not webbrowser.open(url):
                    say("Tarayıcı otomatik açılamadı; yukarıdaki adresi tarayıcıda açabilirsin.")
            except webbrowser.Error:
                say("Tarayıcı otomatik açılamadı; yukarıdaki adresi tarayıcıda açabilirsin.")
        return process.wait()
    except KeyboardInterrupt:
        say("\nOyun kapatılıyor. Kaydedilen ilerlemen korunuyor.")
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        say(f"\nBaşlatma sorunu: {exc}")
        return 1
    finally:
        if process is not None:
            stop_process(process)


if __name__ == "__main__":
    raise SystemExit(main())
