#pragma once

#include "Common.hpp"

struct Program {
	PyObject_HEAD
	int program;
	PyObject * iface;
};

extern PyTypeObject ProgramType;

PyObject * CreateProgramType(int program, PyObject * iface);
