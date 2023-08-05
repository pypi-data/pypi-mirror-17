#include "Experimental.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * ExampleMethod(PyObject * self, PyObject * args, PyObject * kwargs) {
	Py_RETURN_NONE;
}


PyObject * Dummy_ExampleMethod(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ExampleMethod() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ExampleMethod() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod ExperimentalMethods[] = {
	{
		301,
		(PyCFunction)ExampleMethod,
		(PyCFunction)Dummy_ExampleMethod,
		METH_VARARGS | METH_KEYWORDS,
		"ExampleMethod",
		"\n"
	}
};

int NumExperimentalMethods;
