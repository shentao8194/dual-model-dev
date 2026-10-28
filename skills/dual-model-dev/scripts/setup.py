"""Interactive international onboarding. Never run with a key in arguments."""
import csv
import getpass
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
import warnings
import webbrowser

STATE = Path(os.environ.get('DUAL_MODEL_HOME', str(Path.home()/'.dual-model-dev'))).expanduser().resolve()

def main():
    if not sys.stdin.isatty():
        raise ValueError('Run setup in your own interactive terminal, not a chat tool or pipe.')
    warnings.simplefilter('error', getpass.GetPassWarning)
    print('BytePlus international setup for Dual Model Dev')
    print('Register/sign in, enable ModelArk access, and create a dedicated API key yourself.')
    print('Console: https://console.byteplus.com/')
    print('Key instructions: https://docs.byteplus.com/en/docs/ModelArk/api-key')
    if input('Open official registration and key instructions in your browser? [y/N] ').lower() == 'y':
        webbrowser.open('https://console.byteplus.com/')
        webbrowser.open('https://docs.byteplus.com/en/docs/ModelArk/api-key')
    print('1: General-purpose ModelArk API (writing and coding)')
    print('2: Coding Plan (coding only; writing is disabled)')
    choice = input('Select the entitlement you already have [1]: ').strip() or '1'
    if choice not in ('1','2'): raise ValueError('Select 1 or 2.')
    base_url = 'https://ark.ap-southeast.bytepluses.com/api/' + ('v3' if choice == '1' else 'coding/v3')
    print('Confirm the following endpoint matches your console:', base_url)
    print('Copy actual model or inference endpoint IDs from your account; availability is not guaranteed.')
    kimi = input('Kimi model / endpoint ID: ').strip()
    deepseek = input('DeepSeek model / endpoint ID: ').strip()
    if not kimi or not deepseek or any(c.isspace() for c in kimi+deepseek):
        raise ValueError('Both account-supported model IDs are required.')
    if (STATE/'config.json').exists() and input('Replace existing local configuration? Type YES: ') != 'YES':
        print('Cancelled.'); return
    print('The key stays local until you authorize an API task. No paid request is made by setup.')
    key = getpass.getpass('Dedicated API key (hidden): ').strip()
    if not key or any(c.isspace() for c in key): raise ValueError('Invalid empty or whitespace-containing key.')
    STATE.mkdir(parents=True, exist_ok=True)
    folder = STATE/('credentials-'+uuid.uuid4().hex)
    folder.mkdir(mode=0o700)
    if os.name == 'nt':
        identity = subprocess.run(['whoami.exe','/user','/fo','csv','/nh'],capture_output=True,text=True,check=True)
        sid = next(csv.reader(io.StringIO(identity.stdout.strip())))[1]
        if not sid.startswith('S-1-'): raise ValueError('Could not identify current Windows user.')
        subprocess.run(['icacls.exe',str(folder),'/grant:r',f'*{sid}:(OI)(CI)F','/inheritance:r'],capture_output=True,check=True)
    else:
        os.chmod(STATE,0o700)
    key_path = folder/'api.key'
    fd = os.open(key_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(key)
    key = None
    cfg = {'base_url':base_url,'api_key_env':'DUAL_MODEL_API_KEY','api_key_file':str(key_path),
           'planner':kimi,'executor':deepseek,'max_calls':48,'max_output_tokens':4096,
           'max_total_tokens':500000,'timeout_seconds':1800,'max_repairs':1}
    temp = STATE/('config-'+uuid.uuid4().hex+'.tmp')
    temp.write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    if os.name != 'nt': os.chmod(temp,0o600)
    temp.replace(STATE/'config.json')
    print('Saved local settings:',STATE/'config.json')
    print('Credentials are permission-restricted, not encrypted. No key was printed.')
    print('Return to your agent and invoke $dual-model-dev. Model access still requires a live task to verify.')

if __name__ == '__main__':
    try: main()
    except (KeyboardInterrupt,EOFError):
        print('\nCancelled.'); raise SystemExit(1)
    except Exception:
        print('Setup failed. Check interactive terminal support, input and directory permissions. No key was printed.')
        raise SystemExit(1)
