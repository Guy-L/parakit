import requests 
from datetime import datetime, timezone, timedelta
from settings import parakit_settings
from version import VERSION_DATE

try:
    _commits_response = requests.get('https://api.github.com/repos/Guy-L/parakit/commits?sha=master&per_page=100')
except Exception as e:
    print(f"\nVersion-checker: Failed to communicate with GitHub ({type(e).__name__}).")
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
        print(f"A new version is available! ({new_commits} new commit{'s' if new_commits > 1 else ''})")
        
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
        print(f'or download a Release if one from after {_latest_version_date.strftime("%Y-%m-%d %H:%M")} UTC is available.')
        print('If you installed via Git, please do \'git pull\'. You may need to resolve a merge')
        print('conflict if changes were made to settings.py or analysis.py which conflict with yours.')
        print('If this happens and you\'re not sure how to proceed, feel free to contact the developer.')