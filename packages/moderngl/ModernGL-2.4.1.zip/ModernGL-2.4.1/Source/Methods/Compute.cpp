#include "Compute.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * NewComputeShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewComputeShader", &source)) {
		return 0;
	}

	int shader = OpenGL::glCreateShader(OpenGL::GL_COMPUTE_SHADER);
	OpenGL::glShaderSource(shader, 1, &source, 0);
	OpenGL::glCompileShader(shader);

	int compiled = OpenGL::GL_FALSE;
	OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
	if (!compiled) {
		static const char * logTitle = "NewComputeShader() compile failed\n";
		static int logTitleLength = strlen(logTitle);

		int logLength = 0;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_INFO_LOG_LENGTH, &logLength);
		int logTotalLength = logLength + logTitleLength;

		PyObject * content = PyUnicode_New(logTotalLength, 255);
		if (PyUnicode_READY(content)) {
			OpenGL::glDeleteShader(shader);
			return 0;
		}

		char * data = (char *)PyUnicode_1BYTE_DATA(content);
		memcpy(data, logTitle, logTitleLength);

		int logSize = 0;
		OpenGL::glGetShaderInfoLog(shader, logLength, &logSize, data + logTitleLength);
		data[logTitleLength] = 0;

		OpenGL::glDeleteShader(shader);

		PyErr_SetObject(ModuleCompileError, content);
		return 0;
	}

	int program = OpenGL::glCreateProgram();

	OpenGL::glAttachShader(program, shader);

	int linked = OpenGL::GL_FALSE;
	OpenGL::glLinkProgram(program);
	OpenGL::glGetProgramiv(program, OpenGL::GL_LINK_STATUS, &linked);

	if (!linked) {
		static const char * logTitle = "NewComputeShader() linking failed\n";
		static int logTitleLength = strlen(logTitle);

		int logLength = 0;
		OpenGL::glGetProgramiv(program, OpenGL::GL_INFO_LOG_LENGTH, &logLength);
		int logTotalLength = logLength + logTitleLength;

		PyObject * content = PyUnicode_New(logTotalLength, 255);
		if (PyUnicode_READY(content)) {
			OpenGL::glDeleteProgram(program);
			OpenGL::glDeleteShader(shader);
			return 0;
		}

		char * data = (char *)PyUnicode_1BYTE_DATA(content);
		memcpy(data, logTitle, logTitleLength);

		int logSize = 0;
		OpenGL::glGetProgramInfoLog(program, logLength, &logSize, data + logTitleLength);
		data[logTitleLength] = 0;

		OpenGL::glDeleteProgram(program);
		OpenGL::glDeleteShader(shader);

		PyErr_SetObject(ModuleCompileError, content);
		return 0;
	}

	return CreateComputeShaderType(shader, program);
}

PyObject * DeleteComputeShader(PyObject * self, PyObject * args) {
	ComputeShader * shader;

	if (!PyArg_ParseTuple(args, "O!:DeleteComputeShader", &ComputeShaderType, &shader)) {
		return 0;
	}

	OpenGL::glDeleteProgram(shader->program);
	OpenGL::glDeleteShader(shader->shader);
	Py_RETURN_NONE;
}

PyObject * RunComputeShader(PyObject * self, PyObject * args, PyObject * kwargs) {
	ComputeShader * shader;
	int x = 1;
	int y = 1;
	int z = 1;

	static const char * kwlist[] = {"shader", "x", "y", "z", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|iii:RunComputeShader", (char **)kwlist, &ComputeShaderType, &shader, &x, &y, &z)) {
		return 0;
	}

	OpenGL::glUseProgram(shader->program);
	OpenGL::glDispatchCompute(x, y, z);
	Py_RETURN_NONE;
}


PyObject * Dummy_NewComputeShader(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewComputeShader() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewComputeShader() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteComputeShader(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteComputeShader() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteComputeShader() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_RunComputeShader(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "RunComputeShader() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "RunComputeShader() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}


PythonMethod ComputeMethods[] = {
	{
		403,
		(PyCFunction)NewComputeShader,
		(PyCFunction)Dummy_NewComputeShader,
		METH_VARARGS,
		"NewComputeShader",
		"Compiles and links a compute shader from GLSL source.\n"
		"\n"

		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"
		"\n"

		"Returns:\n"
		"\tprogram (ModernGL.ComputeShader) The index of the new program object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DeleteComputeShader,
		(PyCFunction)Dummy_DeleteComputeShader,
		METH_VARARGS,
		"DeleteComputeShader",
		"Compute shader is a standalone shader program.\n"
		"\n"

		"Parameters:\n"
		"\tprogram (ModernGL.ComputeShader) The index of a program object returned by the ModernGL.NewComputeShader.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\n"
	},
	{
		403,
		(PyCFunction)RunComputeShader,
		(PyCFunction)Dummy_RunComputeShader,
		METH_VARARGS | METH_KEYWORDS,
		"RunComputeShader",
		"Run the compute shader.\n"
		"\n"

		"Parameters:\n"
		"\tprogram (ModernGL.ComputeShader) The index of a program object returned by the ModernGL.NewComputeShader.\n"
		"\tx (int) The x group size of the workers. By default is 1\n"
		"\ty (int) The y group size of the workers. By default is 1\n"
		"\tz (int) The z group size of the workers. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\n"
	},
};

int NumComputeMethods = sizeof(ComputeMethods) / sizeof(ComputeMethods[0]);
