#define Py_LIMITED_API
#include <Python.h>
#include "structmember.h"

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

typedef struct {
      PyObject_HEAD
      /* Type-specific fields go here. */
      PyObject *remotes; /* which remotes you're connected to */
      PyObject *error_callable; /* call with any async errors */
} go_vncdriver_VNCSession_object;

static PyObject *go_vncdriver_Error;

/* Go functions exposed directly to Python */
PyObject * GoVNCDriver_VNCSession_peek(PyObject *, PyObject *);
PyObject * GoVNCDriver_VNCSession_flip(PyObject *, PyObject *);
PyObject * GoVNCDriver_VNCSession_step(PyObject *, PyObject *);
PyObject * GoVNCDriver_VNCSession_close(PyObject *, PyObject *);
PyObject * GoVNCDriver_VNCSession_render(PyObject *, PyObject *);

/* Go functions which are called only from C */
int GoVNCDriver_VNCSession_c_init(go_vncdriver_VNCSession_object *, PyObject *);
void GoVNCDriver_VNCSession_c_close(go_vncdriver_VNCSession_object *);

/* Global functions */
PyObject * GoVNCDriver_setup(PyObject *, PyObject *);

/* end go functions */

void PyErr_SetGoVNCDriverError(char* msg) {
    PyErr_SetString(go_vncdriver_Error, msg);
    free(msg);
}

PyObject *GoPyArray_SimpleNew(int nd, npy_intp* dims, int typenum) {
    return PyArray_SimpleNew(nd, dims, typenum);
}

PyObject *GoPyArray_SimpleNewFromData(int nd, npy_intp* dims, int typenum, void *data) {
  return PyArray_SimpleNewFromData(nd, dims, typenum, data);
}

/* VNCSession object */

static void
go_vncdriver_VNCSession_dealloc(go_vncdriver_VNCSession_object* self)
{
    Py_XDECREF(self->remotes);
    Py_XDECREF(self->error_callable);
    GoVNCDriver_VNCSession_c_close(self);
    self->ob_type->tp_free((PyObject*)self);
}

static int
go_vncdriver_VNCSession_init(go_vncdriver_VNCSession_object *self, PyObject *args, PyObject *kwds)
{
    PyObject *remotes, *error_callable;
    static char *kwlist[] = {"remotes", "error_callable", NULL};

    error_callable = &_Py_NoneStruct;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", kwlist, &remotes, &error_callable))
        return -1;

    Py_INCREF(remotes);
    self->remotes = remotes;

    Py_INCREF(error_callable);
    self->error_callable = error_callable;

    // Prepare a new args list
    if ((args = Py_BuildValue("(OO)", remotes, error_callable)) == NULL) {
        return -1;
    }

    int res = GoVNCDriver_VNCSession_c_init(self, args);
    Py_DECREF(args);
    if (res == -1) {
        return -1;
    }

    return 0;
}

static PyMemberDef go_vncdriver_VNCSession_members[] = {
    {"remotes", T_OBJECT_EX, offsetof(go_vncdriver_VNCSession_object, remotes), 0,  "VNC remotes"},
    {"error_callable", T_OBJECT_EX, offsetof(go_vncdriver_VNCSession_object, error_callable), 0,  "Gets called with any asynchronous errors"},
    {NULL}  /* Sentinel */
};

static PyMethodDef go_vncdriver_VNCSession_methods[] = {
  {"close", (PyCFunction)GoVNCDriver_VNCSession_close, METH_NOARGS, "Closes the connection"},
  {"flip", (PyCFunction)GoVNCDriver_VNCSession_flip, METH_NOARGS, "Flips to the most recently updates screen"},
  {"peek", (PyCFunction)GoVNCDriver_VNCSession_peek, METH_NOARGS, "Peek at the last returned screen"},
  {"render", (PyCFunction)GoVNCDriver_VNCSession_render, METH_NOARGS, "Render the screen"},
  {"step", (PyCFunction)GoVNCDriver_VNCSession_step, METH_O, "Perform actions and then flip"},
  {NULL}  /* Sentinel */
};

// https://docs.python.org/2.7/extending/newtypes.html
PyTypeObject go_vncdriver_VNCSession_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "go_vncdriver.VNCSession",             /*tp_name*/
    sizeof(go_vncdriver_VNCSession_object), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)go_vncdriver_VNCSession_dealloc,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        /*tp_flags*/
    "VNCSession objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    go_vncdriver_VNCSession_methods,             /* tp_methods */
    go_vncdriver_VNCSession_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)go_vncdriver_VNCSession_init,      /* tp_init */
    0,                         /* tp_alloc */
    0,                 /* tp_new */
};

// Needed because CGo can't access static variables
PyObject *get_go_vncdriver_VNCSession_type() {
  return (PyObject *) &go_vncdriver_VNCSession_type;
}

static PyMethodDef go_vncdriver_module_methods[] = {  
    {"setup", GoVNCDriver_setup, METH_NOARGS, "Configure logging."},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION == 3
// TODO: currently broken
static struct PyModuleDef go_vncdriver_module = {  
};

PyMODINIT_FUNC  
PyInit_go_vncdriver(void)  
{
    return PyModule_Create(&go_vncdriver_module);
}
#else
PyMODINIT_FUNC
initgo_vncdriver(void)
{
    PyObject *m;

    go_vncdriver_VNCSession_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&go_vncdriver_VNCSession_type) < 0)
        return;

    m = Py_InitModule("go_vncdriver", go_vncdriver_module_methods);
    if (m == NULL)
        return;

    go_vncdriver_Error = PyErr_NewException("go_vncdriver.Error", NULL, NULL);
    Py_INCREF(go_vncdriver_Error);
    PyModule_AddObject(m, "Error", go_vncdriver_Error);

    Py_INCREF(&go_vncdriver_VNCSession_type);
    PyModule_AddObject(m, "VNCSession", (PyObject *) &go_vncdriver_VNCSession_type);

    import_array();
}
#endif
