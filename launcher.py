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
    import requests
    import base64
    from datetime import datetime
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

_pip_exe = os.path.join(_venv_path, 'bin', 'pip') if platform.system() != 'Windows' else os.path.join(_venv_path, 'Scripts', 'pip')
_python_exe = os.path.join(_venv_path, 'bin', 'python') if platform.system() != 'Windows' else os.path.join(_venv_path, 'Scripts', 'python')

#Install missing required packages in the venv
def get_installed_packages(venv_path):
    result = subprocess.run([_pip_exe, "freeze"], capture_output=True, text=True)
    return {line.split('==')[0] for line in result.stdout.splitlines()}

def get_required_packages(requirements_path):
    with open(requirements_path) as reqs:
        return {line.split('==')[0] for line in reqs if line and not line.startswith('#')}
        
if get_required_packages(_reqs_path) - get_installed_packages(_venv_path):
    print(f"Setup: Missing packages detected; running pip install.")
    try:
        subprocess.check_call([_pip_exe, "install", "-r", _reqs_path])
        print(f"Setup: All required modules installed to '{_venv_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Setup error: Error occurred while installing requirements.txt modules: {e}")
        input_exit()
else:
    print(f"Setup: Requirements all good.")
    
#Run state-reader
subprocess.run([_python_exe, _script_path])

#Inform users if running non-latest version
VERSION_DATE = datetime(2023, 5, 31, 0, 0) #note for the dev: always set to slightly in the future before commit or else...

_commits_response = requests.get('https://api.github.com/repos/Guy-L/thgym/commits?sha=state-reader') #todo update to new repo

try:
    _commits_response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Version-checker: HTTP error occurred: {err}")
    input_exit()
    
_commits = _commits_response.json()
_latest_version_date = datetime.strptime(_commits[0]['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ')

if _latest_version_date > VERSION_DATE:
    print()
    print('A new version is available!')
    print('New changes:')
    
    counter = 0
    max_commits = 6
    max_commit_msg_len = 75
    
    for commit in _commits:
        commit_date = datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ')
        if commit_date > VERSION_DATE:
            counter += 1
            if counter < max_commits:
                commit_msg = commit['commit']['message']
                if len(commit_msg) > max_commit_msg_len:
                    commit_msg = commit_msg[:max_commit_msg_len] + '...'
                    
                print(f"• [{commit_date.strftime('%Y-%m-%d %H:%M')}] {commit_msg}")
    
    if counter >= max_commits:
        print(f"• ... and more! ({counter} commits)")
    
    print()
    print('If you installed via Code > Download ZIP, please do so again')
    print(f'or download a Release if one from {_latest_version_date.strftime("%Y-%m-%d %H:%M")} is available.')
    print('If you installed via Git, please do \'git pull\'. You may need to resolve a merge')
    print('conflict if changes were made to settings.py or analysis.py which conflict with yours.')
    print('If this happens and you\'re not sure how to proceed, feel free to contact the developer.')
    
#Prevent instant exit
input_exit()