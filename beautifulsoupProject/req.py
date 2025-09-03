import os
import subprocess
import time


def remove_ghost_file():
    file_path = r"FetchedBookCovers\\দারবি"

    print("Trying to remove ghost file...")

    # Method 1: Check if file actually exists
    try:
        if os.path.exists(file_path):
            print("File exists in os.path.exists()")
        else:
            print("File doesn't exist in os.path.exists()")
    except:
        pass

    # Method 2: Force delete via command prompt
    try:
        result = subprocess.run(
            f'del /f /q /a "{file_path}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"Command result: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Command error: {e}")

    # Method 3: Use attrib command to remove attributes
    try:
        subprocess.run(f'attrib -r -s -h "{file_path}"', shell=True, check=True)
        print("Attributes removed")
    except:
        pass


remove_ghost_file()