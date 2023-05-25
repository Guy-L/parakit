def input_exit():
    print()
    input("Press Enter to close the program.")
    exit()

#Extreme sanity check
try:
    import venv
    import sys
    import os
    import platform
    import subprocess
except ImportError as e:
    print(f"Setup error: Error while importing standard libraries: {e}\nIf you see this message, please contact the developer!")
    input_exit()

_venv_path   = 'venv'
_reqs_path   = 'requirements.txt'
_script_path = 'state_reader.py'
    
#Create venv if not already created
if not os.path.isfile(os.path.join(_venv_path, 'pyvenv.cfg')):
    if os.path.exists(_venv_path):
        print(f"Setup error: The venv folder at '{_venv_path}' appears to be corrupted (missing config file).")
        print("Fix the issue or delete the folder and run this script again.")
        input_exit()
        
    venv.create(_venv_path, with_pip=True)
    print(f"Setup: venv created at '{_venv_path}'")

pip_exe = os.path.join(_venv_path, 'bin', 'pip') if platform.system() != 'Windows' else os.path.join(_venv_path, 'Scripts', 'pip')
python_exe = os.path.join(_venv_path, 'bin', 'python') if platform.system() != 'Windows' else os.path.join(_venv_path, 'Scripts', 'python')

#Install missing required packages in the venv
def get_installed_packages(venv_path):
    result = subprocess.run([pip_exe, "freeze"], capture_output=True, text=True)
    return {line.split('==')[0] for line in result.stdout.splitlines()}

def get_required_packages(requirements_path):
    with open(requirements_path) as reqs:
        return {line.split('==')[0] for line in reqs if line and not line.startswith('#')}
        
if get_required_packages(_reqs_path) - get_installed_packages(_venv_path):
    print(f"Setup: Missing packages detected; running pip install.")
    try:
        subprocess.check_call([pip_exe, "install", "-r", _reqs_path])
        print(f"Setup: All required modules installed to '{_venv_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Setup error: Error occurred while installing requirements.txt modules: {e}")
        input_exit()
else:
    print(f"Setup: Requirements all good.")
    
#Run state-reader
subprocess.run([python_exe, _script_path])
input_exit()