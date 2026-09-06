import os
import requests
import datetime

seen_urls = set()
cleaned_lines = []
playlist_content = ""
channel_count = 0

# গিটহাব থেকে সিগন্যাল নেওয়া হচ্ছে যে কোডটি কীভাবে রান হয়েছে
event_name = os.environ.get('GITHUB_EVENT_NAME', 'workflow_dispatch')
check_dead_links = (event_name == 'workflow_dispatch')

if check_dead_links:
    print("🔍 Manual Run: Checking channels for dead and duplicate links...\n")
else:
    print("⚡ Auto Run: Generating playlist instantly without checking dead links...\n")

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

    # ডুপ্লিকেট লিংক চেক (সবসময় করবে)
    if url in seen_urls:
        print(f"🔄 Duplicate removed: {name}")
        continue
    
    is_alive = True
    
    # শুধুমাত্র ম্যানুয়ালি রান করলেই ডেড লিংক চেক করবে
    if check_dead_links:
        try:
            r = requests.get(url, timeout=10, stream=True)
            if r.status_code != 200:
                is_alive = False
                print(f"❌ Dead link removed (Status {r.status_code}): {name}")
            else:
                print(f"✅ Alive: {name}")
        except Exception as e:
            is_alive = False
            print(f"❌ Dead link removed (Timeout/Error): {name}")
    else:
        # অটো রানের সময় ধরে নিবে যে লিংকটি সচল আছে
        print(f"⏩ Added (Skipped check): {name}")
    
    # লিংক সচল থাকলে বা চেক স্কিপ করলে প্লেলিস্টে যোগ করবে
    if is_alive:
        seen_urls.add(url)
        cleaned_lines.append(line)
        
        if len(parts) == 4:
            playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n\n'
        else:
            playlist_content += f'#EXTINF:-1,{name}\n{url}\n\n'
        channel_count += 1

# পরিষ্কার করা চ্যানেলগুলো আবার channels.txt এ সেভ করা
with open("channels.txt", "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

# নতুন প্লেলিস্ট জেনারেট করা
now = datetime.datetime.now()
last_update = now.strftime("%d-%b-%Y %I:%M %p")

header = "#EXTM3U\n"
header += f"# Developer: Farabi Ahmed Shakil\n"
header += f"# Last Update: {last_update}\n"
header += f"# Total Channels: {channel_count}\n\n"

with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(header + playlist_content)

print(f"\n🎉 Update Complete! Total Active Channels: {channel_count}")
