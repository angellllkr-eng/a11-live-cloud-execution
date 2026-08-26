from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AE = ROOT / 'alphaevolve-on-googlecloud'
sys.path.insert(0, str(AE / 'examples' / 'circle_packing'))

from src.evaluate import (  # type: ignore
    CIRCLE_PACKING_EVALUATION_METRIC,
    INITIAL_PROGRAM_CODE,
    circle_packing_evaluation,
)

OUT = ROOT / 'A11-OWNER-RUNTIME' / 'PROOF.json'


def main() -> None:
    candidate = {
        'content': {
            'files': [{'path': 'program.py', 'content': INITIAL_PROGRAM_CODE}]
        }
    }
    result = circle_packing_evaluation(candidate)
    score = result['scores']['scores'][0]['score']
    proof = {
        'status': 'PROVEN',
        'owner': 'София Tech Register EOOD',
        'brand': 'A11',
        'portfolio': 'A11-K.space',
        'project_id': 'mind-reply-496111',
        'account': 'mind-reply@mind-reply-496111.iam.gserviceaccount.com',
        'component': 'alphaevolve-circle-packing-seed-evaluator',
        'metric': CIRCLE_PACKING_EVALUATION_METRIC,
        'score': score,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'billing_enabled': False,
        'discovery_engine': 'GATED',
        'gemini_enterprise_app_id': 'UNVERIFIED',
        'cluster_toolkit': 'GATED',
        'zapier_mcp': 'FAILED',
        'commercial_paths': {
            'A11 Signal': 'https://buy.stripe.com/eVq14h6wEb042XK5Oy63K06',
            'A11 Operator': 'https://buy.stripe.com/00w8wJg7e6JO55Sfp863K05',
            'A11 Council': 'https://buy.stripe.com/6oUeV7bQYgkocyk3Gq63K04',
            'Repository Reality Engine': 'https://book.stripe.com/8x2dR36wEb04aqc90K63K03',
            'PATCH Revenue Engine': 'https://book.stripe.com/00wdR3aMUfgkbugel463K02',
            'GitHub + Python Profit Audit': 'https://book.stripe.com/8x2aER4owd8c1TG4Ku63K00',
        },
    }
    OUT.write_text(json.dumps(proof, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(proof, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
