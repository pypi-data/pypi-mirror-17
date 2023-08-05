#pragma once

#include "Common.hpp"

struct IndexBuffer {
	PyObject_HEAD
	int ibo;
	int size;
};

extern PyTypeObject IndexBufferType;

PyObject * CreateIndexBufferType(int ibo, int size);
