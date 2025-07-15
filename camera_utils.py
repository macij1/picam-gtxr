from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from datetime import datetime
import time
import os
import subprocess

def init_camera():
    try:
        picam2 = Picamera2()
    except Exception as e:
        print(f"No cams available: {e}")
        return None
    return picam2

def take_selfie(picam2):
    """
    Captures and stores a high-quality still image using the Pi Camera
    """
    # PiCamv2.1 max resolution: (3280,2464), PiCamv3  defaults to (4608, 2592)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"photos/selfie_{ts}.jpg"

    try:
        # Configure for still capture at max quality
        config = picam2.create_still_configuration(
            main={"size": (3280, 2464)}, 
            controls={
                "AfMode": 0,            # 0 = Manual focus
                "LensPosition": 0.0     # 0.0 ≈ infinity
            })
        picam2.configure(config)
        picam2.start()
        picam2.capture_file(path)
        print(f"Selfie taken and saved to {path}")
    except Exception as e:
        print(f"Error, Photo Unsuccessful: {e}")
    finally:
        picam2.stop()


def record_h264_segments(picam2, camera_manager, duration=7200, stop_event=None):
    """
    Records video segments and encodes in h264. 
    These can be merged and wrapped in an mp4 video using fmpeg - see fmpeg_processing.sh
    """
    try:
        # Configuration
        video_config = picam2.create_video_configuration(
            main={"size": (640, 480), "format": "XBGR8888"}, # for PiCamv3,this defaults to (1536, 864)
            controls={
                "FrameDurationLimits": (8333, 8333),  # 1/120 sec = 8333 μs
                # when not specified, exposure is automatic and limited by the framerate:
                #"ExposureTime": 300,  # Very short exposure (μs), adjust as needed
                #"AnalogueGain": 1.0,  # Low ISO, expecting high light
                "NoiseReductionMode": 0,  # cdn_off equivalent
                "AfMode": 0,            # 0 = Manual focus
                "LensPosition": 0.0     # 0.0 ≈ infinity
            })
        picam2.configure(video_config)
        picam2.start()

        segment_length = 30
        encoder = H264Encoder()

        i = 0
        start_time = time.time()
        while not (stop_event and stop_event.is_set()):
            filename = f"{camera_manager.main_video_path}video_{i:03d}.h264"
            pts_filename = f"{camera_manager.main_video_path}video_{i:03d}.pts"
            print(f"Recording segment: {filename}")
            with open(pts_filename, "w") as pts_output:
                picam2.start_recording(encoder, filename, pts=pts_filename)
                time.sleep(segment_length)
                picam2.stop_recording()
            i += 1
            if i > 100 and duration and (time.time() - start_time) >= duration: 
                print("Duration reached. Ending recording.")
                break
    
    except KeyboardInterrupt:
        print("Stopping recording due to keyboard interrupt.")
    except Exception as e:
        print(f"Error: Camera video configuration unsuccessful: {e}") 
    finally:
        picam2.stop()


####### Deprecated functionalities:

# Video in one single take, deprecated
def record_video(picam2, camera_manager, duration=120):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{camera_manager.main_video_path}video_{ts}.h264"
    try:
        print(f"Starting recording: {path}")
        encoder = H264Encoder()
        picam2.start_recording(encoder, path)
        time.sleep(duration)
        picam2.stop_recording()
        print("Recording successful")
    except Exception as e:
        print(f"Error, Photo Unsuccessful: {e}")

def record_and_pipe_video(picam2, camera_manager, duration=None, stop_event=None):
    # Configuration
    video_config = picam2.create_video_configuration(
        main={"size": (640, 480), "format": "XBGR8888"},
        controls={
            "FrameDurationLimits": (8333, 8333),  # 1/120 sec = 8333 μs
            "ExposureTime": 300,  # Very short exposure (μs), adjust as needed
            "AnalogueGain": 1.0,  # Low ISO
            "NoiseReductionMode": 0,  # cdn_off equivalent
        }
    )
    picam2.configure(video_config)
    output_pattern = f"{camera_manager.main_video_path}video%03d.mp4"

    framerate = 120
    segment_length = 10
    # Start ffmpeg subprocess for segmentation
    ffmpeg = subprocess.Popen([
        "ffmpeg",
        "-f", "h264",
        "-framerate", str(framerate),
        "-i", "pipe:0",
        "-c", "copy",
        "-f", "segment",
        "-segment_time", str(segment_length),
        "-reset_timestamps", "1",
        output_pattern
    ], stdin=subprocess.PIPE)

    # Start recording
    print(f"Starting recording: {output_pattern}")
    encoder = H264Encoder()
    output = FileOutput(ffmpeg.stdin)

    picam2.start()
    picam2.start_recording(encoder, output)

    try:
        print("Recording... Press Ctrl+C to stop.")
        start_time = time.time()
        while True:
            time.sleep(5)
            if stop_event and stop_event.is_set():
                print("Stop event received. Ending recording.")
                break
            if duration and (time.time() - start_time) >= duration:
                print("Duration reached. Ending recording.")
                break
    except KeyboardInterrupt:
        print("Stopping recording due to keyboard interrupt.")
    finally:
        picam2.stop_recording()
        ffmpeg.stdin.close()
        ffmpeg.wait()



