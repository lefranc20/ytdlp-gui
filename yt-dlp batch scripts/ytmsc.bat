@echo off

echo "Música no music.youtube ou Soundcloud (O LIMITE É POR VOLTA DE 192k ou às vezes 160k)"
set /p link="Digite o link para baixar um álbum: "

::Música no music.youtube ou Soundcloud (O LIMITE É 192k):
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 192k --embed-metadata --embed-thumbnail --write-thumbnail -o "%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s" %link%