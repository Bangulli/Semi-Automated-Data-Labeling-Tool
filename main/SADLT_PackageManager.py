import sys
import subprocess

Packages = ['opencv', 'pillow', 'numpy', 'tk', 'tensorflow', 'pandas']

# implement conda as a subprocess:
for element in Packages:
    subprocess.check_call([sys.executable, '-m', 'conda', 'install', element])