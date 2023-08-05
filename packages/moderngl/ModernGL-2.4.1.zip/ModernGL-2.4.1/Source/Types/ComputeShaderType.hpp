#pragma once

#include "Common.hpp"

struct ComputeShader {
	PyObject_HEAD
	int shader;
	int program;
};

extern PyTypeObject ComputeShaderType;

PyObject * CreateComputeShaderType(int shader, int program);
