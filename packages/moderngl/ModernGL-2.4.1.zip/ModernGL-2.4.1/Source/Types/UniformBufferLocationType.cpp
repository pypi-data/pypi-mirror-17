#include "UniformBufferLocationType.hpp"

#include "Errors.hpp"

PyObject * UniformBufferLocation_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int UniformBufferLocation_init(UniformBufferLocation * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate UniformBufferLocation.\nCall GetUniformBufferLocation(...) to get a UniformBufferLocation object.");
	return -1;
}

void UniformBufferLocation_dealloc(UniformBufferLocation * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * UniformBufferLocation_str(UniformBufferLocation * self) {
	return PyUnicode_FromFormat("<UniformBufferLocation = %d>", self->location);
}

PyTypeObject UniformBufferLocationType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.UniformBufferLocation",
	sizeof(UniformBufferLocation),
	0,
	(destructor)UniformBufferLocation_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)UniformBufferLocation_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)UniformBufferLocation_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"UniformBufferLocation",
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
	(initproc)UniformBufferLocation_init,
	0,
	UniformBufferLocation_new,
};

PyObject * CreateUniformBufferLocationType(int location, int program, int size) {
	UniformBufferLocation * obj = (UniformBufferLocation *)UniformBufferLocationType.tp_alloc(&UniformBufferLocationType, 0);

	if (obj != 0) {
		obj->location = location;
		obj->program = program;
		obj->size = size;
	}

	return (PyObject *)obj;
}
