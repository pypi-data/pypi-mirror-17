#include "EnableFlagType.hpp"

#include "Errors.hpp"

const char * enableTable[] = {
	"Nothing",
	"Blend",
	"CullFace",
	"Blend, CullFace",
	"DepthTest",
	"Blend, DepthTest",
	"CullFace, DepthTest",
	"Blend, CullFace, DepthTest",
	"Multisample",
	"Blend, Multisample",
	"CullFace, Multisample",
	"Blend, CullFace, Multisample",
	"DepthTest, Multisample",
	"Blend, DepthTest, Multisample",
	"CullFace, DepthTest, Multisample",
	"Blend, CullFace, DepthTest, Multisample",
};

PyObject * EnableFlag_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int EnableFlag_init(EnableFlag * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate EnableFlag.");
	return -1;
}

void EnableFlag_dealloc(EnableFlag * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * EnableFlag_str(EnableFlag * self) {
	return PyUnicode_FromFormat("<EnableFlag = %s>", enableTable[self->value]);
}

PyObject * EnableFlag_add(EnableFlag * a, EnableFlag * b) {
	CHECK_AND_REPORT_ARG_TYPE_ERROR("a", a, EnableFlagType);
	CHECK_AND_REPORT_ARG_TYPE_ERROR("b", b, EnableFlagType);
	return CreateEnableFlagType(a->value | b->value);
}

PyObject * EnableFlag_sub(EnableFlag * a, EnableFlag * b) {
	CHECK_AND_REPORT_ARG_TYPE_ERROR("a", a, EnableFlagType);
	CHECK_AND_REPORT_ARG_TYPE_ERROR("b", b, EnableFlagType);
	return CreateEnableFlagType(a->value & (~b->value));
}

PyNumberMethods EnableFlag_num = {
	(binaryfunc)EnableFlag_add,
	(binaryfunc)EnableFlag_sub,
};

PyTypeObject EnableFlagType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.EnableFlag",
	sizeof(EnableFlag),
	0,
	(destructor)EnableFlag_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)EnableFlag_str,
	&EnableFlag_num,
	0,
	0,
	0,
	0,
	(reprfunc)EnableFlag_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"EnableFlag",
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
	(initproc)EnableFlag_init,
	0,
	EnableFlag_new,
};

PyObject * CreateEnableFlagType(unsigned value) {
	EnableFlag * obj = (EnableFlag *)EnableFlagType.tp_alloc(&EnableFlagType, 0);

	if (obj != 0) {
		obj->value = value;
	}

	return (PyObject *)obj;
}
