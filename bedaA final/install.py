import os
import subprocess

# List of required packages
required_packages = [
    "opencv-python",
    "face-recognition",
    "pyserial",
    "pyttsx3",
    "openpyxl"
]

def install_packages():
    """Install all necessary packages."""
    for package in required_packages:
        try:
            subprocess.check_call(["pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please try manually.")
        except Exception as e:
            print(f"An error occurred while installing {package}: {e}")

if __name__ == "__main__":
    install_packages()
