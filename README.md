# gtxr-picamera
This single-camera system was developed by the Georgia Tech Experimental Rocketry Club (GTXR) for the launch of "Live and Let Fly", in July 2025.

It enables different use-cases:

1. Automatic flight video recording: run_automatic_managerr.sh
2. Interactive flight video recording: run_picam_manager.sh
3. Remote picture triggering: take_selfie.sh

For more information, please contact Juan Macias(jromero74@gatech.edu).

## Software environment

The script env_setup.sh creates a python venv with all the necessary depedendencies, including [python3-picamera2](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf), which enables the use of Pi Camera module.

## Hardware environment

The system was tested on both Raspberry Pi Zero 2W and Raspberry Pi 5, and [camera modules](https://www.raspberrypi.com/documentation/accessories/camera.html) 2.1 and 3.
We powered the devices with power over USB during dev, and with a LiPo battery for launch.

## Console access
To develop, we preconfigured a headless Pi during flashing to connect to a local LAN, to enable remote access with SSH through a WiFi or Ethernet network.
Then, we configured console access through a USB Serial connection. To do so, follow the follwing tutorial: [here](https://github.com/macij1/gtxr-picamera/blob/main/USB-gadgetmode.md)

## Camera configuration

For Live and Let Fly, our camera was configured with the following parameters:

- Autofocus off
- Manual focus to inf
- Sensor mode:
    {'bit_depth': 10,
    'crop_limits': (768, 432, 3072, 1728),
    'exposure_limits': (9, 77193343, 20000),
    'format': SRGGB10_CSI2P,
    'fps': 120.13,
    'size': (1536, 864),
    'unpacked': 'SRGGB10'}

## Other resources

### Use of serial mockups

'socat -d -d pty,raw,echo=0 pty,raw,echo=0'
This should output two paths whose inputs and outputs are connected.

### [Camera software](<https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-apps>)
### [Raspberry Pi pinout](https://pinout.xyz/pinout/ground)
### [Raspberry Pi Camera module 3](https://datasheets.raspberrypi.com/camera/camera-module-3-product-brief.pdf)
# picam-gtxr
# picam-gtxr
# picam-gtxr
# picam-gtxr
