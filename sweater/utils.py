import subprocess
import time
import os
import sweater.config as config
import sys
import ast

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

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
