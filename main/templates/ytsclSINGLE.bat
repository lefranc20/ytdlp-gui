@echo off

echo "Musica no music.youtube ou Soundcloud (O LIMITE E POR VOLTA DE 192k (ACHO) ou as vezes 160k)"
echo "Formato: %%(uploader)s - %%(title)s.%%(ext)s"
set /p link="Digite o link para baixar um album no music.youtube/artista no soundcloud: "

::Musicas unicas no music.youtube ou Soundcloud:
yt-dlp -f bestaudio --extract-audio --audio-format m4a --audio-quality 128k --embed-metadata --embed-thumbnail -o "%%(uploader)s - %%(title)s.%%(ext)s" %link%