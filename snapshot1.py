import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import cv2
import numpy as np
import os

# Initialize GStreamer
Gst.init(None)

# Define the RTSP URI and output folder
rtsp_uri = "rtsp://your_rtsp_stream_uri_here"
output_folder = "output_images"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define a callback function to save each frame as an image
frame_number = 0
def save_frame_callback(frame):
    global frame_number
    frame_path = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
    cv2.imwrite(frame_path, frame)
    frame_number += 1

# Define a callback function to handle new samples
def on_new_sample(sink, data):
    sample = sink.emit("pull-sample")
    buffer = sample.get_buffer()
    success, info = buffer.map(Gst.MapFlags.READ)
    if success:
        frame_data = info.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
        save_frame_callback(frame)
        buffer.unmap(info)
    return Gst.FlowReturn.OK

# Create a GStreamer pipeline
pipeline = Gst.Pipeline()

# Create elements for the RTSP source, decode the video, and convert it to images
source = Gst.ElementFactory.make("rtspsrc", "source")
source.set_property("location", rtsp_uri)

decode = Gst.ElementFactory.make("decodebin", "decode")
decode.connect("pad-added", decodebin_pad_added, pipeline)

convert = Gst.ElementFactory.make("videoconvert", "convert")
sink = Gst.ElementFactory.make("autovideosink", "sink")

# Define a function to handle new pads when they are added to the pipeline
def decodebin_pad_added(element, pad, pipeline):
    pad.link(convert.get_static_pad("sink"))

# Add the elements to the pipeline
pipeline.add(source)
pipeline.add(decode)
pipeline.add(convert)
pipeline.add(sink)

# Connect the callback function to the sink element
sink.connect("new-sample", on_new_sample, None)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

try:
    loop = GLib.MainLoop()
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    pipeline.set_state(Gst.State.NULL)
