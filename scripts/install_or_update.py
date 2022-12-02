from os import path
import os, sys, subprocess, os, shutil, re

class InstallOrUpdateLogger(object):
    def __init__(self, log_path):
        self.terminal = sys.stdout
        try:
            self.log = open(log_path, "w")
        except:
            self.log = None
        return
    def __del__(self):
        sys.stdout = self.terminal
        if self.log: self.log.close()
        return
    def write(self, message):
        self.terminal.write(message)
        if self.log:
            self.log.write(message)
            self.log.flush()
        return
    def flush(self):
        if self.log: self.log.flush()
        return

def main():
    base=path.dirname(path.dirname(__file__))
    sys.stdout = InstallOrUpdateLogger(path.join(base, "install_or_update.log"))

    # Create config if it doesn't exist
    
    if not path.exists(path.join(base, "config.ini")):
        shutil.copy(path.join(base, "dist/config.ini.dist"), path.join(base, "config.ini"))
    if not path.exists(path.join(base, "models.yaml")):
        shutil.copy(path.join(base, "dist/models.yaml.dist"), path.join(base, "models.yaml"))
    if not path.exists(path.join(base, "defaults.yaml")):
        shutil.copy(path.join(base, "dist/defaults.yaml.dist"), path.join(base, "defaults.yaml"))

    # Read the config

    repo = os.environ.get("AIO_REPO", "https://github.com/parlance-zz/g-diffuser-aio.git")
    branch = os.environ.get("AIO_BRANCH", "main") 

    # We can't rely on dotenv existing yet, stdlib only
    with open(path.join(base, "config.ini"), "r") as config_file:
        for line in config_file:
            repo_match = re.match(r'\s*AIO_REPO=(\S+)', line)
            branch_match = re.match(r'\s*AIO_BRANCH\s*=\s*(\S+)', line)

            if repo_match: repo=repo_match.group(1)
            if branch_match: branch=branch_match.group(1)

    # Update this repo, and any submodules
    results = []

    if not path.exists(path.join(base, ".git")):
        results.append(subprocess.run(("git", "init"), cwd=base))

    result = subprocess.run(("git", "remote", "get-url", "origin"), cwd=base, capture_output=True, text=True)
    results.append(result)
    has_remote = result.returncode == 0
    remote_url = result.stdout.strip()

    if not has_remote:
        results.append(subprocess.run(("git", "remote", "add", "origin", repo), cwd=base))
    elif remote_url != repo:
        results.append(subprocess.run(("git", "remote", "set-url", "origin", repo), cwd=base))

    results.append(subprocess.run(("git", "fetch"), cwd=base))
    results.append(subprocess.run(("git", "reset", "--hard", "origin/"+branch), cwd=base))
    results.append(subprocess.run(("git", "submodule", "update", "--init", "--recursive"), cwd=base))
    
    # Install the server dependencies

    os.environ["PIP_EXTRA_INDEX_URL"]="https://download.pytorch.org/whl/cu116"
    results.append(subprocess.run(("python", "-m", "flit", "install", "--pth-file"), cwd=os.path.join(base, "stable-diffusion-grpcserver")))

    # Verify installation by checking all subprocess results
    error_occurred = False
    for result in results:
        if result.returncode != 0:
            error_occurred = True
            break
    
    print("")
    if error_occurred:
        print("An error occurred while installing/updating. Please check the output above for more information.")
    else:
        print("Install or update completed successfully.")

if __name__ == "__main__":
    main()