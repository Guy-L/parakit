from utils import *
from datetime import datetime, timezone, timedelta
from settings import parakit_settings
from version import VERSION_DATE

try:
    import requests
except KeyboardInterrupt:
    exit()

try:
    _commits_response = requests.get('https://api.github.com/repos/Guy-L/parakit/commits?sha=master&per_page=100')
except KeyboardInterrupt:
    exit()
except Exception as e:
    print(bright("Version-checker:"), f"Failed to communicate with GitHub ({type(e).__name__}).")
    exit()

try:
    _commits_response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(bright("Version-checker:"), f"HTTP error occurred: {e}")
    exit()

_commits = _commits_response.json()
_latest_version_date = datetime.strptime(_commits[0]['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

if _latest_version_date > VERSION_DATE:
    if parakit_settings['minimize_version_checker']:

        new_commits = 0
        for commit in _commits:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if commit_date > VERSION_DATE:
                new_commits += 1

        print(separator)
        print(color(bright("A new version is available! ") + f"({new_commits} new change{'s' if new_commits > 1 else ''})", 'green'))

    else:
        new_commit_list = []
        new_commits = 0
        max_commits = 6
        max_commit_msg_len = 75

        for commit in _commits:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if commit_date > VERSION_DATE:
                new_commits += 1
                if len(new_commit_list) < max_commits:
                    commit_msg = commit['commit']['message']
                    if len(commit_msg) > max_commit_msg_len:
                        commit_msg = commit_msg[:max_commit_msg_len] + '...'

                    new_commit_list.append(bp + bright(f" [{commit_date.strftime('%Y-%m-%d %H:%M')} UTC] ") + commit_msg)

        print(separator)
        s = ('s' if new_commits > 1 else '')
        print(color(bright("A new version is available! ") + f"({new_commits} new change{s})", 'green'))
        print(underline(bright(f'New change{s}:')))
        print("\n".join(new_commit_list))

        if new_commits >= max_commits:
            print(bp, italics(f"... and {'much ' if new_commits > 12 else ''}more!"))

        if new_commits >= 3:
            print()
            print(bright("ParaKit is always improving. We recommend you update now."))
            print(f"- If you installed with Git, simply enter \033[30;47mgit pull\033[0m.")
            print(f"- If you installed by downloading the project files without")
            print(f"  Git (i.e. Code -> Download ZIP), you should do so again.")
            print(f"- Either way, because of the project's current setup,")
            print(f"  you may need to resolve conflicts in {italics('analysis.py')} or")
            print(f"  {italics('settings.py')}. {darker('There are plans to address this soon.')}")