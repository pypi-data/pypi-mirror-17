#include "ProgramType.hpp"

#include "Errors.hpp"

PyObject * Program_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int Program_init(Program * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate Program.\nCall NewProgram(...) to get a Program object.");
	return -1;
}

void Program_dealloc(Program * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * Program_str(Program * self) {
	return PyUnicode_FromFormat("<Program = %d>", self->program);
}

PyObject * Program_get_item(Program * self, PyObject * key) {
	PyObject * value = PyDict_GetItem(self->iface, key);
	Py_INCREF(value);
	return value;
}

PyMemberDef Program_members[] = {
	{"interface", T_OBJECT_EX, offsetof(Program, iface), 0, "Program interface"},
	{0},
};

PyMappingMethods Program_map = {
	0,
	(binaryfunc)Program_get_item,
	0,
};

PyTypeObject ProgramType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Program",
	sizeof(Program),
	0,
	(destructor)Program_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)Program_str,
	0,
	0,
	&Program_map,
	0,
	0,
	(reprfunc)Program_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"Program",
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	Program_members,
	0,
	0,
	0,
	0,
	0,
	0,
	(initproc)Program_init,
	0,
	Program_new,
};

PyObject * CreateProgramType(int program, PyObject * iface) {
	Program * obj = (Program *)ProgramType.tp_alloc(&ProgramType, 0);

	if (obj != 0) {
		obj->program = program;
		obj->iface = iface;
	}

	return (PyObject *)obj;
}
