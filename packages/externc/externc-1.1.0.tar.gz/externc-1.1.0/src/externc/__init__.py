import importlib as _importlib
from importlib import machinery as _machinery
import os as _os
import types as _types
import builtins as _builtins

from . import compilers as _compilers

__all__ = ["c"]
__version__ = "1.0.0"

_moddef = """
#define PY_SSIZE_T_CLEAN
#include<Python.h>
{incl}

{mod}

static PyMethodDef {name}_methods[] = {{
  {meth}
  {{NULL, NULL, 0, NULL}} //sentinel
}};

static struct PyModuleDef {name}_module = {{
  PyModuleDef_HEAD_INIT,
  .m_name = "{name}",
  .m_doc = PyDoc_STR("an ExternC generated module"),
  .m_size = -1,
  
  .m_methods = {name}_methods
}};

PyMODINIT_FUNC PyInit_{name}(void){{
  PyObject* mod = PyModule_Create(&{name}_module);
  {init}
  return mod;
}}
"""

_funcdef = """
{rtype} {name}({args}){{
  {code}
}}
"""

_methdef = """
{{
  .ml_name = {name},
  .ml_meth = {func},
  .ml_flags = {call},
  .ml_doc = PyDoc_STR({doc})
}},
"""

def _rep(i):
    st = '"'
    esc = "\\\n\'\""
    for i in i:
        if ord(i) < 32:
            st += f"\\{ord(i):o}"
        elif i in esc:
            st += "\\" + i
        else:
            st += i
    st += '"'
    return st

def _mk_mod(name, incl, mod, meth, init):
    incl = "\n".join([f"#include<{i}>" for i in incl])
    return _moddef.format(name=name, incl=incl, mod=mod,
            meth=meth, init=init)

def _mk_func(name, rtype, args, code):
    vari = False
    if len(args) and args[-1] == "...":
        vari = True
        args = args[:-1]
    sargs = [f"{i} {j}" for i, j in args]
    if vari:
        sargs.append("...")
    sargs = ", ".join(sargs)
    return _funcdef.format(rtype = rtype, name=name,
            args=sargs, code=code)

def _mk_meth(name, func, call, doc):
    return _methdef.format(name=_rep(name), func=func,
            call=call, doc=_rep(doc), )

_nmls: list[int] = [0]

def c(code: str, /, *, include: tuple[str] | tuple[()] = (), name: str | None =None, compiler: _compilers.Compiler=_compilers.get_cc(), funcname: str = "func") -> _types.BuiltinFunctionType:
    """
    This function is the core of this module.
    It recieves the body of a C function of the signature PyObject* (PyObject* self, PyObject* args, PyObject* kwargs) and returns the builtin_function_or_method that this code produces.
    It optionally recieves a few options for e.g. the name of the generated function and it's call signature.
    Consult the source code and the python documentation for more information.
    """
    if name != None and not name.isidentifier():
        raise ValueError(f"Name {name} not a valid identifier")
    if not funcname.isidentifier():
        raise ValueError(f"Function name {funcname} not a valid identifier")
    if name == None:
        name = f"externc_{_nmls[0]:x}"
        _nmls[0] += 1
    fn = _mk_func(funcname, "PyObject*",
            (("PyObject*", "self"), ("PyObject*", "args"), ("PyObject*", "kwargs")), code)
    meth = _mk_meth(funcname, funcname, "METH_VARARGS | METH_KEYWORDS",
            "an ExternC generated function")
    mod = _mk_mod(name, tuple(include), fn, meth, "")
    so = min(_machinery.EXTENSION_SUFFIXES)
    compiler.compile(mod, name + so)
    try:
        md = _importlib.import_module(name)
        md = _importlib.reload(md)
    finally:
        _os.remove(name + so)
    return getattr(md, funcname)

setattr(_builtins, "c", c)
