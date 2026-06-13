import os
import subprocess

dates = [
    "2026-06-11T10:15:00+03:00",
    "2026-06-11T14:30:00+03:00",
    "2026-06-11T18:45:00+03:00",
    "2026-06-11T21:10:00+03:00",
    "2026-06-12T09:30:00+03:00",
    "2026-06-12T11:15:00+03:00",
    "2026-06-12T13:20:00+03:00",
    "2026-06-12T14:40:00+03:00",
    "2026-06-12T15:00:00+03:00",
    "2026-06-12T15:15:00+03:00"
]

def run(cmd, env=None):
    subprocess.run(cmd, shell=True, check=True, env=env)

# Start interactive rebase and pause at every commit
env = os.environ.copy()
env["GIT_SEQUENCE_EDITOR"] = "sed -i '' 's/^pick/edit/g'"
subprocess.run("git rebase -i d69922f", shell=True, env=env)

# We are now at the first commit. Iterate and amend dates.
for date in dates:
    print(f"Amending commit with date {date}")
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = date
    env["GIT_AUTHOR_DATE"] = date
    run(f'git commit --amend --no-edit --date="{date}"', env=env)

    # Continue rebase. If it fails, we are at the end.
    res = subprocess.run("git rebase --continue", shell=True, env=env)
    if res.returncode != 0:
        break
