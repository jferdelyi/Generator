#!/usr/bin/env python
import os
import signal
import sys

# Signal handler for ctrl+c
def signalHandler(sig, frame):
    os.system("pkill flask")
    os.system("pkill node")
    os.system("pkill 'ng serve'")
    os.system("pkill 'Python'")
    print("App closed")
    sys.exit(0)

# Bind signal SIGINT
signal.signal(signal.SIGINT, signalHandler)

# Start server
os.system("python3 server.py &")

# Start client
os.system("python3 client.py &")

# Wait for ctrl+c
signal.pause()

