#!/bin/bash

# Menu de opções
echo "Escolha uma opção de download:"
echo "1. Baixar áudio"
echo "2. Baixar vídeo em melhor qualidade"
echo "3. Baixar vídeo em resolução específica"
echo "4. Baixar playlist"
read -p "Opção: " opcao

# Solicitar URL do vídeo ou playlist
read -p "Digite a URL do vídeo/playlist: " url

parseMetadata=(
    --parse-metadata "%(like_count)s:%(meta_likes)s"
    --parse-metadata "%(dislike_count)s:%(meta_dislikes)s"
    --parse-metadata "%(view_count)s:%(meta_views)s"
    --parse-metadata "%(average_rating)s:%(meta_rating)s"
    --parse-metadata "%(release_date>%Y-%m-%d,upload_date>%Y-%m-%d)s:%(meta_publish_date)s"
)

embed=(
    --xattrs --no-overwrites
    --sub-lang en --embed-subs --add-metadata
    --write-auto-subs --embed-metadata --embed-thumbnail --embed-chapters
)

case $opcao in
    1)
        # Baixar apenas o áudio
        read -p "Digite o formato do áudio (m4a ou mp3): " audioTipo
        "$YT_DLP" -f bestaudio -x --audio-format $audioTipo "${embed[@]}" "${parseMetadata[@]}" "$url"
        ;;
    2)
        # Baixar vídeo na melhor qualidade disponível
        "$YT_DLP" -f bestvideo+bestaudio --merge-output-format mp4 -o "%(uploader)s_-_%(title)s.%(ext)s" "${embed[@]}" "${parseMetadata[@]}" "$url"
        ;;
    3)
        # Solicitar resolução específica
        read -p "Digite a resolução (ex: 720): " res
        "$YT_DLP" -f "bestvideo[height<=$res]+bestaudio/best[height<=$res]" --merge-output-format mp4 -o "%(title)s_%(id)s.%(ext)s"  "${embed[@]}"  "${parseMetadata[@]}"    "$url"
        ;;
    4)
        # Baixar uma playlist inteira
        "$YT_DLP" -i "${embed[@]}" "${parseMetadata[@]}" "$url"
        ;;
    *)
        echo "Opção inválida."
        ;;
esac
