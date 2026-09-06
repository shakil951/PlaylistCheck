import requests
import datetime

seen_urls = set()
cleaned_lines = []
playlist_content = ""
channel_count = 0

print("🔍 Checking channels for dead and duplicate links...\n")

with open("channels.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    stripped_line = line.strip()
    
    # ফাঁকা লাইন এবং কমেন্ট (#) গুলো যেমন ছিল তেমনই রেখে দিবে
    if not stripped_line or stripped_line.startswith("#"):
        cleaned_lines.append(line)
        continue

    parts = [x.strip() for x in stripped_line.split("|")]
    
    if len(parts) == 4:
        name, group, logo, url = parts
    elif len(parts) == 2:
        name, url = parts
        group, logo = "", ""
    else:
        cleaned_lines.append(line)
        continue

    # ১. ডুপ্লিকেট লিংক চেক
    if url in seen_urls:
        print(f"🔄 Duplicate removed: {name}")
        continue
    
    # ২. ডেড (নষ্ট) লিংক চেক
    try:
        # লিংকটি সচল আছে কি না তা চেক করছে
        r = requests.get(url, timeout=10, stream=True)
        if r.status_code == 200:
            seen_urls.add(url)
            cleaned_lines.append(line) # লিংক ঠিক থাকলে ফাইলে রেখে দিবে
            
            # প্লেলিস্টের জন্য টেক্সট তৈরি
            if len(parts) == 4:
                playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n\n'
            else:
                playlist_content += f'#EXTINF:-1,{name}\n{url}\n\n'
            channel_count += 1
            print(f"✅ Alive: {name}")
        else:
            print(f"❌ Dead link removed (Status {r.status_code}): {name}")
    except Exception as e:
        print(f"❌ Dead link removed (Timeout/Error): {name}")

# ৩. পরিষ্কার করা চ্যানেলগুলো আবার channels.txt এ সেভ করা
with open("channels.txt", "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

# ৪. নতুন প্লেলিস্ট জেনারেট করা
now = datetime.datetime.now()
last_update = now.strftime("%d-%b-%Y %I:%M %p")

header = "#EXTM3U\n"
header += f"# Developer: Farabi Ahmed Shakil\n"
header += f"# Last Update: {last_update}\n"
header += f"# Total Channels: {channel_count}\n\n"

with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(header + playlist_content)

print(f"\n🎉 Update Complete! Total Active Channels: {channel_count}")
