#!/bin/bash

mkdir -p nobg-1536-avif-100
mkdir -p nobg-1536-webp-99
mkdir -p nobg-1536-webp-100
mkdir -p nobg-1536-avif-99
mkdir -p nobg-512-webp-99
mkdir -p nobg-512-avif-100
mkdir -p nobg-512-webp-100
mkdir -p nobg-512-avif-99

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-1536-avif-100/$(basename "$0" .png).avif" ] || magick "$0" -quality 100 -resize 1536x1536 -define avif:compression-level=8 -filter Lanczos -sharpen 0x1.0 -strip nobg-1536-avif-100/$(basename "$0" .png).avif' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-1536-webp-99/$(basename "$0" .png).webp" ] || magick "$0" -quality 99 -resize 1536x1536 -define webp:method=6 -filter Lanczos -sharpen 0x1.0 -strip nobg-1536-webp-99/$(basename "$0" .png).webp' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-1536-webp-100/$(basename "$0" .png).webp" ] || magick "$0" -quality 100 -resize 1536x1536 -define webp:method=6 -filter Lanczos -sharpen 0x1.0 -strip nobg-1536-webp-100/$(basename "$0" .png).webp' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-1536-avif-99/$(basename "$0" .png).avif" ] || magick "$0" -quality 99 -resize 1536x1536 -define avif:compression-level=8 -filter Lanczos -sharpen 0x1.0 -strip nobg-1536-avif-99/$(basename "$0" .png).avif' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-512-webp-99/$(basename "$0" .png).webp" ] || magick "$0" -quality 99 -resize 512x512 -define webp:method=6 -filter Lanczos -sharpen 0x1.0 -strip nobg-512-webp-99/$(basename "$0" .png).webp' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-512-avif-100/$(basename "$0" .png).avif" ] || magick "$0" -quality 100 -resize 512x512 -define avif:compression-level=8 -filter Lanczos -sharpen 0x1.0 -strip nobg-512-avif-100/$(basename "$0" .png).avif' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-512-webp-100/$(basename "$0" .png).webp" ] || magick "$0" -quality 100 -resize 512x512 -define webp:method=6 -filter Lanczos -sharpen 0x1.0 -strip nobg-512-webp-100/$(basename "$0" .png).webp' '{}' \;

find everypreview -name '*.png' -exec sh -c '[ -e "nobg-512-avif-99/$(basename "$0" .png).avif" ] || magick "$0" -quality 99 -resize 512x512 -define avif:compression-level=8 -filter Lanczos -sharpen 0x1.0 -strip nobg-512-avif-99/$(basename "$0" .png).avif' '{}' \;
