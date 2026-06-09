playlist = "#EXTM3U\n\n"

with open("channels.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        name, url, logo = line.split("|")

        playlist += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n'
        playlist += f'{url}\n\n'

with open("combined_playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist)

print("Playlist generated!")
