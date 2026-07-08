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

**Without proxy (< 20 accounts):**
```
user1@gmail.com|YourPassword123
user2@gmail.com|AnotherPass456
user3@gmail.com|SecurePass789
```

**With proxy (recommended for 20+ accounts):**
```
user1@gmail.com|YourPassword123|socks5://proxy_user:proxy_pass@us.1024proxy.io:1080
user2@gmail.com|AnotherPass456|socks5://proxy_user:proxy_pass@eu.1024proxy.io:1080
user3@gmail.com|SecurePass789|socks5://proxy_user:proxy_pass@sg.1024proxy.io:1080
```

**Format:** `email|password|proxy` (pipe separator)

### Step 2: Farm Tokens

```bash
# Clone repo dulu
git clone https://github.com/Bayu5677/cf-workers-ai-farmer.git
cd cf-workers-ai-farmer

# Buat akun.txt (isi email|password|proxy)
nano akun.txt

# Run with xvfb for headless display
xvfb-run -a python3 cf_farmer.py

# Or run single account for testing
xvfb-run -a python3 cf_farmer.py --only user1@gmail.com

# Custom delay between accounts (default: 10s)
xvfb-run -a python3 cf_farmer.py --delay 15

# Run WITHOUT proxy (ignore proxy in akun.txt)
xvfb-run -a python3 cf_farmer.py --no-proxy
```

**Output:** `cf_keys.txt` with harvested tokens:

```
cloudflare_user1|https://api.cloudflare.com/client/v4/accounts/abc123.../ai/v1|cfut_xxx...|[models]
cloudflare_user2|https://api.cloudflare.com/client/v4/accounts/def456.../ai/v1|cfut_yyy...|[models]
```

---

## 🔒 Proxy Setup Guide

### When to Use Proxy

| Accounts | Recommendation | Why |
|----------|---------------|-----|
| **1-20 accounts** | ❌ No proxy needed | Datacenter IP works fine |
| **20-50 accounts** | ⚠️ Residential proxy | Avoid rate limiting |
| **50-100 accounts** | ✅ Residential proxy | Prevent IP blocks |
| **100+ accounts** | ✅ Proxy + IP rotation | Required for bulk farming |

### Supported Proxy Formats

```
socks5://user:pass@host:port    ← Recommended (SOCKS5)
http://user:pass@host:port      ← HTTP proxy
socks5://host:port              ← No auth required
host:port:user:pass             ← Legacy format (auto-converts)
```

### Recommended Proxy Providers

| Provider | Type | Price | Rotation | Best For |
|----------|------|-------|----------|----------|
| **1024proxy.io** | Residential | $0.50/GB | Per-request | Best value |
| **Bright Data** | Residential | $5.00/GB | Per-request | Enterprise |
| **Oxylabs** | Residential | $4.00/GB | Per-request | High volume |
| **IPRoyal** | Residential | $1.50/GB | Per-request | Budget |

### Configure akun.txt with Proxy

Each account can use **different proxy** for maximum stealth:

```
# US accounts with US proxy
user1@gmail.com|pass123|socks5://user:pass@us.1024proxy.io:1080
user2@gmail.com|pass456|socks5://user:pass@us.1024proxy.io:1081

# EU accounts with EU proxy
user3@gmail.com|pass789|socks5://user:pass@eu.1024proxy.io:1080
user4@gmail.com|pass101|socks5://user:pass@de.1024proxy.io:1080

# SG accounts with SG proxy
user5@gmail.com|pass202|socks5://user:pass@sg.1024proxy.io:1080
```

### Proxy Session Rotation

For **per-request IP rotation**, use session IDs in proxy URL:

```
# Format: socks5://user-region-session:pass@host:port
user1@gmail.com|pass123|socks5://user-us-session1:pass@proxy.1024proxy.io:1080
user2@gmail.com|pass456|socks5://user-us-session2:pass@proxy.1024proxy.io:1080
```

Each `sessionX` gets a **different IP** from the provider's pool.

### Test Proxy Connection

```bash
# Test single account with proxy
xvfb-run python3 cf_farmer.py --only user1@gmail.com

# Expected output:
# [1] user1@gmail.com
# [1] CF login...
#    Proxy: socks5://user:pass@us.1024proxy.io:1080...
# [2] Google OAuth...
# [OK] Token: cfut_wDXfn...
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
| `Proxy connection failed` | Check proxy credentials or switch proxy provider |

---

### Part 3: Inject to 9Router Dashboard (Auto via API)

**9Router** is a unified API proxy for multiple AI providers. Inject all CF tokens for centralized access.

#### Option A: Auto Inject via REST API (Recommended)

```bash
# Edit DASHBOARD URL in inject_to_9router.py first
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

---

## 📈 Scaling Guide

### Small Scale (1-20 accounts)

**No proxy needed.** Datacenter IP works fine.

```bash
# akun.txt (no proxy)
user1@gmail.com|pass123
user2@gmail.com|pass456
...

# Run
xvfb-run python3 cf_farmer.py
```

**Capacity:** 10k-200k neurons/day

---

### Medium Scale (20-100 accounts)

**Residential proxy recommended.**

```bash
# akun.txt (with proxy)
user1@gmail.com|pass123|socks5://user:pass@proxy1.example.com:1080
user2@gmail.com|pass456|socks5://user:pass@proxy2.example.com:1080
...

# Run
xvfb-run python3 cf_farmer.py --delay 15
```

**Capacity:** 200k-1M neurons/day

---

### Large Scale (100+ accounts)

**Residential proxy mandatory** + IP rotation per account.

```bash
# akun.txt (unique session per account)
user1@gmail.com|pass123|socks5://user-session1:pass@proxy.example.com:1080
user2@gmail.com|pass456|socks5://user-session2:pass@proxy.example.com:1080
...

# Run with longer delay
xvfb-run python3 cf_farmer.py --delay 20
```

**Capacity:** 1M+ neurons/day

---

## 🛡️ Security Notes

- **Never commit `akun.txt`** to Git (already in `.gitignore`)
- **Tokens are sensitive** — treat like passwords
- **Rotate tokens** if compromised (delete + re-run harvester)
- **Use App Passwords** if 2FA enabled on Gmail
- **Proxy credentials** should be kept secure

---

## 📋 Files Structure

```
cf-workers-ai-farmer/
├── README.md              # This file
├── cf_farmer.py           # Main token harvester (with proxy support)
├── inject_to_9router.py   # Auto-inject to 9Router dashboard
├── akun.txt               # Your accounts (create this)
├── akun_example.txt       # Example with proxy configs
├── cf_keys.txt            # Harvested tokens (auto-generated)
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── .gitignore             # Ignore sensitive files
```

---

## ❓ FAQ

**Q: Can I use datacenter proxy?**
A: Yes, but residential is safer for 20+ accounts. Datacenter may work for < 20 accounts.

**Q: Do I need different proxy per account?**
A: Recommended but not required. Different proxy per account = more stealth.

**Q: What if proxy is slow?**
A: Increase `--delay` flag. Proxy adds latency to each request.

**Q: Can I mix accounts with and without proxy?**
A: Yes! Add proxy to `akun.txt` only for accounts that need it.

**Q: How to rotate IPs automatically?**
A: Use session-based proxy format: `socks5://user-session1:pass@host:port`

---

**Built by [Bayu5677](https://github.com/Bayu5677)**
