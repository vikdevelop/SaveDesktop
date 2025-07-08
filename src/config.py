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
            ConfigFiles("Desktop folder", [
                (Path(f"{desktop}"), Path("./Desktop/"), True),
            ]),
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
                ConfigFiles("GVFS metadata files", [
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
            DesktopEnvironment.KDE_PLASMA: [
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
                (Path(f"{home}/.local/share/[k]*"), Path("./xdg-data/[k]*"), True),
                (Path(f"{home}/.config/gtkrc"), Path("./xdg-data/gtkrc"), False),
                (Path(f"{home}/.config/latte"), Path("./xdg-data/latte"), True),
                (Path(f"{home}/.config/[k]*"), Path("./xdg-config/[k]*"), True),
            ],
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
        super().__init__()
        self.__revert_copies()

        if DesktopEnvironment.get_current_de() == DesktopEnvironment.KDE_PLASMA:
            self.__kde_import_or_sync()  # I don't know if this should be here, in setup or run function

    def __revert_copies(self):
        """
        Reverts the changes made to the configuration files and restores them to
        their original location. This method applies the `reverse()` operation to each
        configuration file in the `config_files` collection.

        :return: None
        """
        self.config_files = self.config_files = [x.reverse() for x in self.config_files]

    @staticmethod
    def __change_grandparent_dir(paths: List[Path], grandparent: Path):
        """
        Modifies paths to replace their parent directory with a specified grandparent
        directory if their parent directory name matches specific values.

        :param paths: List containing Path objects to be modified.
        :param grandparent: The grandparent directory used for replacement.
        :return: A list of Path objects with updated parent directories where applicable.
        """
        return list(map(
            lambda p: grandparent / p.parent.name / p.name
            if p.parent.name in ['xdg-config', 'xdg-data']
            else p,
            paths
        ))

    @staticmethod
    def __is_xdg_path(path: Path) -> bool:
        """
        Determines if the given path is an XDG path based on the naming convention.

        This static method checks whether the provided path belongs to the XDG
        configuration or data directory by examining the name of the parent
        directory.

        :param path: The path to be checked.
        :type path: Path
        :return: Returns True if the path belongs to an XDG directory, otherwise False.
        :rtype: bool
        """
        return path.parent.name in ['xdg-config', 'xdg-data']

    @staticmethod
    def __create_xdg_path(grandparent: Path, path: Path) -> Path:
        """
        Generate a new XDG-compliant path.

        This method constructs a new path by combining the given `grandparent` path with the
        parent directory name and the name of the `path`. The resulting path follows the structure:
        `grandparent / parent_name_of_path / name_of_path`.

        :param grandparent: The top-level directory where the new path should be rooted.
        :type grandparent: Path
        :param path: The source path whose parent directory name and file name will be used
            to form the new path.
        :type path: Path
        :return: A new path combining `grandparent`, the parent directory name of `path`,
            and the name of `path`.
        :rtype: Path
        """
        return grandparent / path.parent.name / path.name

    def __kde_import_or_sync(self) -> None:
        """
        Processes and updates the list of configuration file paths by ensuring they comply
        with the XDG (X Desktop Group) specification. Determines the current directory
        to use based on whether syncing or import configuration paths exist before transforming
        configurable file paths accordingly.

        :param self: Instance of the class calling the function.
        """
        syncing_path = Path(f"{CACHE}/syncing")
        import_config_path = Path(f"{CACHE}/import_config")
        current_dir = syncing_path if syncing_path.exists() else import_config_path

        modify = partial(self.__create_xdg_path, current_dir)
        transform = lambda p: modify(p) if self.__is_xdg_path(p) else p
        self.config_files = list(map(transform, self.config_files))

    def create_flatpak_desktop(self):
        os.system(f"cp {system_dir}/install_flatpak_from_script.py {CACHE}/")
        if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh") or not os.path.exists(
                f"{CACHE}/syncing/sync_status"):
            if not os.path.exists(f"{home}/.config/autostart"):
                os.mkdir(f"{home}/.config/autostart")
            if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
                with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                    fa.write(
                        f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {CACHE}/install_flatpak_from_script.py")

    def setup(self):
        """
        Sets up the application configuration by importing settings from the Dconf
        database. Handles both backwards compatibility and Flatpak configurations.

        Behavior changes based on whether a "user" directory exists, and whether
        running under Flatpak is detected. Copies configuration directory for older
        versions or executes system commands to load Dconf settings dynamically.

        :param self: Instance of the class containing this method.

        :raises FileNotFoundError: If the required configuration file or directory
            is missing.
        """
        print("importing settings from the Dconf database")
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
        Executes the process to handle parallel copy and create the Flatpak desktop integration
        if applicable. This method is designed to check for specific files and handle Flatpak
        desktop creation when these files are detected.

        :return: None
        """
        self._parallel_copy(max_workers=max_workers)
        if flatpak:
            if any(os.path.exists(path) for path in ["app", "installed_flatpaks.sh", "installed_user_flatpaks.sh"]):
                self.create_flatpak_desktop()

    def teardown(self) -> None:
        pass


if args.save:
    Save().run()
elif args.import_:
    Import().run()
