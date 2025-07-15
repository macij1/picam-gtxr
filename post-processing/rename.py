import os
import re
import sys

def rename_videos(directory):
    pattern = re.compile(r"^video_(\d+)\.pts$")
    files = os.listdir(directory)

    for filename in files:
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            new_filename = f"video_{number:03d}.pts"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            if old_path != new_path:
                print(f"Renaming: {filename} → {new_filename}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_videos.py /path/to/directory")
        sys.exit(1)

    dir_path = sys.argv[1]
    if not os.path.isdir(dir_path):
        print(f"Error: '{dir_path}' is not a directory.")
        sys.exit(1)

    rename_videos(dir_path)
