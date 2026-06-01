import subprocess, os
os.chdir('/app/data/workspaces/StellarSEO')
result = subprocess.run(['git', 'log', '--oneline', '-4'], capture_output=True, text=True, timeout=10)
print(result.stdout)