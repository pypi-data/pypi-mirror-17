#pragma once

#include "Common.hpp"

struct Texture {
	PyObject_HEAD
	int texture;
	int width;
	int height;
	int components;
	bool floats;
};

extern PyTypeObject TextureType;

PyObject * CreateTextureType(int texture, int width, int height, int components, bool floats);
