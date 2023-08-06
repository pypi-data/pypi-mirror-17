#include <Python.h>
#include <Windows.h>
#include "MemoryModule.h"

#if PY_MAJOR_VERSION >= 3
#define READONLY_BUFFER "y#"
#else
#define READONLY_BUFFER "t#"
#endif

static PyObject *c_void_p = NULL;

static PyObject* _MemoryLoadLibrary(PyObject* self, PyObject* args)
{
    void* data;
    size_t size;
    HMEMORYMODULE handle;

    if (!PyArg_ParseTuple(args, READONLY_BUFFER, &data, &size)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    handle = MemoryLoadLibrary(data, size);
    Py_END_ALLOW_THREADS

    if (!handle) {
        PyErr_SetFromWindowsErr(GetLastError());
        return NULL;
    }

    return PyCapsule_New(handle, "HMEMORYMODULE", NULL);
}

static PyObject* _MemoryGetProcAddress(PyObject* self, PyObject* args)
{
    PyObject* module;
    char* name;
    HMEMORYMODULE handle;
    FARPROC address;

    if (!PyArg_ParseTuple(args, "Os", &module, &name)) {
        return NULL;
    }

    handle = PyCapsule_GetPointer(module, "HMEMORYMODULE");
    if (!handle) {
        PyErr_SetString(
            PyExc_TypeError,
            "module must be PyCapsule (HMEMORYMODULE)"
        );
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    address = MemoryGetProcAddress(handle, name);
    Py_END_ALLOW_THREADS

    if (!address) {
        PyErr_SetFromWindowsErr(GetLastError());
        return NULL;
    }

    return PyObject_CallFunction(
        c_void_p,
        "O",
        PyLong_FromVoidPtr(address)
    );
}

static PyObject* _MemoryFreeLibrary(PyObject* self, PyObject* args)
{
    PyObject* module;
    HMEMORYMODULE handle;

    if (!PyArg_ParseTuple(args, "O", &module)) {
        return NULL;
    }

    handle = PyCapsule_GetPointer(module, "HMEMORYMODULE");
    if (!handle) {
        PyErr_SetString(
            PyExc_TypeError,
            "module must be PyCapsule (HMEMORYMODULE)"
        );
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    MemoryFreeLibrary(handle);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}


/**
 * https://github.com/fancycode/MemoryModule/blob/master/MemoryModule.h
 * https://github.com/fancycode/MemoryModule/blob/master/MemoryModule.c
 */
static char _MemoryLoadLibrary_docs[] =
    "MemoryLoadLibrary(data):\n"
    "- data: EXE/DLL as read-only buffer (e.g. str in 2.x and bytes in 3.x)\n"
    "- return: Handle of EXE/DLL as HMEMORYMODULE\n"
    "\n"
    "Load EXE/DLL from memory location with the given size.\n"
    "\n"
    "All dependencies are resolved using default LoadLibrary/GetProcAddress\n"
    "calls through the Windows API.";

static char _MemoryGetProcAddress_docs[] =
    "MemoryGetProcAddress(module, name):\n"
    "- module: Handle of EXE/DLL as HMEMORYMODULE\n"
    "- name: Name of exported method as string\n"
    "- return: Address of exported method as ctypes.c_void_p\n"
    "\n"
    "Get address of exported method. Supports loading both by name and by\n"
    "ordinal value.";

static char _MemoryFreeLibrary_docs[] =
    "MemoryFreeLibrary(module):\n"
    "- module: Handle of EXE/DLL as HMEMORYMODULE\n"
    "\n"
    "Free previously loaded EXE/DLL.";

/**
 * https://github.com/fancycode/MemoryModule/tree/master/doc#memorymodule
 */
static PyMethodDef methods[] = {
    {"MemoryLoadLibrary", (PyCFunction)_MemoryLoadLibrary,
        METH_VARARGS, _MemoryLoadLibrary_docs},
    {"MemoryGetProcAddress", (PyCFunction)_MemoryGetProcAddress,
        METH_VARARGS, _MemoryGetProcAddress_docs},
    {"MemoryFreeLibrary", (PyCFunction)_MemoryFreeLibrary,
        METH_VARARGS, _MemoryFreeLibrary_docs},
    {NULL, NULL, 0, NULL}   /* sentinel */
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "pymemorymodule",
    NULL,
    -1,
    methods,
};
#define INIT_FUNC PyInit_pymemorymodule
#else
#define INIT_FUNC initpymemorymodule
#endif

PyMODINIT_FUNC INIT_FUNC(void)
{
    PyObject *ctypes = PyImport_ImportModule("ctypes");
    c_void_p = PyObject_GetAttrString(ctypes, "c_void_p");

#if PY_MAJOR_VERSION >= 3
    return PyModule_Create(&module);
#else
    Py_InitModule("pymemorymodule", methods);
#endif
}
