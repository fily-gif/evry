import subprocess
import time
import os
import sweater.config as config
import sys
from PIL import Image

def last_githash() -> str | None:
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
        return git_hash[:7]
    except Exception as e:
        print(f"oops github is on fire: {e}")
        return

def get_uptime():
    uptime = round(time.time() - config.start)

    result = ""

    if int(uptime) <= 60:
        result = f'{int(uptime)} seconds'

    elif int(uptime) >= 60 and int(uptime) < 3600:
        result = f'{int(round(uptime/60, 2))} minutes'

    elif int(uptime) >= 3600:
        result = f'{int(round(uptime/3600, 2))} hours'

    else:
        result = f'{int(round(uptime/86400))} days'

    return result

def restart_bot():
    print('Restart requested!')
    os.execv(sys.executable, ['python3'] + sys.argv)

def hex_to_img(hex: str):
    if "#" in hex: 
        hex = str(hex).lstrip('#')
    r, g, b = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    # Create a new image of 480x480 pixels filled with the desired color
    new_img = Image.new("RGB", (480, 480), (r, g, b))
    return new_img