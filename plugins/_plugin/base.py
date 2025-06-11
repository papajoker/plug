from pathlib import Path
import importlib.util
import sys


class PluginBase:
    NAME = ""

    @classmethod
    def getAction(cls):
        pass

    @classmethod
    def getTitle(cls) -> str:
        return cls.NAME

    @staticmethod
    def isEnable() -> bool:
        return True

    def app(self) -> type:
        return None


class Loader_module:
    def __init__(self, name, filename):
        self.filename = filename
        self.name = name
        self.mod = None

    def __enter__(self):
        try:
            spec = importlib.util.spec_from_file_location("dynamic.module_" + self.name, location=self.filename)
            self.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.mod)
        except FileNotFoundError as err:
            print(err, file=sys.stderr)
        return self.mod

    def __exit__(self, exc_type, exc_val, exc_tb):
        # del self.mod  # wait garbage collector (:
        return False


class PluginManager:
    def __init__(self):
        self.modules = {}
        self.path = Path(__file__).parent.parent
        print("défault dir for modules:", self.path)

    def walk(self, path=""):
        if path:
            self.path = Path(path)
        for directory in (d for d in self.path.iterdir() if d.is_dir() and not d.name.startswith("_")):
            name = directory.name
            file_ = directory / "plugin.py"
            if not file_.exists():
                continue
            print("    found sub-dir:", directory.name, directory)
            mod = self.load_module(name, file_)
            if mod:
                self.modules[name] = mod.Plugin()  # save the main class
        return self.modules

    @staticmethod
    def load_module(name, path):
        with Loader_module(name, path) as exo:
            print(exo)
            print(exo.__doc__ if exo.__doc__ else "")
            return exo
