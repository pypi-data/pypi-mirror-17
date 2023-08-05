#include "VertexBufferType.hpp"

#include "Errors.hpp"

PyObject * VertexBuffer_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int VertexBuffer_init(VertexBuffer * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate VertexBuffer.\nCall NewVertexBuffer(...) to get a VertexBuffer object.");
	return -1;
}

void VertexBuffer_dealloc(VertexBuffer * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * VertexBuffer_str(VertexBuffer * self) {
	return PyUnicode_FromFormat("<VertexBuffer = %d>", self->vbo);
}

PyTypeObject VertexBufferType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.VertexBuffer",
	sizeof(VertexBuffer),
	0,
	(destructor)VertexBuffer_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)VertexBuffer_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)VertexBuffer_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"VertexBuffer",
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	(initproc)VertexBuffer_init,
	0,
	VertexBuffer_new,
};

PyObject * CreateVertexBufferType(int vbo, int size) {
	VertexBuffer * obj = (VertexBuffer *)VertexBufferType.tp_alloc(&VertexBufferType, 0);

	if (obj != 0) {
		obj->vbo = vbo;
		obj->size = size;
	}

	return (PyObject *)obj;
}
