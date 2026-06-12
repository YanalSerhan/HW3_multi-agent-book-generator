import urllib.request
import json
import time
import sys

REPO = "YanalSerhan/HW3_multi-agent-book-generator"
COMMIT = "669695d"
URL = f"https://api.github.com/repos/{REPO}/commits/{COMMIT}/check-runs"

print(f"Waiting for CI results on {COMMIT}...")
for _ in range(40):
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if not data.get("check_runs"):
                print("No check runs found yet...")
            else:
                run = data["check_runs"][0]
                status = run.get("status")
                conclusion = run.get("conclusion")
                print(f"Status: {status}, Conclusion: {conclusion}")
                if status == "completed":
                    if conclusion == "success":
                        print("\n✅ GREEN ON GITHUB")
                        sys.exit(0)
                    else:
                        print(f"\n❌ RED ON GITHUB: {conclusion}")
                        sys.exit(1)
    except Exception as e:
        print(f"Error checking API: {e}")
    time.sleep(10)
print("Timeout waiting for CI.")
sys.exit(2)
