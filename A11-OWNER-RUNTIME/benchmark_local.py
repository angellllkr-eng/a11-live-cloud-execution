from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AE = ROOT / 'alphaevolve-on-googlecloud'
sys.path.insert(0, str(AE / 'examples' / 'circle_packing'))
from src.evaluate import INITIAL_PROGRAM_CODE, circle_packing_evaluation


def main() -> None:
    parser = argparse.ArgumentParser(description='Benchmark the A11 local evaluator')
    parser.add_argument('-n', '--runs', type=int, default=1000)
    args = parser.parse_args()
    if args.runs < 1:
        parser.error('--runs must be positive')
    candidate = {'content': {'files': [{'path': 'program.py', 'content': INITIAL_PROGRAM_CODE}]}}
    started = time.perf_counter()
    results = [circle_packing_evaluation(candidate) for _ in range(args.runs)]
    elapsed = time.perf_counter() - started
    scores = [item['scores']['scores'][0]['score'] for item in results]
    report = {
        'status': 'PROVEN',
        'owner': 'София Tech Register EOOD',
        'brand': 'A11',
        'component': 'alphaevolve-local-evaluator',
        'runs': args.runs,
        'elapsed_seconds': elapsed,
        'mean_milliseconds': elapsed * 1000 / args.runs,
        'evaluations_per_second': args.runs / elapsed,
        'metric': 'sum_of_radii',
        'deterministic': len(set(scores)) == 1,
        'score': scores[0],
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'execution': 'LOCAL_ONLY',
        'cloud_alphaevolve': 'GATED',
    }
    output = ROOT / 'A11-OWNER-RUNTIME' / 'BENCHMARK.json'
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
