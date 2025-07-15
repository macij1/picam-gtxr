#!/bin/bash

# Define video directories here:
DIRS=("/Users/juanmaciasromero/Desktop/Pi/code/gtxr-picamera/videos/videos_20250713_111722")

for DIR in "${DIRS[@]}"
do
    echo "Processing $DIR"

    cd "$DIR" || { echo "Directory $DIR not found"; continue; }

    ls video*.h264 | sort | sed "s/^/file '/;s/$/'/" > files.txt

    ffmpeg -r 110 -f concat -safe 0 -i files.txt -c:v libx264 -preset slow -crf 18 "$DIR"_real_time.mp4

    ffmpeg -i "$DIR"_real_time.mp4 -vf "setpts=4*PTS" -an "$DIR"_slowmo.mp4

    cd ..
done

