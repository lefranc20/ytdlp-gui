@echo off

echo "Download de playlists no formato mp4"
echo "Formato: %%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
set /p link="Digite o link> "

::Download de playlists no formato mp4:
yt-dlp -f mp4 --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json --no-abort-on-error -o "%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%