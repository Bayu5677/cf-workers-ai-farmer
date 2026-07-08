# CF Workers AI Token Farmer — Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip3 install DrissionPage
apt install xvfb google-chrome-stable
```

### 2. Prepare akun.txt
Format: `email|password|proxy` (one per line)

**With Proxy (SOCKS5):**
```
user1@gmail.com|password123|socks5://proxy_user:proxy_pass@us.proxy.io:3000
user2@gmail.com|password456|socks5://proxy_user:proxy_pass@eu.proxy.io:3000
```

**Without Proxy:**
```
user3@gmail.com|password789
user4@gmail.com|password000
```

### 3. Run Farming
```bash
# All accounts with proxy
xvfb-run -a python3 cf_farmer.py

# Single account test
xvfb-run -a python3 cf_farmer.py --only user1@gmail.com

# Custom delay (15s between accounts)
xvfb-run -a python3 cf_farmer.py --delay 15

# Ignore proxy in akun.txt
xvfb-run -a python3 cf_farmer.py --no-proxy
```

### 4. Output
Tokens saved to `cf_keys.txt`:
```
cloudflare_user1|https://api.cloudflare.com/client/v4/accounts/xxx/ai/v1|cfut_xxx|[...]
cloudflare_user2|https://api.cloudflare.com/client/v4/accounts/yyy/ai/v1|cfut_yyy|[...]
```

## Proxy Support

- **SOCKS5:** `socks5://user:pass@host:port` (recommended)
- **HTTP:** `http://user:pass@host:port`
- **No auth:** `socks5://host:port` or `host:port`
- **Legacy:** `host:port:user:pass` (auto-convert)

## Troubleshooting

**Xvfb error:**
```bash
pkill Xvfb
xvfb-run -a python3 cf_farmer.py  # Use -a flag
```

**Chrome won't start:**
```bash
# Use chromium instead
sed -i 's|/usr/bin/google-chrome|/usr/bin/chromium-browser|g' cf_farmer.py
```

**Port 9200 conflict:**
```bash
# Change port in cf_farmer.py line ~73
sed -i 's/9200/9500/' cf_farmer.py
```

## Performance

- **Per account:** 5-8 minutes (Google OAuth + CF dashboard)
- **23 accounts:** ~2-3 hours sequential
- **With proxy:** Same speed + IP rotation for stealth

## Next: Inject to 9Router

Use `inject_to_9router.py` to auto-inject tokens to 9Router dashboard.
