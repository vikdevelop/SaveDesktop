import gc
import os, json, gi, argparse, shutil
from abc import ABC, abstractmethod
from functools import wraps, partial

from gi.repository import GLib, Gio
from localization import *
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Iterable, ParamSpec, TypeVar, Any, Generator, Optional, Callable
from enum import Enum
from pathlib import Path

# add command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save", help="Save the current configuration", action="store_true")
parser.add_argument("-i", "--import_", help="Import saved configuration", action="store_true")

args = parser.parse_args()

def get_kde_files(home):
    """
    This method saves the KDE Plasma's configuration files from ~/.config
    and ~/.local/share directories to ./xdg-config and ./xdg-data directories
    in resulting archive
    """
    
    config_dir = Path(f"{home}/.config")
    localshare_dir = Path(f"{home}/.local/share")

    kde_files = [
        (Path(f"{home}/.config/plasma-org.kde.plasma.desktop-appletsrc"), Path("./xdg-config/plasma-org.kde.plasma.desktop-appletsrc"), False),
        (Path(f"{home}/.local/share/plasma-systemmonitor"), Path("./xdg-config/plasma-systemmonitor"), True),
        (Path(f"{home}/.local/share/color-schemes"), Path("./xdg-config/color-schemes"), True),
        (Path(f"{home}/.config/plasmashellrc"), Path("./xdg-config/plasmashellrc"), False),
        (Path(f"{home}/.config/spectaclerc"), Path("./xdg-config/spectaclerc"), False),
        (Path(f"{home}/.config/gwenviewrc"), Path("./xdg-config/gwenviewrc"), False),
        (Path(f"{home}/.config/dolphinrc"), Path("./xdg-config/dolphinrc"), False),
        (Path(f"{home}/.local/share/dolphin"), Path("./xdg-data/dolphin"), True),
        (Path(f"{home}/.local/share/aurorae"), Path("./xdg-data/aurorae"), True),
        (Path(f"{home}/.config/plasmarc"), Path("./xdg-data/plasmarc"), False),
        (Path(f"{home}/.config/Kvantum"), Path("./xdg-data/Kvantum"), True),
        (Path(f"{home}/.local/share/sddm"), Path("./xdg-data/sddm"), True),
        (Path(f"{home}/.config/gtkrc"), Path("./xdg-data/gtkrc"), False),
        (Path(f"{home}/.config/latte"), Path("./xdg-data/latte"), True),
    ]

    # Add all files/dirs starting with "k" from ~/.config
    for item in config_dir.glob("k*"):
        kde_files.append((item, Path("./xdg-config") / item.name, item.is_dir()))

    # Add all files/dirs starting with "k" from ~/.local/share
    for item in localshare_dir.glob("k*"):
        kde_files.append((item, Path("./xdg-data") / item.name, item.is_dir()))

    return kde_files

class DesktopEnvironment(Enum):
    """
    Defines an enumeration of desktop environments and provides functionality
    to retrieve the current desktop environment.

    The DesktopEnvironment Enum represents various graphical desktop environments
    available across different Linux distributions. It offers a static method
    to determine the currently active desktop environment by interpreting system
    environment variables.

    :ivar GNOME: Represents the GNOME desktop environment.
    :ivar COSMIC_OLD: Represents the legacy version of the COSMIC desktop environment.
    :ivar COSMIC_NEW: Represents the new version of the COSMIC desktop environment.
    :ivar PANTHEON: Represents the Pantheon desktop environment.
    :ivar CINNAMON: Represents the Cinnamon desktop environment.
    :ivar BUDGIE: Represents the Budgie desktop environment.
    :ivar XFCE: Represents the XFCE desktop environment.
    :ivar MATE: Represents the MATE desktop environment.
    :ivar KDE_PLASMA: Represents the KDE Plasma desktop environment.
    :ivar DEEPIN: Represents the Deepin desktop environment.
    :ivar HYPRLAND: Represents the Hyprland desktop environment.
    """
    GNOME = 'GNOME'
    COSMIC_OLD = 'COSMIC (Old)'
    COSMIC_NEW = 'COSMIC (New)'
    PANTHEON = 'Pantheon'
    CINNAMON = 'Cinnamon'
    BUDGIE = 'Budgie'
    XFCE = 'Xfce'
    MATE = 'MATE'
    KDE_PLASMA = 'KDE Plasma'
    DEEPIN = 'Deepin'
    HYPRLAND = 'Hyprland'

    @staticmethod
    def get_current_de():
        """
        Determines the current desktop environment based on the `XDG_CURRENT_DESKTOP`
        environment variable.

        This static method retrieves the desktop environment string from the `XDG_CURRENT_DESKTOP`
        environment variable and maps it to a corresponding value from the `DesktopEnvironment`
        enumeration. If the current desktop environment is not in the predefined mappings,
        the method returns `None`.

        :raises KeyError: If the environment variable `XDG_CURRENT_DESKTOP` is not set.

        :return: The corresponding desktop environment from the `DesktopEnvironment`
            enumeration or `None` if no match is found.
        :rtype: Optional[DesktopEnvironment]
        """
        current = os.getenv('XDG_CURRENT_DESKTOP')

        de_mapping = {
            'GNOME': DesktopEnvironment.GNOME,
            'zorin:GNOME': DesktopEnvironment.GNOME,
            'ubuntu:GNOME': DesktopEnvironment.GNOME,
            'pop:GNOME': DesktopEnvironment.COSMIC_OLD,
            'COSMIC': DesktopEnvironment.COSMIC_NEW,
            'Pantheon': DesktopEnvironment.PANTHEON,
            'X-Cinnamon': DesktopEnvironment.CINNAMON,
            'Budgie:GNOME': DesktopEnvironment.BUDGIE,
            'XFCE': DesktopEnvironment.XFCE,
            'MATE': DesktopEnvironment.MATE,
            'KDE': DesktopEnvironment.KDE_PLASMA,
            'Deepin': DesktopEnvironment.DEEPIN,
            'Hyprland': DesktopEnvironment.HYPRLAND
        }

        return de_mapping.get(current)


class ConfigFiles:
    """
    Represents a collection of configuration files and their associated sources.

    This class provides methods for managing a list of configuration file sources,
    allowing the appending, extending, and reversing the source and destination. Each source is a
    tuple containing source and destination paths along with a boolean indicating
    whether the operation should be recursive.

    :ivar label: A label identifying the collection of configuration files.
    :type label: str
    :ivar sources: A list of tuples containing source and destination `Path` objects
        and a boolean indicating if the operation is recursive.
    :type sources: List[Tuple[Path, Path, bool]]
    """
    def __init__(self, label: str, sources: List[Tuple[Path, Path, bool]]):
        self.label = label
        self.sources = sources

    def append(self, source: Tuple[Path, Path, bool]) -> None:
        """
        Appends a new source tuple to the sources list.

        :param source: A tuple containing:
            - A `Path` object representing the source path.
            - A `Path` object representing the destination path.
            - A boolean indicating a specific attribute associated with the tuple.
        :return: None
        """
        self.sources.append(source)

    def extend(self, sources: Iterable[Tuple[Path, Path, bool]]) -> None:
        """
        Extends the existing sources list with the provided new sources.

        :param sources: An iterable containing tuples of source paths, destination
            paths, and a boolean flag. Each tuple represents a source file path
            (:class:`Path`), its corresponding destination path (:class:`Path`),
            and a boolean indicating a specific condition or flag.
        :return: None
        """
        self.sources.extend(sources)

    def reverse(self) -> 'ConfigFiles':
        """
        Reverses the source and destination paths for all entries in the current configuration.

        Each entry's source and destination are swapped, effectively reversing their roles
        in the configuration. A new instance of `ConfigFiles` is returned with the updated
        list of sources.

        :returns: A new `ConfigFiles` instance with reversed source and destination paths
        :rtype: ConfigFiles
        """
        return ConfigFiles(self.label, [
            (dest, source, recursive) for source, dest, recursive in self.sources
        ])


P = ParamSpec('P')
R = TypeVar('R')


class SandwichMeta(type(ABC)):
    """
    Metaclass used for creating classes with a specific behavior of wrapping
    an ``execute`` function with additional setup and teardown operations.

    This metaclass intercepts the creation of new classes. If the class has an
    ``execute`` method defined in its namespace, the metaclass will automatically
    wrap it with a new method ``run`` that ensures ``setup`` is called before, and
    ``teardown`` is called after, the execution of the original ``execute`` method.
    This can be used to enforce reusable pre- and post-execution logic in derived
    classes.

    """
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Any:
        if 'execute' in namespace:
            original_execute = namespace['execute']

            @wraps(original_execute)
            def wrapped_execute(self: Any, *args: P.args, **kwargs: P.kwargs) -> Any:
                self.setup()
                result = original_execute(self, *args, **kwargs)
                self.teardown()
                return result

            namespace['run'] = wrapped_execute

        return super().__new__(mcs, name, bases, namespace)


MAX_WORKERS = 3

class Config(ABC, metaclass=SandwichMeta):
    """
    Abstract base class to manage configuration files for various desktop environments.

    The class provides an interface and utility functions to collect and manage
    desktop environment-specific configuration files. It supports multiple desktop
    environments and allows the inclusion of optional configurations like backgrounds,
    icons, themes, fonts, and specific desktop environment extensions. Each desktop
    environment has a predefined list of configuration paths, which can be extended
    based on the current environment and active settings.

    :ivar config_files: A list of `ConfigFiles` objects, representing configuration
        file groups for syncing across desktop environments and optional
        user-defined settings.
    :type config_files: list
    """
    def __init__(self):
        environment = DesktopEnvironment.get_current_de()
        desktop = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP).replace(" ", "*")

        self.config_files = [
            ConfigFiles("Gtk settings", [
                (Path(f"{home}/.config/gtk-4.0"), Path("./gtk-4.0"), True),
                (Path(f"{home}/.config/gtk-3.0"), Path("./gtk-3.0"), True),
            ])
        ]

        if settings["save-backgrounds"]:
            self.config_files.append(
                ConfigFiles("Backgrounds", [
                    (Path(f"{home}/.local/share/backgrounds"), Path("./backgrounds"), True),
                ])
            )

        if settings["save-icons"]:
            self.config_files.append(
                ConfigFiles("Icons", [
                    (Path(f"{home}/.local/share/icons"), Path("./icons"), True),
                    (Path(f"{home}/.icons"), Path("./.icons"), True),
                ])
            )

        if settings["save-themes"]:
            self.config_files.append(
                ConfigFiles("Themes", [
                    (Path(f"{home}/.local/share/themes"), Path("./themes"), True),
                    (Path(f"{home}/.themes"), Path("./.themes"), True),
                ])
            )

        if settings["save-fonts"]:
            self.config_files.append(
                ConfigFiles("Fonts", [
                    (Path(f"{home}/.local/share/fonts"), Path("./fonts"), True),
                    (Path(f"{home}/.fonts"), Path("./.fonts"), True),
                ])
            )

        if settings["save-desktop-folder"]:
            self.config_files.extend([
                ConfigFiles("Desktop directory and GVFS metadata files", [
                    (Path(f"{desktop}"), Path("./Desktop"), True),
                    (Path(f"{home}/.local/share/gvfs-metadata"), Path("./gvfs-metadata"), True),
                ]),
            ])

        files_to_copy = {
            DesktopEnvironment.GNOME: [
                (Path(f"{home}/.config/gnome-background-properties"), Path("./gnome-background-properties"), True),
                (Path(f"{home}/.local/share/nautilus-python"), Path("./nautilus-python"), True),
                (Path(f"{home}/.config/gnome-control-center"), Path("./gnome-control-center"), True),
                (Path(f"{home}/.local/share/nautilus"), Path("./nautilus"), True),
                (Path(f"{home}/.config/gnome-shell"), Path("./gnome-shell"), True),
            ],
            DesktopEnvironment.PANTHEON: [
                (Path(f"{home}/.config/marlin"), Path("./marlin"), True),
                (Path(f"{home}/.config/plank"), Path("./plank"), True),
            ],
            DesktopEnvironment.CINNAMON: [
                (Path(f"{home}/.config/nemo"), Path("./nemo"), True),
                (Path(f"{home}/.cinnamon"), Path("./.cinnamon"), True)
            ],
            DesktopEnvironment.BUDGIE: [
                (Path(f"{home}/.config/budgie-desktop"), Path("./budgie-desktop"), True),
                (Path(f"{home}/.config/budgie-extras"), Path("./budgie-extras"), True),
                (Path(f"{home}/.config/nemo"), Path("./nemo"), True),
            ],
            DesktopEnvironment.COSMIC_OLD: [
                (Path(f"{home}/.local/share/gnome-shell"), Path("./gnome-shell"), True),
                (Path(f"{home}/.config/pop-shell"), Path("./pop-shell"), True),
            ],
            DesktopEnvironment.COSMIC_NEW: [
                (Path(f"{home}/.local/state/cosmic"), Path("./cosmic-state"), True),
                (Path(f"{home}/.config/cosmic"), Path("./cosmic"), True),
            ],
            DesktopEnvironment.XFCE: [
                (Path(f"{home}/.config/Thunar"), Path("./Thunar"), True),
                (Path(f"{home}/.config/xfce4"), Path("./xfce4"), True),
                (Path(f"{home}/.xfce4"), Path("./.xfce4"), True),
            ],
            DesktopEnvironment.MATE: [
                (Path(f"{home}/.config/caja"), Path("./caja"), True)
            ],
            DesktopEnvironment.KDE_PLASMA: get_kde_files(home),
            DesktopEnvironment.DEEPIN: [
                (Path(f"{home}/.local/share/deepin"), Path("./deepin-data"), True),
                (Path(f"{home}/.config/deepin"), Path("./deepin"), True),
            ],
            DesktopEnvironment.HYPRLAND: [
                (Path(f"{home}/.config/hypr"), Path("./hypr"), True),
            ],
        }

        # Save configs on individual desktop environments
        desktop_env_config = ConfigFiles(
            "Desktop environment configuration files",
            files_to_copy[DesktopEnvironment.get_current_de()]
        )

        if environment == DesktopEnvironment.GNOME and settings["save-extensions"]:
            desktop_env_config.extend([
                (Path(f"{home}/.local/share/gnome-shell"), Path("./gnome-shell"), True),
            ])

        if environment == DesktopEnvironment.CINNAMON and settings["save-extensions"]:
            desktop_env_config.extend([
                (Path(f"{home}/.local/share/cinnamon"), Path("./cinnamon"), True),
            ])

        if environment == DesktopEnvironment.COSMIC_OLD:
            desktop_env_config.extend([
                (Path(f"{home}/.local/share/nautilus"), Path("./nautilus"), True),
            ])

        if environment == DesktopEnvironment.KDE_PLASMA:
            if settings["save-backgrounds"]:
                desktop_env_config.extend([
                    (Path(f"{home}/.local/share/wallpapers"), Path("./xdg-data/wallpapers"), True)
                ])

            if settings["save-extensions"]:
                desktop_env_config.extend([
                    (Path(f"{home}/.local/share/plasma"), Path("./xdg-data/plasma"), True),
                ])

        self.config_files.append(desktop_env_config)

    @abstractmethod
    def setup(self) -> None:
        """
        An abstract method that must be implemented by all subclasses. The purpose
        of this method is to define setup-related operations for the implementing
        class.

        :raise NotImplementedError: If the method is not overridden in a subclass
        :return: None
        """
        pass

    @abstractmethod
    def run(self, max_workers: Optional[int] = None) -> None:
        """
        Represents an abstract method that must be implemented in a subclass.

        The run method is a placeholder to enforce implementation in derived
        classes. The actual behavior and logic must be defined by subclasses.

        This ensures that any class inheriting from the one defining this
        abstract method adheres to a specific interface.

        :abstractmethod:
            The method is declared as abstract and must be overridden.

        :return: None
        """
        pass

    @abstractmethod
    def teardown(self) -> None:
        """
        Represents an abstract method to handle teardown operations. This method
        is meant to be overridden by subclasses to define specific teardown logic
        required for resource cleanup, finalization, or post-execution processes.

        :abstractmethod:
            This is an abstract method and must be implemented in a subclass.
        """
        pass

    @staticmethod
    def __copy_source(source: Path, dest: Path, recursive: bool) -> None:
        """
        Copies a source file or directory to a destination path. If the source is a directory,
        it can optionally copy its contents recursively.

        :param source: The source Path to be copied. This can be a file or a directory.
        :type source: Path
        :param dest: The destination Path where the source will be copied to.
        :type dest: Path
        :param recursive: A boolean flag indicating whether the operation should be recursive
            if the source is a directory.
        :type recursive: bool
        :return: None
        :rtype: None
        """
        if not source.exists():
            return

        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            if recursive:
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, dest)
        except Exception as e:
            print(f"Error copying {source} to {dest}: {e}")

    def _parallel_copy(self, max_workers: Optional[int] = None) -> None:
        """
        Executes parallel copying tasks for a list of configuration files using a thread pool
        executor. Each configuration contains sources, destinations, and whether the copy
        operation should be recursive. The method processes all given configurations and ensures
        all copy operations are completed.

        :return: None
        """

        with ThreadPoolExecutor(max_workers=max_workers or MAX_WORKERS) as executor:
            for config in self.config_files:
                print(f"Processing: {config.label}")
                futures = []

                for source, dest, recursive in config.sources:
                    future = executor.submit(self.__copy_source, source, dest, recursive)
                    futures.append(future)

                for future in futures:
                    future.result()

class Save(Config):

    def __init__(self):
        super().__init__()

    @staticmethod
    def __flatpak_data_dirs() -> Generator[Tuple[Path, Path, Optional[Callable]], None, None]:
        blacklist = settings["disabled-flatpak-apps-data"] + ["cache"]

        dest_dir = Path(f"{CACHE}/save_config/app")
        if Path(f"{CACHE}/periodic_saving/saving_status").exists():
            dest_dir = Path(f"{CACHE}/periodic_saving/app")
        dest_dir.mkdir(exist_ok=True, parents=True)

        def ignore_cache_recursive(dir, entries):
            return [e for e in entries if e == "cache"]

        var_app_path = Path(f"{home}/.var/app")
        with os.scandir(var_app_path) as scanner:
            for entry in scanner:
                if entry.name not in blacklist:
                    source_path = var_app_path / entry.name
                    dest_path = dest_dir / entry.name
                    if entry.is_dir():
                        yield source_path, dest_path, ignore_cache_recursive
                    else:
                        yield source_path, dest_path, None


    def setup(self):
        """
        Sets up necessary directories based on the current desktop environment.

        This method checks if the current desktop environment is KDE Plasma and,
        if so, ensures that the directories relevant to this environment are created.
        It utilizes `Path.mkdir` with `exist_ok=True` to prevent errors if the
        directories already exist.

        :raises OSError: If directory creation fails due to insufficient permissions
            or other I/O errors.
        :return: None
        """
        if DesktopEnvironment.get_current_de() == DesktopEnvironment.KDE_PLASMA:
            create_dirs = [
                Path("xdg-config"),
                Path("xdg-data")
            ]

            map(lambda x: x.mkdir(exist_ok=True), create_dirs)

    def run(self, max_workers: Optional[int] = None) -> None:
        """
        Executes configuration backup and gathers system and application settings.

        This method backs up the system configuration from the `dconf` database and stores it as
        an `.ini` file. Additionally, it checks for Flatpak settings if installed, saving the list
        of installed Flatpak applications along with optional user data. This assists users in
        easily replicating their environment on another system or maintaining backups of critical
        settings.

        :raises OSError: If the system commands executed encounter issues during execution or fail.
        :raises KeyError: If required settings keys are not found in the `settings` dictionary.
        """
        print("Settings from the Dconf database")
        os.system("dconf dump / > ./dconf-settings.ini")

        self._parallel_copy(max_workers=max_workers)

        if flatpak:
            if settings["save-installed-flatpaks"]:
                print("List of installed Flatpak apps")
                os.system(
                    "ls /var/lib/flatpak/app/ | awk '{print \"flatpak install --system \" $1 \" -y\"}' > ./installed_flatpaks.sh"
                )
                os.system(
                    "ls ~/.local/share/flatpak/app | awk '{print \"flatpak install --user \" $1 \" -y\"}' > ./installed_user_flatpaks.sh"
                )

            if settings["save-flatpak-data"]:
                print("User data of installed Flatpak apps")
                with ThreadPoolExecutor(max_workers=max_workers or MAX_WORKERS) as executor:
                    futures = []
                    for source, dest, ignore_pattern in Save.__flatpak_data_dirs():
                        if source.is_dir():
                            futures.append(executor.submit(
                                shutil.copytree, source, dest, dirs_exist_ok=True, ignore=ignore_pattern
                            ))
                        else:
                            futures.append(executor.submit(shutil.copy2, source, dest))

                for future in futures:
                    future.result()

    def teardown(self):
        gc.collect()


class Import(Config):
    def __init__(self):
        self.get_original_variables_state()
        self.set_all_variables_to_true()
        super().__init__()
        self.__revert_copies()

    def __revert_copies(self):
        """
        self.config_files = [x.reverse() for x in self.config_files]
        Reverts the changes made to the configuration files and restores them to
        """
        self.config_files = [x.reverse() for x in self.config_files]
        
    def get_original_variables_state(self):
        """
        Get original state of variables for items to include in the configuration archive
        """
        print("getting original switchers state")
        
        self.icons_sw_state = settings["save-icons"]
        self.themes_sw_state = settings["save-themes"]
        self.backgrounds_sw_state = settings["save-backgrounds"]
        self.fonts_sw_state = settings["save-fonts"]
        self.desktop_sw_state = settings["save-desktop-folder"]
        self.extensions_sw_state = settings["save-extensions"]
        self.flatpak_list_sw_state = settings["save-installed-flatpaks"]
        self.flatpak_data_sw_state = settings["save-flatpak-data"]
        
    def set_all_variables_to_true(self):
        """
        Set all variables to true so that all items in the archive can be imported from the archive
        """
        
        print("setting all of them to TRUE")
        
        settings["save-icons"] = True
        settings["save-themes"] = True
        settings["save-backgrounds"] = True
        settings["save-fonts"] = True
        settings["save-desktop-folder"] = True
        settings["save-extensions"] = True
        settings["save-installed-flatpaks"] = True
        settings["save-flatpak-data"] = True
        
    def set_all_variables_to_original_state(self):
        """
        Set all listed variables to the user-defined state in the application
        """
        
        print("setting all of them to original state")
        
        settings["save-icons"] = self.icons_sw_state
        settings["save-themes"] = self.themes_sw_state
        settings["save-backgrounds"] = self.backgrounds_sw_state
        settings["save-fonts"] = self.fonts_sw_state
        settings["save-desktop-folder"] = self.desktop_sw_state
        settings["save-extensions"] = self.extensions_sw_state
        settings["save-installed-flatpaks"] = self.flatpak_list_sw_state
        settings["save-flatpak-data"] = self.flatpak_data_sw_state

    def import_kde_plasma_shell(self):
        # Copy all of xdg-config to ~/.config/
        os.system(f'cp -au xdg-config/. {home}/.config/')
        # Copy all of xdg-data to ~/.local/share/
        os.system(f'cp -au xdg-data/. {home}/.local/share/')

    def create_flatpak_desktop(self):
        os.system(f"cp {system_dir}/install_flatpak_from_script.py {CACHE}/")
        if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh") or not os.path.exists(f"{CACHE}/syncing/sync_status"):
            if not os.path.exists(f"{home}/.config/autostart"):
                os.mkdir(f"{home}/.config/autostart")
            if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
                with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                    fa.write(
                        f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {CACHE}/install_flatpak_from_script.py")

    def setup(self):
        """
        This method imports the user settings using the dconf command. For the backward compatibility reasons,
        it's also possible copy the 'user' file to the ~/.config/dconf directory, if presents in the archive
        """
        
        print("importing settings from the dconf-settings.ini file")
        if Path("user").exists():
            shutil.copytree("user", f"{home}/.config/dconf/") # backward compatibility with versions 2.9.4 and older
        else:
            if flatpak:
                os.system("dconf load / < ./dconf-settings.ini")
            else:
                os.system("echo user-db:user > temporary-profile")
                os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < dconf-settings.ini')

    def run(self, max_workers: Optional[int] = None):
        """
        This method first opens the setup() method to import Dconf settings,
        then imports KDE Plasma settings from the xdg-config and xdg-data folders.
        This is followed by running a parallel copy, and finally running the
        create_flatpak_desktop() method to set up the import of Flatpak applications
        and their data after logging back into the system.
        """
        
        self.setup()
        # For KDE Plasma, use the shell copy logic and skip the parallel Python copy
        if DesktopEnvironment.get_current_de() == DesktopEnvironment.KDE_PLASMA:
            self.import_kde_plasma_shell()
        self._parallel_copy(max_workers=max_workers)
        if flatpak:
            if any(os.path.exists(path) for path in ["app", "installed_flatpaks.sh", "installed_user_flatpaks.sh"]):
                self.create_flatpak_desktop()
        self.set_all_variables_to_original_state()

    def teardown(self) -> None:
        pass

if args.save:
    Save().run()
elif args.import_:
    Import().run()

