#include "Errors.hpp"

PyObject * ModuleError;
PyObject * ModuleRangeError;
PyObject * ModuleCompileError;
PyObject * ModuleInvalidFormat;
PyObject * ModuleAttributeNotFound;
PyObject * ModuleNotInitialized;
PyObject * ModuleNotSupported;

void RegisterErrors(PyObject * module) {
	ModuleError = PyErr_NewException((char *)"ModernGL.Error", 0, 0);
	Py_INCREF(ModuleError);

	ModuleRangeError = PyErr_NewException((char *)"ModernGL.RangeError", ModuleError, 0);
	Py_INCREF(ModuleRangeError);

	ModuleCompileError = PyErr_NewException((char *)"ModernGL.CompileError", ModuleError, 0);
	Py_INCREF(ModuleCompileError);

	ModuleInvalidFormat = PyErr_NewException((char *)"ModernGL.InvalidFormat", ModuleError, 0);
	Py_INCREF(ModuleInvalidFormat);

	ModuleAttributeNotFound = PyErr_NewException((char *)"ModernGL.AttributeNotFound", ModuleError, 0);
	Py_INCREF(ModuleAttributeNotFound);

	ModuleNotInitialized = PyErr_NewException((char *)"ModernGL.NotInitialized", ModuleError, 0);
	Py_INCREF(ModuleNotInitialized);

	ModuleNotSupported = PyErr_NewException((char *)"ModernGL.NotSupported", ModuleError, 0);
	Py_INCREF(ModuleNotSupported);

	PyModule_AddObject(module, "Error", ModuleError);
	PyModule_AddObject(module, "RangeError", ModuleRangeError);
	PyModule_AddObject(module, "CompileError", ModuleCompileError);
	PyModule_AddObject(module, "InvalidFormat", ModuleInvalidFormat);
	PyModule_AddObject(module, "AttributeNotFound", ModuleAttributeNotFound);
	PyModule_AddObject(module, "NotInitialized", ModuleNotInitialized);
	PyModule_AddObject(module, "NotSupported", ModuleNotSupported);
}
