@echo off

echo "Download de playlists na melhor qualidade possivel em um mp4"
echo "Formato: %%(playlist_title)s/%%(playlist_index)s-%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
set /p link="Digite o link> "

::Download de playlists da mais alta qualidade em um mp4:
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json --no-abort-on-error -o "%%(playlist_title)s/%%(playlist_index)s-%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%