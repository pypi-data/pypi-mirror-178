import shutil as _shutil
import sysconfig as _sysconfig
import subprocess as _subprocess
import os as _os
__all__ = ["Compiler", "Clang"]

class CompilerError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
    def __str__(self) -> str:
        return self.name

class Compiler:
    """
    A compiler interface, not to be instanced directly!
    """
    name = "example-compiler"
    def __init__(self):
        """
        A constructor to be overridden.
        It must allow creation with default settings if called without arguments.
        """
    def compile(self, contents: str, out: str) -> None:
        """
        This method must compile the C code passed to the file
        with a specified name.
        It may throw a CompilerError or a ValueError.
        """
        contents = contents
        out = out
        raise ValueError("The default compiler should never be used")

class Clang(Compiler):
    """
    The default compiler, clang
    """
    def __init__(self, *, include: list[str] = [],
                 link: list[str] = [], features: list[str] = [],
                 opt: str = "3", path: str | None = None) -> None:
        self.include = include
        self.link = link
        self.features = features
        self.opt = opt
        self.path = path
    def compile(self, contents, out):
        if self.path is None:
            self.path = _shutil.which("clang")
        if self.path is None:
            raise FileNotFoundError("No clang executable found")
        args = [
            self.path,
            *(f"-I{i}" for i in self.include),
            *(f"-l{i}" for i in self.link),
            *(f"-f{i}" for i in self.features),
            f"-O{self.opt}",
            f"-I{_sysconfig.get_path('include')}",
            "-w", "-std=c17",
            "-o", out, "-fPIE", "-shared", "-x", "c", "-"
        ]
        pop = _subprocess.Popen(args,
            stdin = _subprocess.PIPE, stdout=_subprocess.DEVNULL,
            stderr = _subprocess.PIPE)
        _, stderr = pop.communicate(contents.encode("utf8"))
        stderr = stderr.decode("utf8")
        pop.poll()
        if pop.returncode != 0:
            raise CompilerError(stderr)

def get_cc() -> Compiler:
    cc = _os.getenv("CC")
    if cc is not None:
        if cc == "clang":
            return Clang()
        if cc.endswith("clang") or cc.endswith("cc") or cc.endswith("clang.exe"):
            return Clang(path = cc)
    if (c := _shutil.which("clang")) is not None:
        return Clang(path = c)
    raise SystemError("No C compiler found, please specify one manually or write an interface yourself.")
