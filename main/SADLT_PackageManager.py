import sys
import subprocess

Packages = ['numpy', 'tk']

# implement conda as a subprocess:
for element in Packages:
    subprocess.check_call([sys.executable, '-m', 'conda', 'install', element])