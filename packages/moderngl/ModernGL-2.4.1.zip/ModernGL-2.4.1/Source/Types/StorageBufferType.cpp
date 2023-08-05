#include "StorageBufferType.hpp"

#include "Errors.hpp"

PyObject * StorageBuffer_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int StorageBuffer_init(StorageBuffer * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate StorageBuffer.\nCall NewStorageBuffer(...) to get a StorageBuffer object.");
	return -1;
}

void StorageBuffer_dealloc(StorageBuffer * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * StorageBuffer_str(StorageBuffer * self) {
	return PyUnicode_FromFormat("<StorageBuffer = %d>", self->sbo);
}

PyTypeObject StorageBufferType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.StorageBuffer",
	sizeof(StorageBuffer),
	0,
	(destructor)StorageBuffer_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)StorageBuffer_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)StorageBuffer_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"StorageBuffer",
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
	(initproc)StorageBuffer_init,
	0,
	StorageBuffer_new,
};

PyObject * CreateStorageBufferType(int sbo, int size) {
	StorageBuffer * obj = (StorageBuffer *)StorageBufferType.tp_alloc(&StorageBufferType, 0);

	if (obj != 0) {
		obj->sbo = sbo;
		obj->size = size;
	}

	return (PyObject *)obj;
}

