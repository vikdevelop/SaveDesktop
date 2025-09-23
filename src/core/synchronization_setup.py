import subprocess, re, os
from savedesktop.globals import *

def check_fs(folder):
    check_filesystem = subprocess.getoutput('df -T "%s" | awk \'NR==2 {print $2}\'' % folder)
    if not "gvfsd" in check_filesystem:
        if not "rclone" in check_filesystem:
            if not os.path.exists(f"{folder}/.stfolder"):
                return "You didn't select the cloud drive folder!"

# set up auto-mounting of the cloud drives after logging in to the system
def set_up_auto_mount(mount_type):
    if mount_type == "periodic-saving":
        cfile_subtitle = settings["periodic-saving-folder"]
    elif mount_type == "cloud-receiver":
        cfile_subtitle = settings["file-for-syncing"]
    else:
        cfile_subtitle = "none"

    if not cfile_subtitle == "none":
        if "gvfs" in cfile_subtitle:
            if "google-drive" in cfile_subtitle:
                pattern = r'.*/gvfs/([^:]*):host=([^,]*),user=([^/]*).*'
            elif "onedrive" in cfile_subtitle:
                pattern = r'.*/gvfs/([^:]+):host=([^,]+),user=([^/]+)'
            else:
                pattern = r'.*/gvfs/([^:]*):host=([^,]*),ssl=([^,]*),user=([^,]*),prefix=([^/]*).*'

            match = re.search(pattern, cfile_subtitle)

            if match:
                if "google-drive" in cfile_subtitle: # Google Drive
                    cloud_service = match.group(1)  # cloud_service for Google Drive
                    host = match.group(2)  # host for Google Drive
                    user = match.group(3)
                    ssl = None  # ssl is not relevant for Google Drive
                    prefix = None  # prefix is not relevant for Google Drive
                    cmd = f"gio mount {cloud_service}://{user}@{host}" # command for Google Drive
                elif "onedrive" in cfile_subtitle: # OneDrive
                    cloud_service = match.group(1)  # cloud_service for OneDrive
                    host = match.group(2)  # host for OneDrive
                    user = match.group(3) # user is not relevant for OneDrive
                    ssl = None  # ssl is not relevant for OneDrive
                    prefix = None  # prefix is not relevant for OneDrive
                    cmd = f"gio mount {cloud_service}://{user}@{host}" # command for OneDrive
                elif "dav" in cfile_subtitle: # DAV
                    cloud_service = match.group(1)  # cloud_service for DAV
                    host = match.group(2)  # host for DAV
                    ssl = match.group(3)  # ssl for DAV
                    user = match.group(4)  # user for DAV
                    if match.group(5): # prefix for DAV
                        prefix_old = match.group(5)
                        prefix = re.sub(r'gio mount |%2F', '/', prefix_old).replace('//', '').strip() # Replace 2%F with /
                    else:
                        prefix = ""
                    
                    if os.getenv("XDG_CURRENT_DESKTOP") in ["X-Cinnamon", "Budgie:GNOME"]:
                        fm = "nemo"
                    else:
                        fm = "nautilus"
                    cmd = (
                        f"output=$(secret-tool lookup object Nextcloud) && "
                        f"output=\"Positive signal\" || "
                        f"output=\"Negative signal\"\n"
                        f"if [[ \"$output\" == \"Positive signal\" ]]; then\n"
                        f"    gio mount davs://{user}@{host}{prefix}\n"
                        f"else\n"
                        f"    {fm} davs://{user}@{host}{prefix}\n"
                        f"fi"
                    )
            else:
                extracted_values = {
                    "cloud_service": cloud_service,
                    "host": host,
                    "user": user,
                    "prefix": prefix,
                    "cmd": cmd
                }
        elif os.path.exists(f"{cfile_subtitle}/.stfolder"):
            cmd = ""
        else:
            cmd = f"rclone mount {cfile_subtitle.split('/')[-1]}: {cfile_subtitle}" if not os.path.exists(f"{download_dir}/SaveDesktop/rclone_drive") else f"rclone mount savedesktop: {download_dir}/SaveDesktop/rclone_drive"

        synchronization_content = f'#!/usr/bin/bash\n{cmd}\nsleep 60s\n{sync_cmd}\n{periodic_saving_cmd}'
        if flatpak:
            synchronization_content += f'\npython3 {CACHE}/flatpaks_installer.py'
        with open(f"{DATA}/savedesktop-synchronization.sh", "w") as f:
            f.write(synchronization_content)

        os.makedirs(f'{home}/.config/autostart', exist_ok=True)
        open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", "w").write(f"[Desktop Entry]\nName=SaveDesktop (Synchronization)\nType=Application\nExec=sh {DATA}/savedesktop-synchronization.sh")

        [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.server.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"] if os.path.exists(path)]
    else:
        raise AttributeError("There aren't possible to get values from the periodic-saving-folder or file-for-syncing strings")
