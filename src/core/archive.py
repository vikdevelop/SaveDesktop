import os, sys, shutil, subprocess, argparse, re
from savedesktop.globals import *
from savedesktop.core.password_store import PasswordStore
from savedesktop.core.de_config import Save, Import

TEMP_CACHE = f"{CACHE}/workspace"
temp_file = f"{CACHE}/temp_file"

# Cleanup the cache dir before saving
def cleanup_cache_dir():
    print("Cleaning up the cache directory")
    try:
        shutil.rmtree(TEMP_CACHE)
    except FileNotFoundError:
        pass
    os.makedirs(TEMP_CACHE, exist_ok=True)
    os.chdir(TEMP_CACHE)

# Get password entered in the "Create a new password" dialog from the temporary file
def get_password():
    if os.path.exists(temp_file):
        with open(temp_file) as tmp:
            return tmp.read().strip()
    elif os.path.exists(f"{DATA}/password"):
        p = PasswordStore()
        return p.password

# Remove above temporary file
def remove_temp_file():
    if os.path.exists(temp_file):
        os.remove(temp_file)

password = get_password()

class Create:
    def __init__(self, dir_path):
        self.path_with_filename = dir_path
        print(f"Output path: {self.path_with_filename}")
        self.start_saving()

    def start_saving(self):
        cleanup_cache_dir()
        Save() # de_config.py

        # In the periodic saving mode, it's not allowed to save the
        # configuration without creating the archive
        if not self.path_with_filename.endswith(".sd.7z"):
            print("Moving the configuration to the user-defined directory")
            self._copy_config_to_folder()
        else:
            self._create_archive()

        print("Configuration saved successfully.")
        remove_temp_file()

    # Copy the configuration folder to the user-defined directory
    def _copy_config_to_folder(self):
        if os.path.exists(self.path_with_filename):
            shutil.rmtree(self.path_with_filename)

        shutil.move(TEMP_CACHE, self.path_with_filename)

    # Create a new ZIP archive with 7-Zip
    def _create_archive(self):
        items_to_backup = [f for f in os.listdir(".") if f not in ('saving_status', '*.7z')]
        cmd = ['7z', 'a', '-snL', '-mx=3', 'cfg.sd.7z', *items_to_backup]
        if settings["enable-encryption"] or os.path.exists(f"{CACHE}/pb"):
            if password:
                cmd.insert(4, "-mem=AES256")
                cmd.insert(5, f"-p{password}")

        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(proc.stdout)

        if proc.returncode not in (0, 1):
            # 0 = everything is OK, 1 = warning (e.g. file not found)
            raise OSError(f"7z failed: {proc.stderr}")
        else:
            print("7z finished with warnings:", proc.stderr)

        print("Moving the configuration archive to the user-defined directory")
        shutil.copyfile('cfg.sd.7z', self.path_with_filename)

class Unpack:
    def __init__(self, dir_path):
        self.path_with_filename = dir_path
        print(f"Input path: {self.path_with_filename}")
        self.start_importing()

    def start_importing(self):
        cleanup_cache_dir()
        self._check_config_type()
        self._replace_home_in_files(".", home)

        Import() # de_config.py

        print("Configuration imported successfully.")
        remove_temp_file()

    # Check, if the input is archive or folder
    def _check_config_type(self):
        # Check, if the input is folder or not
        if self.path_with_filename.endswith(".sd.zip") or self.path_with_filename.endswith(".sd.7z"):
            self._unpack_zip_archive()
        elif self.path_with_filename.endswith(".sd.tar.gz"):
            self._unpack_tar_archive()
        else:
            self._copy_folder_to_cache()

    # Replace original /home/$USER path with actual path in the dconf-settings.ini file and other XML files
    def _replace_home_in_files(self, root, home, patterns=(".xml", ".ini")):
        regex = re.compile(r"(?:/var)?/home/[^/]+/")
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                if filename.endswith(patterns):
                    path = os.path.join(dirpath, filename)
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    new_text = regex.sub(f"{home}/", text)
                    if new_text != text:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        print(f"Updated /home/$USER path in: {path}")

    # Copy the user-defined folder to the cache directory
    def _copy_folder_to_cache(self):
        print("Copying a folder with the configuration to the cache directory")
        shutil.copytree(self.path_with_filename, TEMP_CACHE, dirs_exist_ok=True, ignore_dangling_symlinks=True)

    # Unpack the ZIP archive with 7-Zip
    def _unpack_zip_archive(self):
        if password:
            # Check, if the password for archive is correct or not
            try:
                subprocess.run(
                    ['7z', 'e', '-so', f'-p{password}' if password else '', self.path_with_filename, 'dconf-settings.ini'],
                    capture_output=True, text=True, check=True
                )
            except subprocess.CalledProcessError as e:
                self.__handle_sync_error()
                first_error = next((l for l in e.stderr.splitlines() if "Wrong password" in l), None)
                raise ValueError(first_error or "Wrong password")
            print("Checking password is completed.")

        cmd = ['7z', 'x', '-y', '-snL']

        if password:
            cmd.append(f'-p{password}')

        cmd.extend([
            self.path_with_filename,
            f'-o{TEMP_CACHE}'
        ])

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if proc.returncode >= 7:
            raise OSError(proc.stderr)

    def __handle_sync_error(self):
        # If 7-Zip returns an error regarding an incorrect password and the {CACHE}/sync file
        # is available, the {DATA}/password and {CACHE}/temp_file files will be deleted
        # because them contain the incorrect password for the archive.
        if os.path.exists(f"{CACHE}/sync"):
            os.remove(f"{CACHE}/sync")
            if os.path.exists(f"{DATA}/password"):
                os.remove(f"{DATA}/password")
            subprocess.run(["notify-send", "An error occured", "Password is not enterred, or it's incorrect. Unable to continue."])

        remove_temp_file()

    # Unpack a legacy archive with Tarball (for backward compatibility)
    def _unpack_tar_archive(self):
        cmd = subprocess.run(["tar", "-xzf", self.path_with_filename, "-C", f"{TEMP_CACHE}"], capture_output=True, text=True, check=True)
        print(cmd.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", help="Create archive", type=str)
    parser.add_argument("-u", "--unpack", help="Unpack archive", type=str)
    args = parser.parse_args()

    if args.create:
        dir_path = args.create
        Create(dir_path)
    elif args.unpack:
        dir_path = args.unpack
        Unpack(dir_path)
    else:
        pass
