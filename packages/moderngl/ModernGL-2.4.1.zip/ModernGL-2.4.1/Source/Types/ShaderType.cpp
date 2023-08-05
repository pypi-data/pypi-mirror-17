#include "ShaderType.hpp"

#include "Errors.hpp"

PyObject * Shader_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int Shader_init(Shader * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate Shader.\nCall New...Shader(...) to get a Shader object.");
	return -1;
}

void Shader_dealloc(Shader * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * Shader_str(Shader * self) {
	return PyUnicode_FromFormat("<Shader = %d>", self->shader);
}

PyTypeObject ShaderType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Shader",
	sizeof(Shader),
	0,
	(destructor)Shader_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)Shader_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)Shader_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"Shader",
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
	(initproc)Shader_init,
	0,
	Shader_new,
};

PyObject * CreateShaderType(int shader, ShaderCategory category) {
	Shader * obj = (Shader *)ShaderType.tp_alloc(&ShaderType, 0);

	if (obj != 0) {
		obj->shader = shader;
		obj->category = category;
		obj->attached = false;
	}

	return (PyObject *)obj;
}
