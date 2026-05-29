import yaml

try:
    with open('.github/workflows/tech-debt-audit.yml', 'r') as f:
        data = yaml.safe_load(f)
    print("✅ YAML syntax check: PASSED")
    print(f"   Top-level keys: {list(data.keys())}")
    print(f"   Jobs defined: {list(data.get('jobs', {}).keys())}")
    print(f"   File size: {len(open('.github/workflows/tech-debt-audit.yml').read())} bytes")
except yaml.YAMLError as e:
    print(f"❌ YAML syntax check: FAILED")
    print(f"   Error: {e}")
except FileNotFoundError:
    print(f"❌ File not found at .github/workflows/tech-debt-audit.yml")