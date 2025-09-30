import os, sys, shutil, subprocess, argparse, re
from savedesktop.globals import *
from savedesktop.core.password_store import PasswordStore

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create", help="Create archive", type=str)
parser.add_argument("-u", "--unpack", help="Unpack archive", type=str)
args = parser.parse_args()

TEMP_CACHE = f"{CACHE}/workspace"
temp_file = f"{CACHE}/temp_file"

# Cleanup the cache dir before saving
def cleanup_cache_dir():
    print("Cleaning up the cache directory")
    try:
        shutil.rmtree(TEMP_CACHE)
    except:
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

class Create:
    def __init__(self):
        self.start_saving()

    def start_saving(self):
        cleanup_cache_dir()
        subprocess.run([sys.executable, "-m", "savedesktop.core.de_config", "--save"], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

        # In the periodic saving mode, it's not allowed to save the
        # configuration without creating the archive
        if settings["save-without-archive"] and not os.path.exists(f"{CACHE}/pb") or "Configuration-" in args.create:
            print("Moving the configuration to the user-defined directory")
            self._copy_config_to_folder()
        else:
            self._create_archive()

            print("Moving the configuration archive to the user-defined directory")
            shutil.copyfile('cfg.sd.zip', f"{args.create}.sd.zip")

        print("Configuration saved successfully.")
        remove_temp_file()

    # Copy the configuration folder to the user-defined directory
    def _copy_config_to_folder(self):
        open(f".folder.sd", "w").close()

        if os.path.exists(args.create):
            shutil.rmtree(args.create)

        shutil.move(TEMP_CACHE, f"{args.create}")

    # Create a new ZIP archive with 7-Zip
    def _create_archive(self):
        password = get_password()
        cmd = ['7z', 'a', '-tzip', '-mx=3', '-x!*.zip', '-x!saving_status', 'cfg.sd.zip', '.']
        if settings["enable-encryption"] or os.path.exists(f"{CACHE}/pb") and os.path.exists(f"{DATA}/password"):
            cmd.insert(4, "-mem=AES256")
            cmd.insert(5, f"-p{password}")

        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(proc.stdout)

        if proc.returncode not in (0, 1):
            # 0 = everything is OK, 1 = warning (e.g. file not found)
            raise OSError(f"7z failed: {proc.stderr}")
        else:
            print("7z finished with warnings:", proc.stderr)

class Unpack:
    def __init__(self):
        self.start_importing()

    def start_importing(self):
        self.import_file = args.unpack
        self.import_folder = args.unpack

        cleanup_cache_dir()
        self._check_config_type()
        self._replace_home_in_files(".", home)

        cmd = subprocess.run([sys.executable, "-m", "savedesktop.core.de_config", "--import_"], check=True, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
        print(cmd.stdout)

        print("Configuration imported successfully.")
        remove_temp_file()

    # Check, if the input is archive or folder
    def _check_config_type(self):
        if self.import_file.endswith(".sd.zip") or self.import_file.endswith(".sd.tar.gz"):
            self.is_folder = False
        else:
            self.is_folder = True

        # Check, if the input is folder or not
        if self.is_folder:
            self._copy_folder_to_cache()
        else:
            if self.import_file.endswith(".sd.zip"):
                self._unpack_zip_archive()
            elif self.import_file.endswith(".sd.tar.gz"):
                self._unpack_tar_archive()
            else:
                pass

    # Copy the user-defined folder to the cache directory
    def _copy_folder_to_cache(self):
        shutil.copytree(self.import_folder, TEMP_CACHE, dirs_exist_ok=True, ignore_dangling_symlinks=True)

    # Unpack the ZIP archive with 7-Zip
    def _unpack_zip_archive(self):
        password = get_password()

        if password:
            # Check if the password for archive is correct or not
            try:
                subprocess.run(
                    ['7z', 'e', '-so', f'-p{password}' if password else '', self.import_file, 'dconf-settings.ini'],
                    capture_output=True, text=True, check=True
                )
            except subprocess.CalledProcessError as e:
                self.__handle_sync_error()
                first_error = next((l for l in e.stderr.splitlines() if "Wrong password" in l), None)
                raise ValueError(first_error or "Wrong password")
            print("Checking password is completed.")

        cmd = subprocess.run(
            ['7z', 'x', '-y', f'-p{password}', self.import_file, f'-o{TEMP_CACHE}'],
            capture_output=True, text=True, check=True
        )
        print(cmd.stdout)

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
        cmd = subprocess.run(["tar", "-xzf", self.import_file, "-C", f"{TEMP_CACHE}"], capture_output=True, text=True, check=True)
        print(cmd.stdout)

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

if args.create:
    Create()
elif args.unpack:
    Unpack()
else:
    pass
