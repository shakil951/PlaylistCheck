import requests

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        name, url = [x.strip() for x in line.split("|", 1)]

        try:
            r = requests.get(url, timeout=10, stream=True)

            if r.status_code == 200:
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")

        except:
            print(f"❌ {name}")
