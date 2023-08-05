#pragma once

#include "Common.hpp"

extern PyObject * ModuleError;
extern PyObject * ModuleRangeError;
extern PyObject * ModuleCompileError;
extern PyObject * ModuleInvalidFormat;
extern PyObject * ModuleAttributeNotFound;
extern PyObject * ModuleNotInitialized;
extern PyObject * ModuleNotSupported;

void RegisterErrors(PyObject * module);
