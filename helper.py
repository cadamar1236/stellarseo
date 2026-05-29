import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('backend/main.py') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
print("=== LAST 30 LINES ===")
for i, line in enumerate(lines[-30:], start=len(lines)-29):
    print(f"{i}: {line}", end='')
print("\n=== LINE COUNT ===", len(lines))