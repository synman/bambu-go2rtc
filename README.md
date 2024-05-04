# bambu-go2rtc
 go2rtc mjpeg streamer for bambu printers

## Notice
Based on PoCs found in https://github.com/bambulab/BambuStudio/issues/1536#issuecomment-1811916472 that were optimized in [pybambu](https://github.com/greghesp/pybambu)

### Dependencies
* [Python3](https://www.python.org/downloads/)
* [go2rtc](https://github.com/AlexxIT/go2rtc/releases)

### Usage
* `PRINTER_ADDRESS=192.168.1.100 PRINTER_ACCESS_CODE=12345678 ./go2rtc_linux_arm64` with your Bambu printer's `hostname` or IP address and your respective `access_code` for LAN Only Mode
* Use the included shellscripts ([mac](https://github.com/synman/bambu-go2rtc/blob/main/run-on-mac.sh) / [linux arm](https://github.com/synman/bambu-go2rtc/blob/main/run-on-linux-arm.sh)) as reference and make the necessary adjustments for your environment
* Live Stream - [http://localhost:1984/api/stream.mjpeg?src=bambu_camera](http://localhost:1984/api/stream.mjpeg?src=bambu_camera)
* Single Frame - [http://localhost:1984/api/frame.jpeg?src=bambu_camera](http://localhost:1984/api/frame.jpeg?src=bambu_camera)
* RTSP (VLC/etc) - [rtsp://localhost:8554/bambu_camera](rtsp://localhost:8554/bambu_camera)

### Screenshot

<img width="1667" alt="Screenshot 2024-01-09 at 2 05 49 AM" src="https://github.com/synman/bambu-go2rtc/assets/1299716/6f808120-e895-492c-bc0d-605996c7247b">
