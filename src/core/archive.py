import os, sys, shutil, subprocess, argparse, re
from savedesktop.globals import *

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create", help="Create archive", type=str)
parser.add_argument("-u", "--unpack", help="Unpack archive", type=str)
args = parser.parse_args()

def get_password():
    temp_file = f"{CACHE}/temp_file"
    if os.path.exists(temp_file):
        with open(temp_file) as tmp:
            return tmp.read().strip()
    else:
        return None

def remove_temp_file():
    try:
        os.remove(f"{CACHE}/temp_file")
    except FileNotFoundError:
        pass

class Create:
    def __init__(self):
        self.start_saving()

    def start_saving(self):
        self._cleanup_cache_dir()
        subprocess.run([sys.executable, "-m", "savedesktop.core.config", "--save"], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

        print("Creating and moving the configuration archive or folder to the user-defined directory")

        if settings["save-without-archive"]:
            self._copy_config_to_folder()
        else:
            self._create_archive()
            shutil.copyfile('cfg.sd.zip', f"{args.create}.sd.zip")

        print("Configuration saved successfully.")
        remove_temp_file()

    def _cleanup_cache_dir(self):
        # Cleanup the cache dir before importing
        print("Cleaning up the cache directory")
        save_cache_dir = f"{CACHE}/save_config"
        try:
            shutil.rmtree(save_cache_dir)
        except:
            pass
        os.makedirs(save_cache_dir, exist_ok=True)
        os.chdir(save_cache_dir)

    def _copy_config_to_folder(self):
        open(f"{CACHE}/save_config/.folder.sd", "w").close()
        shutil.move(f"{CACHE}/save_config", f"{args.create}")

    def _create_archive(self):
        password = get_password()
        cmd = ['7z', 'a', '-tzip', '-mx=3', '-x!*.zip', '-x!saving_status', 'cfg.sd.zip', '.']
        if settings["enable-encryption"]:
            cmd.insert(4, "-mem=AES256")
            cmd.insert(5, f"-p{password}")

        proc = subprocess.run(cmd, capture_output=True, text=True)

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

        self._cleanup_cache_dir()
        self._check_config_type()

        # Check, if the input is folder or not
        if self.is_folder:
            self._copy_folder_to_cache()
        else:
            if self.import_file.endswith(".sd.zip"):
                self._unpack_zip_archive()

            elif ".sd.tar.gz" in self.import_file:
                self._unpack_tar_archive()

        self._replace_home_in_files(".", home)
        subprocess.run([sys.executable, "-m", "savedesktop.core.config", "--import_"], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

        self._remove_status_file()

        print("Configuration imported successfully.")
        remove_temp_file()

    def _cleanup_cache_dir(self):
        # Cleanup the cache dir before importing
        print("Cleaning up the cache directory")
        imp_cache_dir = f"{CACHE}/import_config"
        try:
            shutil.rmtree(imp_cache_dir)
        except:
            pass
        os.makedirs(imp_cache_dir, exist_ok=True)
        os.chdir(imp_cache_dir)

        # Create a txt file to prevent removing the cache's content after closing the app window
        open("import_status", "w").close()

    def _check_config_type(self):
        if self.import_file.endswith(".sd.zip") or self.import_file.endswith(".sd.tar.gz"):
            self.is_folder = False
        else:
            self.is_folder = True

    def _copy_folder_to_cache(self):
        shutil.copytree(self.import_folder, f"{CACHE}/import_config", dirs_exist_ok=True, ignore_dangling_symlinks=True)

    def _unpack_zip_archive(self):
        password = get_password()

        if password:
            try:
                subprocess.run(
                    ['7z', 'e', '-so', f'-p{password}' if password else '', self.import_file, 'dconf-settings.ini'],
                    capture_output=True, text=True, check=True
                )
            except subprocess.CalledProcessError as e:
                first_error = next((l for l in e.stderr.splitlines() if "Wrong password" in l), None)
                raise ValueError(first_error or "Wrong password")
            print("Checking password is completed.")

        subprocess.run(
            ['7z', 'x', '-y', f'-p{password}', self.import_file, f'-o{CACHE}/import_config'],
            capture_output=False, text=True, check=True
        )

    def _unpack_tar_archive(self):
        subprocess.run(["tar", "-xzf", self.import_file, "-C", f"{CACHE}/import_config"],capture_output=True, text=True, check=True)

    # Replace original /home/$USER path with actual path in the dconf-settings.ini file and other XML files
    def _replace_home_in_files(self, root, home, patterns=(".xml", ".ini")):
        regex = re.compile(r"/home/[^/]+/")
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

    def _remove_status_file(self):
        if all(not os.path.exists(p) for p in [
            f"{CACHE}/import_config/app",
            f"{CACHE}/import_config/installed_flatpaks.sh",
            f"{CACHE}/import_config/installed_user_flatpaks.sh"
        ]):
            os.remove("import_status")

if args.create:
    Create()
elif args.unpack:
    Unpack()
else:
    pass
