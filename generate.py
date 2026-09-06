import datetime

channel_list = ""
channel_count = 0

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        
        # ফাঁকা লাইন অথবা '#' দিয়ে শুরু হওয়া লাইনগুলো (কমেন্ট) এড়িয়ে যাবে
        if not line or line.startswith("#"):
            continue

        parts = [x.strip() for x in line.split("|")]

        # যদি লাইনে ৪টি জিনিস থাকে (Name | Group | Logo | URL)
        if len(parts) == 4:
            name, group, logo, url = parts
            channel_list += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            channel_list += f'{url}\n\n'
            channel_count += 1
            
        # যদি লাইনে ২টি জিনিস থাকে (Name | URL)
        elif len(parts) == 2:
            name, url = parts
            channel_list += f'#EXTINF:-1,{name}\n'
            channel_list += f'{url}\n\n'
            channel_count += 1
            
        else:
            print(f"Warning: এই লাইনটি ঠিক ফরম্যাটে নেই: {line}")

# বর্তমান সময় বের করা হচ্ছে 
now = datetime.datetime.now()
last_update = now.strftime("%d-%b-%Y %I:%M %p")

# প্লেলিস্টের হেডার তৈরি (আপনার নাম, চ্যানেল সংখ্যা এবং সময়)
header = "#EXTM3U\n"
header += f"# Developer: Farabi Ahmed Shakil\n"
header += f"# Last Update: {last_update}\n"
header += f"# Total Channels: {channel_count}\n\n"

# হেডার এবং চ্যানেল লিস্ট একসাথে যোগ করা
final_playlist = header + channel_list

# নতুন ফাইলে সেভ করা
with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(final_playlist)

print(f"Playlist generated successfully! Total Channels: {channel_count}")
