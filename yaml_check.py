#!/usr/bin/env python3
"""YAML syntax check for GitHub Actions workflow file."""
import yaml, sys

fpath = '.github/workflows/tech-debt-audit.yml'

try:
    with open(fpath, 'r') as f:
        raw = f.read()
    data = yaml.safe_load(raw)

    print("✅ YAML syntax check: PASSED")
    print(f"   File size: {len(raw)} bytes")
    print(f"   Lines: {raw.count(chr(10))}")
    print(f"   Top-level keys: {list(data.keys())}")
    print(f"   Jobs defined: {list(data.get('jobs', {}).keys())}")
    steps = data.get('jobs', {}).get('tech-debt-audit', {}).get('steps', [])
    step_names = [s.get('name', 'unnamed') for s in steps]
    print(f"   Steps ({len(steps)}): {step_names}")

    on_trigger = data.get('on', {})
    push_branches = []
    pr_branches = []
    if isinstance(on_trigger, dict):
        push_obj = on_trigger.get('push', {})
        pr_obj = on_trigger.get('pull_request', {})
        if isinstance(push_obj, dict):
            push_branches = push_obj.get('branches', [])
        if isinstance(pr_obj, dict):
            pr_branches = pr_obj.get('branches', [])
    wf_dispatch = 'workflow_dispatch' in (on_trigger if isinstance(on_trigger, dict) else {})
    print(f"   Triggers: push={push_branches}, pull_request={pr_branches}, workflow_dispatch={wf_dispatch}")

    sys.exit(0)

except yaml.YAMLError as e:
    print(f"❌ YAML syntax check: FAILED")
    prob = getattr(e, 'problem', '')
    mark = getattr(e, 'problem_mark', None)
    loc = f"line {mark.line}, col {mark.column}" if mark else "unknown location"
    print(f"   Error: {prob} ({loc})")
    sys.exit(1)
except FileNotFoundError:
    print(f"❌ File not found: {fpath}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    sys.exit(1)