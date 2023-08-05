#include "UniformBufferType.hpp"

#include "Errors.hpp"

PyObject * UniformBuffer_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int UniformBuffer_init(UniformBuffer * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate UniformBuffer.\nCall NewUniformBuffer(...) to get a UniformBuffer object.");
	return -1;
}

void UniformBuffer_dealloc(UniformBuffer * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * UniformBuffer_str(UniformBuffer * self) {
	return PyUnicode_FromFormat("<UniformBuffer = %d>", self->ubo);
}

PyTypeObject UniformBufferType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.UniformBuffer",
	sizeof(UniformBuffer),
	0,
	(destructor)UniformBuffer_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)UniformBuffer_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)UniformBuffer_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"UniformBuffer",
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
	(initproc)UniformBuffer_init,
	0,
	UniformBuffer_new,
};

PyObject * CreateUniformBufferType(int ubo, int size) {
	UniformBuffer * obj = (UniformBuffer *)UniformBufferType.tp_alloc(&UniformBufferType, 0);

	if (obj != 0) {
		obj->ubo = ubo;
		obj->size = size;
	}

	return (PyObject *)obj;
}
