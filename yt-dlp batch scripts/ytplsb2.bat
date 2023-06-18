@echo off

set /p link="Digite o link> "

::Arquivação da mais alta qualidade para mp4 de playlists:
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json --no-abort-on-error -o "%%(playlist_title)s/%%(title)s[%%(upload_date)s][url_or_id_is - %%(id)s].%%(ext)s" %link%