for file in /everypreview/*.png; do
    magick "$file" -resize 512x512 -filter Lanczos -quality 95 -strip -sharpen 0x1.0 /out/$(basename "$file")
done
