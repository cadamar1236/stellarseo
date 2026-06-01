with open('REPO_CONTEXT.md') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
print(f"Last 20 lines (lines {len(lines)-19}-{len(lines)}):")
for i, line in enumerate(lines[-20:], len(lines)-19):
    print(f"{i:4d}: {line}", end='')