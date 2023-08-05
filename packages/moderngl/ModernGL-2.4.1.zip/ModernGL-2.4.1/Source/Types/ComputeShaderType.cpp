#include "ComputeShaderType.hpp"

#include "Errors.hpp"

PyObject * ComputeShader_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int ComputeShader_init(ComputeShader * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate ComputeShader.\nCall NewComputeShader(...) to get a ComputeShader object.");
	return -1;
}

void ComputeShader_dealloc(ComputeShader * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * ComputeShader_str(ComputeShader * self) {
	return PyUnicode_FromFormat("<ComputeShader = %d>", self->program);
}

PyTypeObject ComputeShaderType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.ComputeShader",
	sizeof(ComputeShader),
	0,
	(destructor)ComputeShader_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)ComputeShader_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)ComputeShader_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"ComputeShader",
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
	(initproc)ComputeShader_init,
	0,
	ComputeShader_new,
};

PyObject * CreateComputeShaderType(int shader, int program) {
	ComputeShader * obj = (ComputeShader *)ComputeShaderType.tp_alloc(&ComputeShaderType, 0);

	if (obj != 0) {
		obj->shader = shader;
		obj->program = program;
	}

	return (PyObject *)obj;
}

