import requests

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        
        if not line:
            continue

        parts = [x.strip() for x in line.split("|")]
        
        # নতুন ৪ ভাগের ফরম্যাট থেকে Name এবং URL আলাদা করা
        if len(parts) == 4:
            name = parts[0]
            url = parts[3]
        # পুরোনো ২ ভাগের ফরম্যাট থেকে Name এবং URL আলাদা করা
        elif len(parts) == 2:
            name = parts[0]
            url = parts[1]
        else:
            continue # ভুল লাইন হলে এড়িয়ে যাবে

        try:
            # লিংকটি চেক করা হচ্ছে
            r = requests.get(url, timeout=10, stream=True)
            
            if r.status_code == 200:
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")
                
        except:
            print(f"❌ {name}")
