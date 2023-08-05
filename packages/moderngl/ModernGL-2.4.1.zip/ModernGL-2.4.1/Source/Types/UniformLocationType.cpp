#include "UniformLocationType.hpp"

#include "Errors.hpp"

PyObject * UniformLocation_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int UniformLocation_init(UniformLocation * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate UniformLocation.\nCall GetUniformLocation(...) to get a UniformLocation object.");
	return -1;
}

void UniformLocation_dealloc(UniformLocation * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * UniformLocation_str(UniformLocation * self) {
	return PyUnicode_FromFormat("<UniformLocation = %d>", self->location);
}

PyTypeObject UniformLocationType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.UniformLocation",
	sizeof(UniformLocation),
	0,
	(destructor)UniformLocation_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)UniformLocation_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)UniformLocation_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"UniformLocation",
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
	(initproc)UniformLocation_init,
	0,
	UniformLocation_new,
};

PyObject * CreateUniformLocationType(int location, int program, int type) {
	UniformLocation * obj = (UniformLocation *)UniformLocationType.tp_alloc(&UniformLocationType, 0);

	if (obj != 0) {
		obj->location = location;
		obj->program = program;
		obj->type = type;
	}

	return (PyObject *)obj;
}
