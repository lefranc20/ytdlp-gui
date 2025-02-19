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

        # Define o padrão de nome do arquivo
        padrao_de_saida="./%(title)s [%(id)s].%(ext)s"


        # Escreve as legendas automáticas (especifique senão ele irá chamar todas as possíveis!): --write-auto-subs 
        # Executa o yt-dlp
        "$YT_DLP" --cookies-from-browser chrome -f "bestvideo[height<=$res]+bestaudio/best[height<=$res]" --merge-output-format mp4 --write-info-json --write-comments --all-subs --embed-subs --embed-thumbnail --embed-metadata -o "$padrao_de_saida" "$url"

        # Encontra o nome do arquivo MP4 baixado
        nome_do_video=$(ls ./*.mp4 2>/dev/null | head -n 1)

        # Verifica se o arquivo MP4 foi encontrado
        if [ -z "$nome_do_video" ]; then
        echo "Nenhum arquivo MP4 encontrado. Verifique o URL e a resolução."
        exit 1
        fi

        # Extrai o nome do arquivo JSON de informações
        info_json="${nome_do_video%.*}.info.json"

        # Verifica se o arquivo JSON existe
        if [ ! -f "$info_json" ]; then
        echo "Arquivo JSON de informações não encontrado."
        exit 1
        fi

        # Extrai e formata os metadados
        jq -r '
        "
        Title: \(.title)\n
        Description: \(.description)\n
        Views: \(.view_count)\n
        Likes: \(.like_count)\n
        Dislikes: \(.dislike_count)\n
        Comments Count: \(.comment_count)\n
        Text: \(.text)\n
        "
        ' "$info_json" > metadata.txt

        # Adiciona metadados ao vídeo
        ffmpeg -i "$nome_do_video" -c copy \
        -metadata title="$(jq -r '.title' "$info_json")" \
        -metadata description="$(jq -r '.description' "$info_json")" \
        -metadata comment="$(cat metadata.txt)" \
        "${nome_do_video%.mp4}_com_metadados.mp4"

        # Substitui o arquivo original e limpa arquivos extras
        mv "${nome_do_video%.mp4}_com_metadados.mp4" "$nome_do_video"
        rm "$info_json" metadata.txt
        ;;
    4)
        padrao_de_saida_playlist="./%(playlist_title)s/%(playlist_index)s-%(title)s [%(upload_date)s] [%(id)s].%(ext)s" 

        # Baixar uma playlist inteira
        "$YT_DLP" -o "$padrao_de_saida_playlist" "$url"
        ;;
    *)
        echo "Opção inválida."
        ;;
esac
