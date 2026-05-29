f = open('backend/main.py')
lines = f.readlines()
f.close()
print(f"Total lines: {len(lines)}")
print("=== LAST 30 LINES ===")
for i, line in enumerate(lines[-30:], start=len(lines)-29):
    print(f"{i}: {line}", end='')