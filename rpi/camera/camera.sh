#!/bin/bash
echo "Launching gst"

gst-launch-1.0 -v v4l2src device="/dev/video0" ! videoconvert ! clockoverlay ! \
videoscale ! video/x-raw,width=640, height=360 !  x264enc bitrate=256 speed-preset=ultrafast ! video/x-h264,profile=\"high\" ! \
mpegtsmux ! hlssink playlist-root=http://192.168.0.156:8080/camera location=segment_%05d.ts target-duration=1 max-files=10 playlist-length=1