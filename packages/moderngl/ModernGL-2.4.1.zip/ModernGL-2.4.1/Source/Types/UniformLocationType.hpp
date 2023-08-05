#pragma once

#include "Common.hpp"

struct UniformLocation {
	PyObject_HEAD
	int location;
	int program;
	int type;
};

extern PyTypeObject UniformLocationType;

PyObject * CreateUniformLocationType(int location, int program, int type);
