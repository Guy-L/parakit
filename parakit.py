def input_exit():
    print()
    try:
        input("\33[5mPress \33[1mEnter\033[22m to close the program.\033[25m")
    except KeyboardInterrupt:
        print()
    print("\033[F\033[K\033[F", end='')
    exit()

#Extreme sanity check
try:
    import venv
    import sys
    import os
    import platform
    import subprocess
    import traceback
    import shutil
    from utils import *
except Exception as e:
    print(f"\33[31mSetup error:\33[0m Error while importing standard libraries: {e}")
    print("If you see this message, please contact the developer!")
    input_exit()

def valid_venv(bin_folder, pr=False):
    missing = []

    if not os.path.exists(os.path.join(_venv_path, 'pyvenv.cfg')):
        missing.append('pyvenv.cfg')
    if not os.path.exists(os.path.join(_venv_path, bin_folder, 'pip.exe')):
        missing.append('pip')
    if not os.path.exists(os.path.join(_venv_path, bin_folder, 'python.exe')):
        missing.append('python')

    if pr and missing:
        print(darker(color(f"Invalid venv for bin folder '{bin_folder}': ", 'red') + f"Missing: {', '.join(missing)}"))
    return not bool(missing)

try:
    _venv_path = 'venv'
    _reqs_path = 'requirements.txt'
    _worker_script_path = 'state_reader.py'
    _vcheck_script_path = 'version_check.py'

    #Create venv if not already created
    if not os.path.exists(_venv_path):
        print(color(bright("\nIf this is your first time using ParaKit, welcome!"), 'green'))
        print(color("Please give us a moment to finish setting things up.", 'green'))
        print(color(darker("It should take about a minute.\n"), 'green'))

        print(bright("First Time Setup:"), f"Creating virtual environment at '{bright(_venv_path)}'...")
        venv.create(_venv_path, with_pip=True)
        print(bright("First Time Setup:"), f"Virtual environment created at '{bright(_venv_path)}'.")

        print(bright("First Time Setup:"), f"Installing dependencies...")
        print(bright("Tip:"), "If it seems to do no progress at all for a while, try pressing Enter.", italics(darker("Python's weird.\n")))
    else:
        print(italics(darker("Checking dependencies...")), end='\r')

    if valid_venv('Scripts', True):
        _pip_exe = os.path.join(_venv_path, 'Scripts', 'pip')
        _python_exe = os.path.join(_venv_path, 'Scripts', 'python')

    elif valid_venv('bin', True):
        _pip_exe = os.path.join(_venv_path, 'bin', 'pip')
        _python_exe = os.path.join(_venv_path, 'bin', 'python')

    else:
        print(color("Setup error:", 'red'), "The virtual environment is unusable.")
        print("To try to fix this, the "+bright(_venv_path)+" folder will be deleted and will be re-made next time.")
        print("If it still doesn't work, please try "+bright(underline("updating to the latest Python version"))+".")
        input_exit()

    #Install missing required packages in the venv
    def get_installed_packages(venv_path):
        result = subprocess.run([_pip_exe, "freeze"], capture_output=True, text=True)
        return {line.split('==')[0] for line in result.stdout.splitlines()}

    def get_required_packages(requirements_path):
        with open(requirements_path) as reqs:
            return {line.strip() for line in reqs if line and not line.startswith('#')}

    if get_required_packages(_reqs_path) - get_installed_packages(_venv_path):
        print(bright("Setup:"), "Missing packages detected; running pip install.")
        try:
            subprocess.check_call([_pip_exe, "install", "-r", _reqs_path])
            print(bright("Setup:"), color("All required modules installed to '"+bright(_venv_path)+"'", 'green'))
        except Exception as e:
            print(color("Setup error:", 'red'), f"Error occurred while installing requirements.txt modules: {bright(e)}")
            print("If you see this message, please contact the developer!")
            input_exit()

    #Run state-reader
    subprocess.run([_python_exe, _worker_script_path])

except KeyboardInterrupt:
    print("Setup interrupted by user.")
    input_exit()

except Exception as e:
    print(color("Uncaught setup error:", 'red'), e, darker())
    traceback.print_exc()
    print(default() + "If you see this message, please contact the developer!")
    input_exit()

finally:
    if not valid_venv('Scripts') and not valid_venv('bin') and os.path.exists(_venv_path):
        shutil.rmtree(_venv_path)

#Inform users if running non-latest version
try:
    subprocess.run([_python_exe, _vcheck_script_path])
except KeyboardInterrupt:
    pass

#Prevent instant exit
input_exit()