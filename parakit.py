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
    import base64
    from datetime import datetime, timezone, timedelta
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
    print("\nIf this is your first time using ParaKit, welcome!")
    print("Please give us a moment to finish setting up.\nIt should take about a minute.\n")
    print("If it seems to do no progress at all for a while, try pressing Enter. Python's weird.")

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
    print("Setup: Missing packages detected; running pip install.")
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
import requests 
from settings import parakit_settings
VERSION_DATE = datetime(2023, 8, 13, 18, 44, 0, tzinfo=timezone.utc)
#note for devs: this should always be set to a couple minutes in the future when pushing
#there is a pre-commit hook that will do this for you, ask Guy if you don't have it!

try:
    _commits_response = requests.get('https://api.github.com/repos/Guy-L/parakit/commits?sha=master')
except Exception as e:
    print(f"\nVersion-checker: Failed to communicate with GitHub ({type(e).__name__})")
    input_exit()

try:
    _commits_response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"\nVersion-checker: HTTP error occurred: {e}")
    input_exit()
    
_commits = _commits_response.json()
_latest_version_date = datetime.strptime(_commits[0]['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

if _latest_version_date > VERSION_DATE:
    if parakit_settings['minimize_version_checker']:
    
        new_commits = 0
        for commit in _commits:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if commit_date > VERSION_DATE:
                new_commits += 1
    
        print('\n================================')
        print(f'A new version is available! ({new_commits} new commits)')
        
    else: 
        print('\n================================')
        print('A new version is available!')
        print('New changes:')
        
        new_commits = 0
        max_commits = 6
        max_commit_msg_len = 75
        
        for commit in _commits:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if commit_date > VERSION_DATE:
                new_commits += 1
                if new_commits < max_commits:
                    commit_msg = commit['commit']['message']
                    if len(commit_msg) > max_commit_msg_len:
                        commit_msg = commit_msg[:max_commit_msg_len] + '...'
                        
                    print(f"• [{commit_date.strftime('%Y-%m-%d %H:%M')} UTC] {commit_msg}")
        
        if new_commits >= max_commits:
            print(f"• ... and more! ({new_commits} commits)")
        
        print()
        print('If you installed via Code > Download ZIP, please do so again')
        print(f'or download a Release if one from {_latest_version_date.strftime("%Y-%m-%d %H:%M")} UTC is available.')
        print('If you installed via Git, please do \'git pull\'. You may need to resolve a merge')
        print('conflict if changes were made to settings.py or analysis.py which conflict with yours.')
        print('If this happens and you\'re not sure how to proceed, feel free to contact the developer.')
    
#Prevent instant exit
input_exit()
