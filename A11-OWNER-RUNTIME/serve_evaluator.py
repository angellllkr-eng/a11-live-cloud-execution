from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import BoundedSemaphore
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'alphaevolve-on-googlecloud' / 'examples' / 'circle_packing'))
from src.evaluate import CIRCLE_PACKING_EVALUATION_METRIC, circle_packing_evaluation

MAX_BODY = 512 * 1024

def get_candidate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError('request body must be a JSON object')
    if isinstance(payload.get('code'), str):
        return {'content': {'files': [{'path': 'program.py', 'content': payload['code']}]}}
    candidate = payload.get('candidate', payload)
    try:
        source = candidate['content']['files'][0]['content']
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("candidate must contain content.files[0].content or a string 'code'") from exc
    if not isinstance(source, str):
        raise ValueError('candidate source must be a string')
    return candidate

class Handler(BaseHTTPRequestHandler):
    server_version = 'A11-Local-Evaluator/1.0'
    protocol_version = 'HTTP/1.1'

    def reply(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == '/healthz':
            self.reply(200, {'status': 'PROVEN', 'service': 'a11-local-alphaevolve-evaluator', 'mode': 'LOOPBACK_ONLY', 'metric': CIRCLE_PACKING_EVALUATION_METRIC, 'cloud': 'GATED'})
        elif self.path == '/':
            self.reply(200, {'status': 'PROVEN', 'endpoints': ['GET /healthz', 'POST /evaluate'], 'warning': 'Candidate source executes locally; keep this service on loopback.'})
        else:
            self.reply(404, {'status': 'FAILED', 'error': 'not found'})

    def do_POST(self) -> None:
        if self.path != '/evaluate':
            self.reply(404, {'status': 'FAILED', 'error': 'not found'})
            return
        try:
            length = int(self.headers.get('Content-Length', '-1'))
        except ValueError:
            length = -1
        if length < 0:
            self.reply(411, {'status': 'FAILED', 'error': 'Content-Length required'})
            return
        if length > MAX_BODY:
            self.reply(413, {'status': 'FAILED', 'error': 'request body too large'})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode('utf-8'))
            candidate = get_candidate(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self.reply(400, {'status': 'FAILED', 'error': str(exc)})
            return
        if not self.server.semaphore.acquire(timeout=30):
            self.reply(429, {'status': 'GATED', 'error': 'local evaluator capacity is busy'})
            return
        try:
            result = circle_packing_evaluation(candidate)
        except Exception as exc:
            self.reply(500, {'status': 'FAILED', 'error': f'evaluator failure: {exc}'})
        else:
            self.reply(200, {'status': 'PROVEN', 'result': result})
        finally:
            self.server.semaphore.release()

    def log_message(self, format: str, *args: Any) -> None:
        return

def main() -> None:
    parser = argparse.ArgumentParser(description='A11 loopback-only local AlphaEvolve evaluator')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--concurrency', type=int, default=4)
    args = parser.parse_args()
    if args.host not in {'127.0.0.1', 'localhost', '::1'}:
        parser.error('loopback-only serving is mandatory')
    if not 1 <= args.port <= 65535 or args.concurrency < 1:
        parser.error('invalid port or concurrency')
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.semaphore = BoundedSemaphore(args.concurrency)
    print(f'PROVEN: http://{args.host}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
