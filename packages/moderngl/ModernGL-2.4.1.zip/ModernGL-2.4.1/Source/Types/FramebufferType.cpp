#include "FramebufferType.hpp"

#include "Errors.hpp"

PyObject * Framebuffer_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int Framebuffer_init(Framebuffer * self, PyObject * args, PyObject * kwargs) {
	int fbo;

	static const char * kwlist[] = {"fbo", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "I|:NewFramebuffer", (char **)kwlist, &fbo)) {
		return -1;
	}

	self->fbo = fbo;
	self->color = 0;
	self->depth = 0;

	return 0;
}

void Framebuffer_dealloc(Framebuffer * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * Framebuffer_str(Framebuffer * self) {
	return PyUnicode_FromFormat("<Framebuffer = %d>", self->fbo);
}

PyTypeObject FramebufferType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Framebuffer",
	sizeof(Framebuffer),
	0,
	(destructor)Framebuffer_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)Framebuffer_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)Framebuffer_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"Framebuffer",
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
	(initproc)Framebuffer_init,
	0,
	Framebuffer_new,
};

PyObject * CreateFramebufferType(int fbo, int color, int depth) {
	Framebuffer * obj = (Framebuffer *)FramebufferType.tp_alloc(&FramebufferType, 0);

	if (obj != 0) {
		obj->fbo = fbo;
		obj->color = color;
		obj->depth = depth;
	}

	return (PyObject *)obj;
}

