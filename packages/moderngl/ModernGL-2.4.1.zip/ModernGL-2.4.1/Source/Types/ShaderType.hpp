#pragma once

#include "Common.hpp"

enum ShaderCategory {
	VERTEX_SHADER,
	FRAGMENT_SHADER,
	GEOMETRY_SHADER,
	TESS_EVALUATION_SHADER,
	TESS_CONTROL_SHADER,
	NUM_SHADER_CATEGORIES,
};

struct Shader {
	PyObject_HEAD
	int shader;
	ShaderCategory category;
	bool attached;
};

extern PyTypeObject ShaderType;

PyObject * CreateShaderType(int shader, ShaderCategory category);
