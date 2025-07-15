import os
import subprocess

def run_ffmpeg_concat(h264_dir, output_path):
    # Step 1: Find all .h264 and .pts files
    h264_files = sorted([
        f for f in os.listdir(h264_dir) if f.endswith(".h264")
    ])

    # Step 2: Load timestamps
    entries = []
    for f in h264_files:
        base = os.path.splitext(f)[0]
        pts_path = os.path.join(h264_dir, base + ".pts")
        if not os.path.exists(pts_path):
            raise FileNotFoundError(f"Missing timestamp for {f}")
        with open(pts_path) as pts_file:
            pts = float(pts_file.readline().strip())
        entries.append((f, pts))

    # Step 3: Sort by PTS
    entries.sort(key=lambda x: x[1])

    # Step 4: Compute durations
    timestamps = [e[1] for e in entries]
    durations = [t2 - t1 for t1, t2 in zip(timestamps[:-1], timestamps[1:])]
    durations.append(durations[-1])  # Repeat last duration

    # Step 5: Convert to .ts
    ts_dir = os.path.join(h264_dir, "ts_segments")
    os.makedirs(ts_dir, exist_ok=True)

    ts_files = []
    for (h264_file, _), duration in zip(entries, durations):
        input_path = os.path.join(h264_dir, h264_file)
        ts_file = os.path.join(ts_dir, h264_file.replace(".h264", ".ts"))
        subprocess.run([
            "ffmpeg", "-y",
            "-r", "120",  # Assume frames were recorded at 120 FPS
            "-i", input_path,
            "-c:v", "copy",
            "-f", "mpegts",
            ts_file
        ], check=True)
        ts_files.append((ts_file, duration))

    # Step 6: Generate ffconcat
    concat_path = os.path.join(h264_dir, "video.ffconcat")
    with open(concat_path, "w") as f:
        f.write("ffconcat version 1.0\n")
        for ts_file, duration in ts_files:
            f.write(f"file '{ts_file}'\n")
            f.write(f"duration {duration:.6f}\n")

    # Step 7: Run ffmpeg to stitch together
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", concat_path,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        output_path
    ], check=True)

    print(f"✅ Final stitched video written to: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python stitch_video_from_pts.py <h264_dir> <output.mp4>")
        sys.exit(1)

    run_ffmpeg_concat(sys.argv[1], sys.argv[2])
