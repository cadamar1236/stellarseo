import json, os, re

report = {
    "tool": "backend-audit",
    "target": "backend/",
    "findings": [],
    "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0}
}

def add_finding(severity, category, title, detail, recommendation):
    report["findings"].append({
        "severity": severity,
        "category": category,
        "title": title,
        "detail": detail,
        "recommendation": recommendation
    })
    report["summary"][severity] += 1

req_path = "backend/requirements.txt"
with open(req_path) as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

for line in lines:
    if ">=" in line and "<" not in line and "==" not in line:
        add_finding("medium", "dependency-pinning",
            f"Open-ended dependency: {line}",
            f"'{line}' has only a lower bound.",
            "Pin to a specific major version.")

main_path = "backend/main.py"
with open(main_path) as f:
    content = f.read()
lines = content.split("\n")

if '__name__ == "__main__"' not in content:
    add_finding("high", "code-structure",
        "Missing __main__ guard",
        "No `if __name__ == '__main__':` block.",
        "Add section for direct execution.")

dict_calls = [l.strip() for l in lines if ".dict()" in l]
if dict_calls:
    add_finding("high", "pydantic-v1",
        f"Found {len(dict_calls)} .dict() calls",
        f"Lines: {dict_calls[:3]}. Pydantic v2 uses .model_dump().",
        "Replace .dict() with .model_dump().")

if '@app.on_event("startup")' in content:
    add_finding("high", "fastapi-deprecation",
        "Deprecated @app.on_event('startup') used",
        "FastAPI deprecated lifespan event handlers.",
        "Replace with @asynccontextmanager lifespan pattern.")

bare_except = len(re.findall(r'except\s*:', content))
if bare_except > 0:
    add_finding("high", "error-handling",
        f"{bare_except} bare 'except:' block(s) found",
        "Bare except catches all exceptions.",
        "Replace with specific exception types.")

func_defs = re.findall(r'^\s*def\s+(\w+)\s*\(', content, re.MULTILINE)
typed_funcs = re.findall(r'^\s*def\s+\w+\s*\([^)]*\)\s*->', content, re.MULTILINE)
untyped = len(func_defs) - len(typed_funcs)
if untyped > 0:
    add_finding("medium", "type-hints",
        f"{untyped} function(s) missing return type hints",
        f"Total: {len(func_defs)} funcs, {len(typed_funcs)} typed.",
        "Add return type hints.")

route_funcs = re.findall(r'@app\.(?:get|post|put|delete|patch)\([^)]+\)\s*\n\s*def\s+\w+', content)
add_finding("low", "code-duplication",
    f"Found {len(route_funcs)} route handlers",
    "Similar CRUD patterns repeated.",
    "Consider using a ViewSet pattern.")

print(json.dumps(report, indent=2))
print(f"\nTotal findings: {len(report['findings'])}", flush=True)