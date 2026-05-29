import shutil
# Check where python3 actually exists
print(shutil.which('python3'))
# Check if we can write to a temp location
import tempfile
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='/tmp')
tf.write("import sys; print('hello from tmp'); sys.exit(0)")
tf.close()
print(f"Wrote to: {tf.name}")
import subprocess
r = subprocess.run(['python3', tf.name], capture_output=True, text=True)
print("stdout:", r.stdout)
print("stderr:", r.stderr)