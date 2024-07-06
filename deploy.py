import os
import subprocess
import shutil
from datetime import datetime

# Define your variables
HUGO_PROJECT_DIR = "/Users/francis/Development/AI-Arena/arena/"
PUBLIC_DIR = os.path.join(HUGO_PROJECT_DIR, "public")
OUTPUT_DIR = "/Users/francis/Development/AI-Arena/tmp/"
REPO_DIR = "/Users/francis/Development/AI-Arena/ghpages/"
GIT_REPO = "git@github.com:c1sc0c0/AI-Arena.git"
COMMIT_MESSAGE = f"Update generated site {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode()}")
        exit(1)
    else:
        print(result.stdout.decode())

def copy_tree(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_tree(s, d)
        else:
            shutil.copy2(s, d)

def main():
    # Change to the Hugo project directory
    os.chdir(HUGO_PROJECT_DIR)

    # Generate the Hugo site
    run_command("hugo")

    # Check if the public directory was generated
    if not os.path.exists(PUBLIC_DIR):
        print("Hugo build failed, public directory not found.")
        exit(1)

    # Copy the generated site to the output directory
    copy_tree(PUBLIC_DIR, REPO_DIR)

    # Change to the repository directory
    os.chdir(REPO_DIR)

    # Add the changes to git
    run_command("git add -A")

    # Commit the changes
    run_command(f"git commit -m '{COMMIT_MESSAGE}'")

    # Push the changes to GitHub
    run_command("git push origin main")

    print("Site successfully generated and published to GitHub Pages.")

if __name__ == "__main__":
    main()