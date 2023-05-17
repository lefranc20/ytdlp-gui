# ytdlp-cmd_scripts
 Um monte de scripts em batch não-organizados para o programa yt-dlp.
### ytarc - Arquivação de canais
```sh
Arquivação da mais alta qualidade para mp4 de canais:\
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%(uploader)s/%(title)s[%(upload_date)s][url_or_id_is - %(id)s].%(ext)s" %link%
```
### ytmp4 - Qualidade qualquer em mp4
Baixar um video de uma qualidade qualquer em mp4:\
```sh
yt-dlp -f mp4 --embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail -o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%
 ```
### ytmp4b - Melhor qualidade em mp4
Baixar um video da melhor qualidade possivel em um mp4:\
```sh
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4 --embed-thumbnail --embed-metadata --embed-chapters --all-subs --embed-subs -o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%
```
### ytmsc - Música
```sh
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 192k --embed-metadata --embed-thumbnail --write-thumbnail -o "%(uploader)s/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s" %link%
```
### ytpls - Playlist
```sh
yt-dlp -f mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%%(playlist_title)s/%%(playlist_index)s-%%(title)s[%%(upload_date)s][url_or_id_is - %%(id)s].%%(ext)s" %link%
```
### yt-plsb - Playlist com as melhores qualidades possíveis em mp4's
```sh
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%%(playlist_title)s/%%(playlist_index)s-%%(title)s[%%(upload_date)s][url_or_id_is - %%(id)s].%%(ext)s" %link%
```
