#!/usr/bin/env python
import os

# Start server
os.chdir("server")
os.environ["FLASK_APP"] = "server.py"
os.system("python -m flask run")

