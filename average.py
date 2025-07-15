def compute_average_interval(file_path):
    with open(file_path, "r") as f:
        timestamps = [float(line.strip()) for line in f if line.strip()]

    if len(timestamps) < 2:
        print("Not enough timestamps to compute intervals.")
        return

    intervals = [t2 - t1 for t1, t2 in zip(timestamps[:-1], timestamps[1:])]
    avg_interval = sum(intervals) / len(intervals)

    print(f"Average interval: {avg_interval:.6f} ms")
    print(f"Approximate FPS: {((1 /1000)*avg_interval):.2f} frames/sec")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python average_interval.py timestamps.txt")
    else:
        compute_average_interval(sys.argv[1])

