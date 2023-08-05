#include "TextureType.hpp"

#include "Errors.hpp"

PyObject * Texture_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	return type->tp_alloc(type, 0);
}

int Texture_init(Texture * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Cannot instantiate Texture.\nCall NewTexture(...) to get a Texture object.");
	return -1;
}

void Texture_dealloc(Texture * self) {
	Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject * Texture_str(Texture * self) {
	return PyUnicode_FromFormat("<Texture = %d>", self->texture);
}

PyTypeObject TextureType = {
	PyVarObject_HEAD_INIT(0, 0)
	"ModernGL.Texture",
	sizeof(Texture),
	0,
	(destructor)Texture_dealloc,
	0,
	0,
	0,
	0,
	(reprfunc)Texture_str,
	0,
	0,
	0,
	0,
	0,
	(reprfunc)Texture_str,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"Texture",
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
	(initproc)Texture_init,
	0,
	Texture_new,
};

PyObject * CreateTextureType(int texture, int width, int height, int components, bool floats) {
	Texture * obj = (Texture *)TextureType.tp_alloc(&TextureType, 0);

	if (obj != 0) {
		obj->texture = texture;
		obj->width = width;
		obj->height = height;
		obj->components = components;
		obj->floats = floats;
	}

	return (PyObject *)obj;
}
