import sys
import subprocess

Packages = ['numpy', 'tk', 'tensorflow', 'pandas']

# implement conda as a subprocess:
for element in Packages:
    subprocess.check_call([sys.executable, '-m', 'conda', 'install', element])