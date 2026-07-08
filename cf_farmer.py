#!/usr/bin/env python3
"""
Cloudflare Workers AI Token Farmer
===================================
Automatically creates CF API tokens with Workers AI permissions
using Google OAuth login (Gmail accounts).

Requirements:
- Python 3.8+
- pip install DrissionPage
- Xvfb (for headless display): apt install xvfb
- Google Chrome: apt install google-chrome-stable

Usage:
- Prepare akun.txt: email|password (one per line)
- Run: xvfb-run python3 cf_farmer.py
"""
from DrissionPage import ChromiumPage, ChromiumOptions
import time, json, random, shutil, argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AKUN_FILE = SCRIPT_DIR / "akun.txt"
RESULT_FILE = SCRIPT_DIR / "cf_keys.txt"
MODELS = '["@cf/zai-org/glm-5.2","@cf/deepseek-ai/deepseek-r1-distill-qwen-32b","@cf/meta/llama-3.3-70b-instruct-fp8-fast","@cf/qwen/qwen2.5-coder-32b-instruct","@cf/qwen/qwq-32b"]'

WORKERS_AI_READ = "a92d2450e05d4e7bb7d0a64968f83d11"
WORKERS_AI_WRITE = "bacc64e0f6c34fc0883a1223f938a104"


def hd(lo=1.0, hi=3.0):
    time.sleep(random.uniform(lo, hi))


def mk_browser(index):
    profile = SCRIPT_DIR / f".profile_{index}"
    profile.mkdir(exist_ok=True)
    co = ChromiumOptions()
    co.set_browser_path("/usr/bin/google-chrome")
    co.set_argument("--no-sandbox")
    co.set_argument("--disable-setuid-sandbox")
    co.set_argument("--disable-gpu")
    co.set_argument("--disable-dev-shm-usage")
    co.set_argument("--window-size=1366,768")
    co.set_argument(f"--user-data-dir={profile}")
    co.set_local_port(9200 + index)
    return ChromiumPage(co), profile


def js_click(page, sel):
    return page.run_js(f"""var el=document.querySelector('{sel}');if(el){{el.dispatchEvent(new MouseEvent('click',{{bubbles:true,cancelable:true,view:window}}));return true;}}return false;""")


def harvest(email, password, index):
    print(f"\n{'='*50}")
    print(f" [{index+1}] {email}")
    print(f"{'='*50}")
    page, profile = mk_browser(index)
    try:
        # [1] CF login
        print(" [1] CF login...")
        page.get("https://dash.cloudflare.com/login")
        page.wait.ele_displayed("tag:button", timeout=20)
        time.sleep(3)

        # [2] Google OAuth
        print(" [2] Google OAuth...")
        page.run_js("""var btns=document.querySelectorAll('button');for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==='Google'){btns[i].dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));break;}}""")
        for _ in range(15):
            time.sleep(1)
            if "accounts.google.com" in (page.url or ""):
                break

        # [3] Email
        print(" [3] Email...")
        page.wait.ele_displayed("#identifierId", timeout=15)
        time.sleep(1)
        page.run_js("document.getElementById('identifierId').focus();")
        time.sleep(0.3)
        for ch in email:
            page.actions.type(ch)
            time.sleep(random.uniform(0.02, 0.08))
        time.sleep(0.5)
        js_click(page, "#identifierNext")
        time.sleep(5)

        # [4] Password
        print(" [4] Password...")
        if not page.run_js("return !!document.querySelector('input[type=password]')"):
            print(" [ERR] Password field not found")
            return False
        page.run_js("document.querySelector('input[type=password]').focus();")
        time.sleep(0.3)
        for ch in password:
            page.actions.type(ch)
            time.sleep(random.uniform(0.02, 0.08))
        time.sleep(0.5)
        js_click(page, "#passwordNext")
        time.sleep(5)

        # [5] Handle Google consent screens
        print(" [5] Waiting for dashboard...")
        for _ in range(60):
            time.sleep(3)
            url = page.url or ""
            if "dash.cloudflare.com" in url and "/login" not in url:
                break
            if "accounts.google.com" in url:
                page.run_js("""var btns=document.querySelectorAll('button');for(var i=0;i<btns.length;i++){var txt=btns[i].textContent.trim();if(txt==='Next'||txt==='Continue'||txt==='Allow'||txt.indexOf('understand')>=0||txt.indexOf('Accept')>=0||txt.indexOf('agree')>=0){btns[i].click();break;}}""")

        if "dash.cloudflare.com" not in (page.url or ""):
            print(f" [ERR] Not on CF: {(page.url or '')[:80]}")
            return False

        # Get account ID
        acc_id = page.run_js("""return fetch('/api/v4/accounts').then(r=>r.json()).then(d=>{ if (d.success && d.result && d.result.length > 0) return d.result[0].id; return ''; });""")
        acc_id = acc_id if isinstance(acc_id, str) else ""
        print(f"    Account: {acc_id}")
        if not acc_id:
            print(" [ERR] Account ID not found")
            return False

        # [6] Create token
        print(" [6] Create token (Workers AI)...")
        token_data = {
            "name": f"cf_ai_{acc_id[:8]}",
            "policies": [
                {
                    "effect": "allow",
                    "permission_groups": [
                        {"id": WORKERS_AI_READ},
                        {"id": WORKERS_AI_WRITE}
                    ],
                    "resources": {f"com.cloudflare.api.account.{acc_id}": "*"}
                }
            ]
        }
        js_code = "var _payload = " + json.dumps(token_data) + ";\n"
        js_code += """return fetch('/api/v4/user/tokens', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(_payload)
        }).then(r => r.json()).then(d => JSON.stringify(d));"""

        result_raw = page.run_js(js_code)
        result = json.loads(result_raw)

        if result.get("success"):
            token = result["result"]["value"]
            api_url = f"https://api.cloudflare.com/client/v4/accounts/{acc_id}/ai/v1"
            tag = email.split("@")[0]
            line = f"cloudflare_{tag}|{api_url}|{token}|{MODELS}"
            with open(RESULT_FILE, "a") as f:
                f.write(line + "\n")
            print(f" [OK] Token: {token[:30]}...")
            return True
        else:
            print(f" [ERR] {result.get('errors', result)}")
            return False
    except Exception as e:
        print(f" [ERR] {e}")
        return False
    finally:
        try: page.quit()
        except: pass
        shutil.rmtree(profile, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Single email")
    parser.add_argument("--delay", type=int, default=10)
    args = parser.parse_args()
    accounts = []
    for line in AKUN_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        acc = {"email": parts[0], "password": parts[1]}
        if args.only and acc["email"] != args.only:
            continue
        accounts.append(acc)
    if not accounts:
        print("No accounts!")
        return
    print(f"Total: {len(accounts)} accounts")
    ok = 0
    for i, acc in enumerate(accounts):
        if harvest(acc["email"], acc["password"], i):
            ok += 1
        if i < len(accounts) - 1:
            hd(args.delay, args.delay + 3)
    print(f"\n{'='*50}")
    print(f" DONE: {ok}/{len(accounts)} succeeded")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
