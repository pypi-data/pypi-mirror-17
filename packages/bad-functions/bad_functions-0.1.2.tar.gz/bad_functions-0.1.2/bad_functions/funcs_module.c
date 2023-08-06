#include <Python.h>
#include "funcs.h"

static PyObject* bad_functions_inf_loop(PyObject *self, PyObject *args)
{
    inf_loop();
    Py_RETURN_NONE;
}

static PyObject* bad_functions_segfault(PyObject *self, PyObject *args)
{
    segfault();
    Py_RETURN_NONE;
}

static PyMethodDef BadFunctionMethods[] = {
    {"inf_loop", bad_functions_inf_loop, METH_VARARGS, "Enter an infinite loop"},
    {"segfault", bad_functions_segfault, METH_VARARGS, "Deliberately cause segfault"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initbad_functions(void)
{
    (void) Py_InitModule("bad_functions", BadFunctionMethods);
}
