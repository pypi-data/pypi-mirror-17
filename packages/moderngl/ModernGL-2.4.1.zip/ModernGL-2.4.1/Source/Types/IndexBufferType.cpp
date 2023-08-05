#include "IndexBufferType.hpp"

#include "Errors.hpp"

PyObject * IndexBuffer_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int IndexBuffer_init(IndexBuffer * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate IndexBuffer.\nCall NewIndexBuffer(...) to get a IndexBuffer object.");
	return -1;
}

void IndexBuffer_dealloc(IndexBuffer * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * IndexBuffer_str(IndexBuffer * self) {
	return PyUnicode_FromFormat("<IndexBuffer = %d>", self->ibo);
}

PyTypeObject IndexBufferType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.IndexBuffer",
	sizeof(IndexBuffer),
	0,
	(destructor)IndexBuffer_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)IndexBuffer_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)IndexBuffer_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"IndexBuffer",
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
	(initproc)IndexBuffer_init,
	0,
	IndexBuffer_new,
};

PyObject * CreateIndexBufferType(int ibo, int size) {
	IndexBuffer * obj = (IndexBuffer *)IndexBufferType.tp_alloc(&IndexBufferType, 0);

	if (obj != 0) {
		obj->ibo = ibo;
		obj->size = size;
	}

	return (PyObject *)obj;
}
