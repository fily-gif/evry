import subprocess
import time
import os
import sweater.config as config
import sys

def last_githash() -> str | None:
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
        return git_hash[:7]
    except Exception as e:
        print(f"oops github is on fire: {e}")
        return None

def get_uptime():
    uptime = round(time.time() - config.start)
    print(uptime)  # debug

    result = ""

    if int(uptime) <= 60:
        result = f'{int(uptime)} seconds'

    elif int(uptime) >= 60 and int(uptime) < 3600:
        result = f'{int(round(uptime/60, 2))} minutes'

    elif int(uptime) >= 3600:
        result = f'{int(round(uptime/3600, 2))} hours'

    else:
        result = f'{int(uptime)} days'

    return result

def restart_bot():
    print('Restart requested!')
    os.execv(sys.executable, ['python3'] + sys.argv)