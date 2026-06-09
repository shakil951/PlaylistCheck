playlist = "#EXTM3U\n\n"

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        name, url = [x.strip() for x in line.split("|", 1)]

        playlist += f"#EXTINF:-1,{name}\n"
        playlist += f"{url}\n\n"

with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist)

print("Playlist generated!")
