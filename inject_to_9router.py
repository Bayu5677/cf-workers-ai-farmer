#!/usr/bin/env python3
"""
Auto-inject Cloudflare tokens to 9Router dashboard via REST API
"""
import json, subprocess, re, sys

DASHBOARD = "http://localhost:20128"  # Edit this!

def inject_tokens(cf_keys_file="cf_keys.txt"):
    """Read tokens from cf_keys.txt and inject to 9Router"""
    tokens = []
    
    print(f"📖 Reading tokens from {cf_keys_file}...")
    try:
        with open(cf_keys_file, 'r') as f:
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
    except FileNotFoundError:
        print(f"❌ File not found: {cf_keys_file}")
        return False
    
    if not tokens:
        print("❌ No tokens found")
        return False
    
    print(f"📋 Loaded {len(tokens)} tokens\n")
    
    success = 0
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
        ], capture_output=True, text=True, timeout=10)
        
        try:
            resp = json.loads(result.stdout)
            if 'connection' in resp and 'id' in resp['connection']:
                print(f"✅ [{i:2d}/{len(tokens)}] {token['name']:30s} → {resp['connection']['id'][:8]}...")
                success += 1
            else:
                print(f"❌ [{i:2d}/{len(tokens)}] {token['name']:30s} → Error: {result.stdout[:80]}")
        except:
            print(f"❌ [{i:2d}/{len(tokens)}] {token['name']:30s} → Parse error")
    
    print(f"\n✨ Result: {success}/{len(tokens)} tokens injected!")
    print(f"📊 Dashboard: {DASHBOARD}/dashboard/providers")
    return success == len(tokens)

if __name__ == "__main__":
    # Allow custom dashboard URL as argument
    if len(sys.argv) > 1:
        DASHBOARD = sys.argv[1]
    
    inject_tokens()
