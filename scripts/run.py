from os import path
import time
import os, sys
from dotenv import load_dotenv

from threading import Thread
from install_or_update import SimpleLogger

if os.name == "nt":
    import pystray_main

def main():
    base=path.dirname(path.dirname(__file__))
    logger = SimpleLogger(path.join(base, "run.log"))

    # Load dotenv into environment

    load_dotenv(path.join(base, "config.ini"))
    
    host = os.environ.get("SD_GRPC_HOST", "localhost")
    port = os.environ.get("SD_GRPC_PORT", "50051")

    if host.lower() == "localhost": # only check for hf token if we are starting a local server
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

    if os.name == "nt":
        pystray_thread = Thread(target=pystray_main.start_pystray, daemon=True)
        pystray_thread.start()

    if host.lower() != "localhost": # don't start the server if we have a remote sdgrpc host
        print("Using remote SD GRPC server: {0}".format(host))
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