#include <Python.h>
#include "structmember.h"
#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

#define get_bit(array, index)   ((array[index / sizeof(array)] & (1 << (index % sizeof(array)))) != 0)
#define set_bit(array, index)   (array[index / sizeof(array)] |= (1 << (index % sizeof(array))))
#define clear_bit(array, index) ((array[index / sizeof(array)] &= ~(1 << (index % sizeof(array)))))

typedef struct {
    PyObject_HEAD
    long length;
    long width;
    long height;
    long* graph;
    long num_edges;
} Graph;

static int Graph_init(Graph* self, PyObject* args)
{
    long i;
    PyObject* py_graph;

    if (! PyArg_ParseTuple(args, "iO", &(self->width), &py_graph))
        return -1;

    if (self->width <= 0)
    {
        PyErr_SetString(PyExc_ValueError, "Width must be positive.");
        return -1;
    }

    self->length = (long) PyList_Size(py_graph);

    self->graph = malloc(self->length * sizeof(*(self->graph)));
    if (self->graph == NULL)
    {
        PyErr_SetNone(PyExc_MemoryError);
        return -1;
    }
    self->height = self->length / self->width;

    self->num_edges = 0;
    for (i = 0; i < self->length; i++)
    {
        self->graph[i] = PyLong_AsLong(PyList_GetItem(py_graph, i));
        if (self->graph[i] > -1)
            self->num_edges++;
    }
    self->num_edges = self->num_edges / 2;

    return 0;
}

static void Graph_dealloc(Graph* self)
{
    free(self->graph);
}


static PyObject* Graph_reduce(Graph* self)
{
    long i;
    PyObject* py_graph = NULL;

    py_graph = PyList_New(self->length);
    for (i = 0; i < self->length; i++)
        PyList_SetItem(py_graph, i, PyLong_FromLong(self->graph[i]));
    return Py_BuildValue("(O(lO))", PyObject_Type((PyObject*) self), self->width, py_graph);
}


static long DFT(Graph* self, long start, long* vertices, long** breaks, long max_radius)
{
    long i;
    char* seen = NULL;
    long head = 0, tail = 1;
    long next_eccentricity_increase = tail;
    long current, next;
    long* current_breaks;
    long* new_breaks;

    long eccentricity = 0;

    seen = calloc(self->height, sizeof(*seen));
    current_breaks = malloc(1 * sizeof(*breaks));
    if (!seen || !current_breaks)
    {
        free(seen);
        free(current_breaks);
        return -1;
    }

    vertices[0] = start;
    seen[start] = 1;  // calloc has done the necessary zeroing for us.
    current_breaks[0] = tail;

    for (head = 0; head < self->height; head++)
    {
        if (head == next_eccentricity_increase)
        {
            eccentricity++; // /*
            new_breaks = realloc(current_breaks, (eccentricity+1) * sizeof(*breaks));
            if (!new_breaks)
            {
                free(seen);
                free(current_breaks);
                return -1;
            }
            current_breaks = new_breaks;
            current_breaks[eccentricity] = tail; //  */
            next_eccentricity_increase = tail;
            if (eccentricity == max_radius)
                break;
        }
        current = vertices[head];
        for (i = 0; i < self->width; i++)
        {
            next = self->graph[self->width * current + i];
            if (next > -1 && seen[next] == 0)
            {
                seen[next] = 1;
                vertices[tail] = next;
                tail++;
            }
        }
    }

    free(seen);

    *breaks = current_breaks;

    return eccentricity;
}

static PyObject* Graph_eccentricity(Graph* self, PyObject* args)
{
    long start = 0;
    long* vertices = NULL;
    long eccentricity = 0;
    long* breaks;

    if (! PyArg_ParseTuple(args, "l", &start))
        return NULL;

    vertices = malloc(self->height * sizeof(*vertices));
    if (!vertices)
        return PyErr_NoMemory();

    eccentricity = DFT(self, start, vertices, &breaks, -1);
    if (eccentricity < 0)
    {
        free(vertices);
        free(breaks);
        return PyErr_NoMemory();
    }

    free(vertices);
    free(breaks);

    return Py_BuildValue("l", eccentricity);
}

static PyObject* Graph_ball(Graph* self, PyObject* args)
{
    long i;
    long start = 0, radius = 0;
    long* vertices = NULL;
    long eccentricity = 0;
    long* breaks;
    PyObject* ball = NULL;

    if (! PyArg_ParseTuple(args, "ll", &start, &radius))
        return NULL;

    if (radius < 0)
        return PyList_New(0);

    vertices = malloc(self->height * sizeof(*vertices));
    if (!vertices)
        return PyErr_NoMemory();

    eccentricity = DFT(self, start, vertices, &breaks, radius);
    if (eccentricity < 0)
    {
        free(vertices);
        return PyErr_NoMemory();
    }

    if (eccentricity < radius)
        radius = eccentricity;

    // Package up the ball.
    ball = PyList_New(breaks[radius]);
    for (i = 0; i < breaks[radius]; i++)
        PyList_SetItem(ball, i, PyLong_FromLong(vertices[i]));

    free(vertices);
    free(breaks);

    return ball;
}

static PyObject* Graph_diameter(Graph* self, PyObject* args)
{
    long i, j;
    long* vertices = NULL;
    char* seen = NULL;
    long eccentricity = 0;
    long max_eccentricity = 0;
    long* breaks;
    long current;

    long mini = 0;
    long maxi = self->height;
    long blocksize;

    if (! PyArg_ParseTuple(args, "|ll", &mini, &maxi))
        return NULL;

    blocksize = maxi - mini;

    vertices = malloc(self->height * sizeof(*vertices));
    seen = calloc(blocksize, sizeof(*seen));
    if (!seen || !vertices)
    {
        free(vertices);
        free(seen);
        return PyErr_NoMemory();
    }

    for (i = 0; i < blocksize; i++)
        if (!seen[i])
        {
            eccentricity = DFT(self, mini + i, vertices, &breaks, -1);
            if (eccentricity < 0)
            {
                free(vertices);
                free(seen);
                return PyErr_NoMemory();
            }
            if (eccentricity >= max_eccentricity)
                max_eccentricity = eccentricity;
            else
                for (j = 0; j < breaks[max_eccentricity - eccentricity]; j++)
                {
                    current = vertices[j];
                    if (current >= mini)
                        seen[current - mini] = 1;
                }
        }

    free(seen);
    free(breaks);

    return Py_BuildValue("l", max_eccentricity);
}

static Py_ssize_t Graph_len(PyObject* self)
{
    return (Py_ssize_t) ((Graph*) self)->height;
}

/* --------------------------------- */

static PySequenceMethods Graph_sequence_methods = {
    &Graph_len,                  /* sq_length */
};

static PyMemberDef Graph_members[] = {
    {"width", T_INT, offsetof(Graph, width), 1, "table width"},
    {"num_edges", T_INT, offsetof(Graph, num_edges), 1, "number of edges"},
    {NULL}  /* Sentinel */
};

static PyMethodDef Graph_methods[] = {
    {"eccentricity", (PyCFunction)Graph_eccentricity, METH_VARARGS, "Return the eccentricity of the given vertex."},
    {"ball", (PyCFunction)Graph_ball, METH_VARARGS, "Return the *closed* ball about the given vertex."},
    {"diameter", (PyCFunction)Graph_diameter, METH_VARARGS, "Return the diameter of self."},
    {"__reduce__", (PyCFunction)Graph_reduce, METH_NOARGS, ""},
    //{"__getstate__", (PyCFunction)Graph_getstate, METH_NOARGS, ""},
    //{"__setstate__", (PyCFunction)Graph_setstate, METH_VARARGS, ""},
    {NULL}  /* Sentinel */
};

/* --------------------------------- */

static PyTypeObject cGraph_GraphType = {
#if PY_MAJOR_VERSION < 3
    PyObject_HEAD_INIT(NULL) 0,/* ob_size */
#else
    PyVarObject_HEAD_INIT(NULL, 0)
#endif
    "cGraph.Graph",             /*tp_name*/
    sizeof(Graph),              /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor) Graph_dealloc, /*tp_dealloc*/
    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
    0,                          /*tp_setattr*/
    0,                          /*tp_compare*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    &Graph_sequence_methods,    /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash */
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    0,                          /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "Graph objects",            /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    Graph_methods,              /* tp_methods */
    Graph_members,              /* tp_members */
    0,                          /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    (initproc) Graph_init,      /* tp_init */
    0,                          /* tp_alloc */
    PyType_GenericNew,          /* tp_new */
};

#if PY_MAJOR_VERSION < 3
static PyMethodDef cGraph_methods[] = {
    {NULL}  /* Sentinel */
};

PyMODINIT_FUNC initcGraph(void)
{
    PyObject* m;

    if (PyType_Ready(&cGraph_GraphType) < 0)
        return;

    m = Py_InitModule3("cGraph", cGraph_methods, "Example module that creates an extension type.");

    Py_INCREF(&cGraph_GraphType);
    PyModule_AddObject(m, "Graph", (PyObject*) &cGraph_GraphType);
}
#else
static PyModuleDef cGraphmodule = {
    PyModuleDef_HEAD_INIT,
    "cGraph",
    "Example module that creates an extension type.",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_cGraph(void)
{
    PyObject* m;

    cGraph_GraphType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&cGraph_GraphType) < 0)
        return NULL;

    m = PyModule_Create(&cGraphmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&cGraph_GraphType);
    PyModule_AddObject(m, "Graph", (PyObject*) &cGraph_GraphType);
    return m;
}
#endif

