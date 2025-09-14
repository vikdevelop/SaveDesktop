import hashlib, os
from savedesktop.globals import *

# Repeated XOR with SHA-256-hashed key
def xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Get CPU model
def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            return next((l.split(":",1)[1].strip() for l in f if "model name" in l), "")
    except:
        return ""

# Get motherboard model
def get_board_name():
    try:
        with open("/sys/devices/virtual/dmi/id/board_name") as f:
            return f.read().strip()
    except:
        return ""

# Get BIOS version
def get_bios_version():
    try:
        with open("/sys/devices/virtual/dmi/id/bios_version") as f:
            return f.read().strip()
    except:
        return ""

# Create a device fingerprint based on the CPU and MB model and BIOS version
def get_device_fingerprint():
    return "::".join([get_cpu(), get_board_name(), get_bios_version()])

class PasswordStore:
    def __init__(self, password=None):
        self.device_fingerprint = get_device_fingerprint()
        
        if password:
            self.password = password
            self.store_pwd()
        else:
            self.password = self.load_pwd()

    # Store the entered password to the {DATA}/password file
    def store_pwd(self):
        salt = os.urandom(16)  # 128-bit salt
        key_material = f"{self.device_fingerprint}::{salt.hex()}"
        key = hashlib.sha256(key_material.encode()).digest()

        encrypted = xor(self.password.encode(), key)

        with open(f"{DATA}/password", "wb") as f:
            f.write(salt + b"::" + encrypted)

    # Load the password stored in the {DATA}/password file
    def load_pwd(self):
        try:
            with open(f"{DATA}/password", "rb") as f:
                stored = f.read()
                salt, encrypted = stored.split(b"::", 1)
                try:
                    key_material = f"{self.device_fingerprint}::{salt.hex()}"
                    key = hashlib.sha256(key_material.encode()).digest()
                except:
                    key = None

                return xor(encrypted, key).decode()
        except Exception as e:
            print("[ERROR]", e)
            return None

