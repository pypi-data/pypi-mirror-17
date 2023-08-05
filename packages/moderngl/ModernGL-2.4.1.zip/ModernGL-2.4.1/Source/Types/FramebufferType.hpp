#pragma once

#include "Common.hpp"

struct Framebuffer {
	PyObject_HEAD
	int fbo;
	int color;
	int depth;
};

extern PyTypeObject FramebufferType;

PyObject * CreateFramebufferType(int fbo, int color, int depth);
