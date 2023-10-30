Um script em batch com a finalidade de construir o teu proprio template de execução do yt-dlp.


# Snippets
Alguns snippets dos mais utilizados, caso tu queira copiar, abaixo:
### ytarc - Arquivação de canais na melhor qualidade possível
```cmd
Arquivação da mais alta qualidade para mp4 de canais:
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%(uploader)s/%(title)s[%(upload_date)s][url_or_id_is - %(id)s].%(ext)s" %link%
```
### ytmp4 - Vídeo em uma qualidade pré-definida no Youtube (normalmente em 720p)
Baixar um video de uma qualidade qualquer em mp4:
```cmd
yt-dlp -f mp4 --embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail -o "%(title)s [%(upload_date)s] [%(id)s].%(ext)s" %link%
 ```
### ytmsc - Música
No download de musicas:
``` cmd
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 192k --embed-metadata --embed-thumbnail --write-thumbnail -o "%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s" %link%
```
### ytpls - Playlist em qualidade pré-definida no Youtube
Para playlists do youtube:
```cmd
yt-dlp -f mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%(playlist_title)s/%(playlist_index)s-%(title)s[%(upload_date)s][url_or_id_is - %(id)s].%(ext)s" %link%
```