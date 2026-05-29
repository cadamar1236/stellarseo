#!/usr/bin/env python3
"""Validate YAML syntax of tech-debt-audit.yml"""
import yaml, sys, os

# Try common paths
candidates = [
    '.github/workflows/tech-debt-audit.yml',
    '/app/data/workspaces/StellarSEO/.github/workflows/tech-debt-audit.yml',
]
fpath = None
for c in candidates:
    if os.path.exists(c):
        fpath = c
        break

if not fpath:
    # walk
    for root, dirs, files in os.walk('/app'):
        for f in files:
            if f == 'tech-debt-audit.yml':
                fpath = os.path.join(root, f)
                break
        if fpath:
            break

print(f"File path: {fpath}")
print(f"Exists: {os.path.exists(fpath) if fpath else 'N/A'}")

if not fpath:
    print("❌ Could not locate tech-debt-audit.yml")
    sys.exit(1)

with open(fpath, 'r') as f:
    raw = f.read()

data = yaml.safe_load(raw)
print("✅ YAML syntax check: PASSED")
print(f"   File size: {len(raw)} bytes")
print(f"   Lines: {raw.count(chr(10))}")
print(f"   Top-level keys: {list(data.keys())}")
print(f"   Jobs: {list(data.get('jobs', {}).keys())}")
steps = data.get('jobs', {}).get('tech-debt-audit', {}).get('steps', [])
for i, s in enumerate(steps, 1):
    print(f"   Step {i}: {s.get('name', 'unnamed')}")
sys.exit(0)