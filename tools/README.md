# Tools

This directory contains several tools for the robot:

| Executable         | Stable  | Description |
|--------------------|---------|-------------|
| camera_calibrate.py | Y | performs camera calibration using either a chessboard or asymmetric circle target. Target patterns are in the `patterns` folder. |
| cmd.py       | N | send various commands to the robot [work in progress] |
| image_view   | Y | subscribe to image messages and display them for debugging |
| mjpeg-server | Y | create a web server which serves up an mjpeg stream from a camera. Any web browser on any device can see this stream (easier than image_view) |
| video.py     | Y | capture images or a video clip from a camera |
| wevserver.py | N | serve up a web page containing debugging and status info for the robot |

**Note:** Please take stable with a grain of salt ... all of this is still in major development.

**Note:** There is some duplication between these, and it will eventually be sorted out.
