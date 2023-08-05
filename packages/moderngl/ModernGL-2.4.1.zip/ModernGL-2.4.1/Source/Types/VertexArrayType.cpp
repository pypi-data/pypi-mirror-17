#include "VertexArrayType.hpp"

#include "Errors.hpp"

PyObject * VertexArray_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int VertexArray_init(VertexArray * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate VertexArray.\nCall NewVertexArray(...) to get a VertexArray object.");
	return -1;
}

void VertexArray_dealloc(VertexArray * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * VertexArray_str(VertexArray * self) {
	return PyUnicode_FromFormat("<VertexArray = %d>", self->vao);
}

PyTypeObject VertexArrayType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.VertexArray",
	sizeof(VertexArray),
	0,
	(destructor)VertexArray_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)VertexArray_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)VertexArray_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"VertexArray",
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
	(initproc)VertexArray_init,
	0,
	VertexArray_new,
};

PyObject * CreateVertexArrayType(int vao, int program, bool indexed) {
	VertexArray * obj = (VertexArray *)VertexArrayType.tp_alloc(&VertexArrayType, 0);

	if (obj != 0) {
		obj->vao = vao;
		obj->program = program;
		obj->indexed = indexed;
	}

	return (PyObject *)obj;
}
