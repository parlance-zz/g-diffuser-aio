from os import path
import time
import subprocess, os, shutil, sys
from dotenv import load_dotenv

from threading import Thread
import pystray_main

class ServerLogger(object):
    def __init__(self, log_path):
        self.terminal = sys.stdout
        try:
            self.log = open(log_path, "w") # overwrite log file on startup
        except:
            self.log = None
        return

    def write(self, message):
        self.terminal.write(message)
        if self.log: self.log.write(message)
        return

def main():
    base=path.dirname(path.dirname(__file__))
    sys.stdout = ServerLogger(path.join(base, "run.log"))

    # Load dotenv into environment

    load_dotenv(path.join(base, "config"))
    
    hfToken = os.environ.get('HF_API_TOKEN', '')
    if not hfToken or hfToken == '{your huggingface token}':
        print("ERROR: You need to register an account on HuggingFace, create an API token, and save it into the 'config' file in this directory")
        input("Press enter to exit")
        sys.exit(-1)
    if hfToken[0] == "{":
        print("ERROR: Don't wrap your token with {} brackets.")
        input("Press enter to exit")
        sys.exit(-1)

    # Run server

    pystray_thread = Thread(target=pystray_main.start_pystray, daemon=True)
    pystray_thread.start()

    host = os.environ.get("SD_GRPC_HOST", "localhost")
    port = os.environ.get("SD_GRPC_PORT", "50051")

    if host.lower() != "localhost":
        print("Using remote SD GRPC server: {0}:{1}".format(host, port))
        while True:
            time.sleep(2)
    else:
        print("Starting SD GRPC Server on {0}:{1}...".format(host, port))
        from sdgrpcserver import server
        server.main()
    
if __name__ == "__main__":
    main()
    print("Press enter continue...") # important so users get a chance to see grpc server startup errors
    input()