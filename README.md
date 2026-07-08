# 🌩️ Cloudflare Workers AI Token Farmer

**Automatic token harvester for Cloudflare Workers AI Free Tier**

Farm unlimited Cloudflare Workers AI tokens from multiple Google accounts, then inject them into 9Router dashboard for unified API access.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📊 What You Get

- **10,000 neurons/day per account** (Cloudflare Free Tier)
- **Unlimited accounts** — farm as many as you need
- **No credit card required**
- **Automated OAuth login** via DrissionPage
- **Auto-inject to 9Router** dashboard for unified access
- **All models included:** Llama 3.3 70B, DeepSeek R1, Qwen 2.5, GLM 5.2, Kimi K2.6, etc.

---

## 🚀 Quick Start

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip google-chrome-stable xvfb

# Install Python dependencies
pip3 install DrissionPage
```

### Step 1: Prepare Accounts

Create `akun.txt` with your Gmail accounts (one per line):

```
user1@gmail.com|YourPassword123
user2@gmail.com|AnotherPass456
user3@gmail.com|SecurePass789
```

**Format:** `email|password` (pipe separator, no spaces)

**Note:** Accounts must have Google OAuth enabled for Cloudflare login.

### Step 2: Farm Tokens

```bash
# Run with xvfb for headless display
xvfb-run python3 cf_farmer.py

# Or run single account for testing
xvfb-run python3 cf_farmer.py --only user1@gmail.com

# Custom delay between accounts (default: 10s)
xvfb-run python3 cf_farmer.py --delay 15
```

**Output:** `cf_keys.txt` with harvested tokens:

```
cloudflare_user1|https://api.cloudflare.com/client/v4/accounts/abc123.../ai/v1|cfut_xxx...|[models]
cloudflare_user2|https://api.cloudflare.com/client/v4/accounts/def456.../ai/v1|cfut_yyy...|[models]
```

---

## 🎯 Step-by-Step: Complete Workflow

### Part 1: Create Cloudflare Accounts (Manual Setup)

1. **Go to Cloudflare Dashboard**
   - Open: https://dash.cloudflare.com/sign-up
   - Click **"Sign up with Google"**

2. **Login with Gmail**
   - Use your Gmail account
   - Allow Cloudflare access permissions

3. **Verify Account**
   - No credit card needed
   - Free tier activates immediately
   - Workers AI quota: **10,000 neurons/day**

4. **Repeat for Multiple Accounts**
   - Use different Gmail accounts
   - Each account = separate 10k neurons/day quota
   - 10 accounts = 100k neurons/day total capacity

---

### Part 2: Harvest Tokens (Automated)

This script automates token creation for all accounts.

**What the script does:**

1. Opens Cloudflare login page
2. Clicks "Sign in with Google"
3. Enters email + password (human-like typing)
4. Handles Google OAuth consent screens
5. Extracts Cloudflare Account ID
6. Creates API token with **Workers AI permissions** via browser fetch API
7. Saves token to `cf_keys.txt`

**Token Permissions:**
- Workers AI Read: `a92d2450e05d4e7bb7d0a64968f83d11`
- Workers AI Write: `bacc64e0f6c34fc0883a1223f938a104`

**Run the harvester:**

```bash
# Full auto mode (all accounts in akun.txt)
xvfb-run python3 cf_farmer.py

# Test single account first
xvfb-run python3 cf_farmer.py --only test@gmail.com --delay 5
```

**Expected output:**

```
==================================================
 [1] user1@gmail.com
==================================================
 [1] CF login...
 [2] Google OAuth...
 [3] Email...
 [4] Password...
 [5] Waiting for dashboard...
    Account: 632b39bf31b41ddbe4194e782c746c87
 [6] Create token (Workers AI)...
 [OK] Token: cfut_wDXfnyWd7zRVHNcp7WAwhGeDvb...

==================================================
 DONE: 1/1 succeeded
==================================================
```

**Troubleshooting:**

| Issue | Fix |
|-------|-----|
| `[ERR] Password field not found` | Google flagged login as suspicious — use App Password or less restrictive security |
| `[ERR] Not on CF: accounts.google.com` | Stuck on consent screen — increase delay or check 2FA settings |
| `[ERR] Account ID not found` | Dashboard API failed — retry or check account status |
| `selenium.common.exceptions` | Wrong package — use `DrissionPage`, not Selenium |
| `DISPLAY not set` | Must run with `xvfb-run` for headless mode |

---

### Part 3: Inject to 9Router Dashboard (Auto via API)

**9Router** is a unified API proxy for multiple AI providers. Inject all CF tokens for centralized access.

#### Option A: Auto Inject via REST API (Recommended)

**Script:** `inject_to_9router.py`

```python
#!/usr/bin/env python3
import json, subprocess, re

# Dashboard URL
DASHBOARD = "http://your-9router-host:20128"

# Read tokens from cf_keys.txt
tokens = []
with open('cf_keys.txt', 'r') as f:
    for line in f:
        if not line.strip():
            continue
        parts = line.strip().split('|')
        if len(parts) >= 3:
            name = parts[0]
            url = parts[1]
            api_key = parts[2]
            match = re.search(r'/accounts/([a-f0-9]+)/', url)
            if match:
                tokens.append({
                    'name': name,
                    'apiKey': api_key,
                    'accountId': match.group(1)
                })

print(f"Loaded {len(tokens)} tokens")

# Inject via /api/providers
for i, token in enumerate(tokens, 1):
    payload = {
        "provider": "cloudflare-ai",
        "name": token['name'],
        "authType": "apikey",
        "apiKey": token['apiKey'],
        "providerSpecificData": {"accountId": token['accountId']},
        "priority": i,
        "isActive": True
    }
    
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f"{DASHBOARD}/api/providers",
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ], capture_output=True, text=True)
    
    resp = json.loads(result.stdout)
    if 'connection' in resp and 'id' in resp['connection']:
        print(f"✅ [{i}/{len(tokens)}] {token['name']} added")
    else:
        print(f"❌ [{i}/{len(tokens)}] {token['name']} failed: {result.stdout[:100]}")

print(f"\n✨ Done! Check dashboard: {DASHBOARD}/dashboard/providers")
```

**Run:**

```bash
# Edit DASHBOARD URL in script first
python3 inject_to_9router.py
```

**Expected output:**

```
Loaded 10 tokens
✅ [1/10] cloudflare_user1 added
✅ [2/10] cloudflare_user2 added
...
✅ [10/10] cloudflare_user10 added

✨ Done! Check dashboard: http://your-host:20128/dashboard/providers
```
