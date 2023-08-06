#include <Python.h>
#include "structmember.h"
#include <Judy.h>
#include <stdlib.h>

#define HASH_SIZE 33
// Type definition
typedef struct {
	PyObject_HEAD
	Pvoid_t JMap;
} HexMap;

typedef struct {
	PyObject_HEAD
	int q;
	int r;
	int s;
} Hex;

static void Hex_dealloc(Hex* self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *Hex_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Hex *self;

    self = (Hex *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->q = 0;
        self->r = 0;
        self->s = 0;
    }

    return (PyObject *)self;
}

static int Hex_init(Hex *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"q", "r", "s", NULL};

	if (! PyArg_ParseTupleAndKeywords(args, kwds, "|iii", kwlist, &self->q, &self->r, &self->s))
    	return -1;

	return 0;
}


static PyMemberDef Hex_members[] = {
    {"q", T_INT, offsetof(Hex, q), 0,
     "q"},
    {"r", T_INT, offsetof(Hex, r), 0,
     "r"},
    {"s", T_INT, offsetof(Hex, s), 0,
     "s"},
    {NULL}  /* Sentinel */
};

static PyObject *Hex_repr(Hex *obj)
{
    return PyUnicode_FromFormat("Hex q: \%i r: \%i s: \%i",
                                obj->q, obj->r, obj->s);
}

// Object description
static PyTypeObject HexType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "point.Hex",             /* tp_name */
    sizeof(Hex), /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Hex_dealloc,   /* tp_dealloc */
	0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    Hex_repr,                  /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "Hex cube coordinates",    /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,				           /* tp_methods  Hex_methods goes here */
    Hex_members,               /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Hex_init,        /* tp_init */
    0,                         /* tp_alloc */
    Hex_new,                   /* tp_new */
};

static void HexMap_dealloc(HexMap* self)
{
	Word_t Bytes;
	JSLFA(Bytes, self->JMap)
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *HexMap_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    HexMap *self;

    self = (HexMap*)type->tp_alloc(type, 0);
    if (self != NULL) {
		self->JMap = (PWord_t)NULL;
    }

    return (PyObject *)self;
}

static int HexMap_init(HexMap *self, PyObject *args, PyObject *kwds)
{
	return 0;
}

unsigned char *hashHexCoord(int q, int r, int s)
{
	unsigned char *ret;
	char buf[HASH_SIZE];
	size_t size = HASH_SIZE;

	ret = (unsigned char*)malloc(sizeof(unsigned char) * HASH_SIZE);
	snprintf(buf, size, "%d%d%d", q, r, s);
	memcpy(ret, buf, strlen(buf) + 1);
	return (ret);
}

static PyObject *HexMap_set(HexMap *self, PyObject *args)
{
	PyObject 		*HexCoord;
	unsigned int	value;
	PWord_t 		ptr;
	unsigned char	*hash;

	HexCoord = malloc(sizeof(PyObject*));
	if (! PyArg_ParseTuple(args, "O!I", &HexType, &HexCoord, &value))
        return -1;

	hash = hashHexCoord(((Hex*)HexCoord)->q, ((Hex*)HexCoord)->r, ((Hex*)HexCoord)->s);
	JSLI(ptr, self->JMap, hash);
	free(hash);
	*ptr = (Word_t)value;

	Py_RETURN_NONE;
}

static PyObject *HexMap_get(HexMap *self, PyObject *args)
{
	PyObject		*HexCoord;
	PWord_t			Value;
	unsigned char	*hash;

	HexCoord = malloc(sizeof(PyObject*));
	Value = malloc(sizeof(PWord_t));
	if (! PyArg_ParseTuple(args, "O!", &HexType, &HexCoord))
		return -1;

	hash = hashHexCoord(((Hex*)HexCoord)->q, ((Hex*)HexCoord)->r, ((Hex*)HexCoord)->s);
	JSLG(Value, self->JMap, hash);
	free(hash);
	if (!Value)
		Py_RETURN_NONE;
	return Py_BuildValue("I", *(unsigned int*)Value);
}

static PyMethodDef HexMap_methods[] = {
    {"set", (PyCFunction)HexMap_set, METH_VARARGS,
    "set a position on the hex grid to a value"
    },
	{"get", (PyCFunction)HexMap_get, METH_VARARGS,
	"get the value at position on the hex grid return None if position does not exist"
	},
    {NULL}  /* Sentinel */
};
// Object description
static PyTypeObject HexMapType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "map.HexMap",              /* tp_name */
    sizeof(HexMap),            /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)HexMap_dealloc,   /* tp_dealloc */
	0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "A hexagonal map object",  /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    HexMap_methods,            /* tp_methods  Hex_methods goes here */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)HexMap_init,        /* tp_init */
    0,                         /* tp_alloc */
    HexMap_new,                   /* tp_new */
};

static PyModuleDef hexmapmodule = {
    PyModuleDef_HEAD_INIT,
    "hexmap",
    "A module for string and manipulating hexagonal grids.",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_map(void)
{
    PyObject* m;

    if (PyType_Ready(&HexMapType) < 0)
        return NULL;

    if (PyType_Ready(&HexType) < 0)
        return NULL;

    m = PyModule_Create(&hexmapmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&HexMapType);
    PyModule_AddObject(m, "HexMap", (PyObject *)&HexMapType);
	Py_INCREF(&HexType);
    PyModule_AddObject(m, "Hex", (PyObject *)&HexType);

    return m;
}
