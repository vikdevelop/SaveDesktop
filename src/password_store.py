import hashlib, uuid, os, subprocess
from localization import *

def xor(data: bytes, key: bytes) -> bytes:
    # Repeated XOR with SHA-256-hashed key
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Get CPU Model
def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            return next((l.split(":",1)[1].strip() for l in f if "model name" in l), "")
    except:
        return ""

# Get Motherboard Name
def get_board_name():
    try:
        with open("/sys/devices/virtual/dmi/id/board_name") as f:
            return f.read().strip()
    except:
        return ""

# Get BIOS Version   
def get_bios_version():
    try:
        with open("/sys/devices/virtual/dmi/id/bios_version") as f:
            return f.read().strip()
    except:
        return ""

# Create a device hash based on the CPU model, the motherboard name and the BIOS version
def get_device_hash():
    parts = [get_cpu(), get_board_name(), get_bios_version()]
    return hashlib.sha256("::".join(parts).encode()).hexdigest()  # returns the hex string

class PasswordStore:
    def __init__(self, password=None):
        self.device_hash = get_device_hash()
        self.key = hashlib.sha256(self.device_hash.encode()).digest()

        if password:
            self.password = password
            self.store_pwd()
        else:
            self.password = self.load_pwd()
    
    # Encrypt the device hash and the entered password to the {DATA}/password file
    def store_pwd(self):
        encrypted = xor(self.password.encode(), self.key)
        with open(f"{DATA}/password", "wb") as f:
            f.write(self.device_hash.encode() + b"::" + encrypted)
    
    # Load the password from the {DATA}/password file and check the hashes
    def load_pwd(self):
        try:
            with open(f"{DATA}/password", "rb") as f:
                stored = f.read()
                stored_hash, encrypted = stored.split(b"::", 1)
                if stored_hash.decode() != self.device_hash:
                    raise ValueError("Device mismatch!")
                return xor(encrypted, self.key).decode()
        except Exception as e:
            print("[ERROR]", e)
            return None
