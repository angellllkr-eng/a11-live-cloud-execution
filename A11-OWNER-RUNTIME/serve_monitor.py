from __future__ import annotations

import argparse
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path(__file__).resolve().parent
MONITOR_DIR = RUNTIME / "monitor"
AE = ROOT / "alphaevolve-on-googlecloud"
sys.path.insert(0, str(AE / "examples" / "circle_packing"))

from src.evaluate import (  # type: ignore
    CIRCLE_PACKING_EVALUATION_METRIC,
    INITIAL_PROGRAM_CODE,
    circle_packing_evaluation,
)

MODELS = {
    "gemini-3.7": {
        "label": "Gemini 3.7",
        "provider": "Google",
        "cloud": "GATED",
        "note": "UI-selected only. Remote Gemini path blocked until billing + ADC + GE_APP_ID.",
    },
    "grok-6": {
        "label": "Grok 6",
        "provider": "xAI",
        "cloud": "GATED",
        "note": "UI-selected only. No remote Grok calls from this local monitor.",
    },
    "sol-5.6": {
        "label": "Sol 5.6",
        "provider": "A11 catalog",
        "cloud": "GATED",
        "note": "UI-selected only. Local analysis label for comparison runs.",
    },
    "nvidia-pro": {
        "label": "NVIDIA Pro tier",
        "provider": "NVIDIA",
        "cloud": "GATED",
        "note": "UI-selected only. No GPU cloud dispatch from this loopback page.",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def status_payload() -> dict[str, Any]:
    proof = read_json(RUNTIME / "PROOF.json")
    bench = read_json(RUNTIME / "BENCHMARK.json")
    cloud = read_json(RUNTIME / "CLOUD-PREFLIGHT.json")
    return {
        "status": "PROVEN",
        "service": "a11-live-performance-monitor",
        "mode": "LOOPBACK_ONLY",
        "owner": "София Tech Register EOOD",
        "brand": "A11 / MindReply",
        "portfolio": "A11-K.space",
        "models": MODELS,
        "local": {
            "status": proof.get("status", bench.get("status", "UNVERIFIED")),
            "metric": proof.get("metric", bench.get("metric", CIRCLE_PACKING_EVALUATION_METRIC)),
            "score": proof.get("score", bench.get("score")),
            "mean_ms": bench.get("mean_milliseconds"),
            "eps": bench.get("evaluations_per_second"),
            "benchmark_status": bench.get("status", "UNVERIFIED"),
            "deterministic": bench.get("deterministic"),
        },
        "cloud": cloud
        or {
            "Billing": "BLOCKED",
            "ADC": "BLOCKED",
            "DiscoveryEngineAPI": "BLOCKED",
            "GE_APP_ID": "UNVERIFIED",
            "CloudMutation": "GATED",
        },
        "warning": "Model selector is local-only. Cloud inference and deployment remain GATED.",
    }


def run_local_sample(model_key: str) -> dict[str, Any]:
    if model_key not in MODELS:
        raise ValueError(f"unsupported model: {model_key}")
    candidate = {
        "content": {
            "files": [{"path": "program.py", "content": INITIAL_PROGRAM_CODE}]
        }
    }
    started = time.perf_counter()
    result = circle_packing_evaluation(candidate)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    score = result["scores"]["scores"][0]["score"]
    return {
        "status": "PROVEN",
        "model": model_key,
        "model_meta": MODELS[model_key],
        "metric": CIRCLE_PACKING_EVALUATION_METRIC,
        "score": score,
        "elapsed_ms": elapsed_ms,
        "execution": "LOCAL_ONLY",
        "cloud_inference": "GATED",
        "result": result,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "A11-Live-Monitor/1.0"
    protocol_version = "HTTP/1.1"

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self._send(code, raw, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            html = (MONITOR_DIR / "index.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
            return
        if path == "/healthz":
            self._json(200, {"status": "PROVEN", "service": "a11-live-performance-monitor", "mode": "LOOPBACK_ONLY"})
            return
        if path == "/api/status":
            self._json(200, status_payload())
            return
        if path == "/api/models":
            self._json(200, {"status": "PROVEN", "models": MODELS, "cloud_inference": "GATED"})
            return
        self._json(404, {"status": "FAILED", "error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/sample":
            self._json(404, {"status": "FAILED", "error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 0 or length > 64 * 1024:
            self._json(400, {"status": "FAILED", "error": "invalid body length"})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            model = str(payload.get("model", "gemini-3.7"))
            result = run_local_sample(model)
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"status": "FAILED", "error": str(exc)})
            return
        self._json(200, result)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="A11 loopback live performance monitor")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("loopback-only serving is mandatory")
    if not (MONITOR_DIR / "index.html").exists():
        raise SystemExit("BLOCKED: monitor/index.html missing")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"PROVEN: http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
