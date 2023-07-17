@echo off

set /p link="Digite o link> "

::Arquivação em mp4 (qualquer um bom) de playlists:
yt-dlp -f mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json --no-abort-on-error -o "%%(playlist_title)s/%%(playlist_index)s-%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%