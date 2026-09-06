playlist = "#EXTM3U\n\n"

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # লাইনকে '|' দিয়ে ভাগ করা হচ্ছে
        parts = [x.strip() for x in line.split("|")]

        # যদি লাইনে ৪টি জিনিস থাকে (Name | Group | Logo | URL)
        if len(parts) == 4:
            name, group, logo, url = parts
            playlist += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            playlist += f'{url}\n\n'
            
        # যদি লাইনে আগের মতো শুধু ২টি জিনিস থাকে (Name | URL)
        elif len(parts) == 2:
            name, url = parts
            playlist += f'#EXTINF:-1,{name}\n'
            playlist += f'{url}\n\n'
            
        else:
            print(f"Warning: এই লাইনটি ঠিক ফরম্যাটে নেই: {line}")

with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist)

print("Playlist generated successfully!")
