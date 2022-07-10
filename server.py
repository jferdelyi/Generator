#!/usr/bin/env python
import os

# Start server
os.chdir("server")
os.environ["FLASK_APP"] = "server.py"
os.system("flask run --host=0.0.0.0 -p 4242")

