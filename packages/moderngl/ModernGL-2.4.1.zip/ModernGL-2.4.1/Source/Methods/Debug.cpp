#include "Debug.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * DebugInfo(PyObject * self) {
	int viewport[4] = {};
	OpenGL::glGetIntegerv(OpenGL::GL_VIEWPORT, viewport);
	int activeViewportWidth = viewport[2];
	int activeViewportHeight = viewport[3];

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);

	PyObject * activeViewport = PyDict_New();
	PyDict_SetItemString(activeViewport, "width", PyLong_FromLong(activeViewportWidth));
	PyDict_SetItemString(activeViewport, "height", PyLong_FromLong(activeViewportHeight));

	PyObject * dict = PyDict_New();
	PyDict_SetItemString(dict, "versionNumber", PyLong_FromLong(versionNumber));
	PyDict_SetItemString(dict, "maxTextureUnits", PyLong_FromLong(maxTextureUnits));
	PyDict_SetItemString(dict, "defaultVertexArray", PyLong_FromLong(defaultVertexArray));
	PyDict_SetItemString(dict, "activeProgram", PyLong_FromLong(activeProgram));
	PyDict_SetItemString(dict, "activeViewport", activeViewport);

	switch (OpenGL::glGetError()) {
		case OpenGL::GL_NO_ERROR:
			PyDict_SetItemString(dict, "error", PyUnicode_FromString("GL_NO_ERROR"));
			break;

		case OpenGL::GL_INVALID_ENUM:
			PyDict_SetItemString(dict, "error", PyUnicode_FromString("GL_INVALID_ENUM"));
			break;

		case OpenGL::GL_INVALID_VALUE:
			PyDict_SetItemString(dict, "error", PyUnicode_FromString("GL_INVALID_VALUE"));
			break;

		case OpenGL::GL_INVALID_OPERATION:
			PyDict_SetItemString(dict, "error", PyUnicode_FromString("GL_INVALID_OPERATION"));
			break;

		case OpenGL::GL_OUT_OF_MEMORY:
			PyDict_SetItemString(dict, "error", PyUnicode_FromString("GL_OUT_OF_MEMORY"));
			break;
	}

	PyObject * textures = PyList_New(maxTextureUnits);

	for (int i = 0; i < maxTextureUnits; ++i) {
		int binding = 0;
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + i);
		OpenGL::glGetIntegerv(OpenGL::GL_TEXTURE_BINDING_2D, &binding);
		PyList_SET_ITEM(textures, i, PyLong_FromLong(binding));
	}

	PyDict_SetItemString(dict, "textures", textures);
	return dict;
}

PyObject * DebugVar(PyObject * self, PyObject * args) {
	PyObject * obj;

	if (!PyArg_ParseTuple(args, "O:DebugVar", &obj)) {
		return 0;
	}

	if (PyObject_TypeCheck(obj, &FramebufferType)) {
		return PyUnicode_FromString("Framebuffer");
	}

	if (PyObject_TypeCheck(obj, &VertexArrayType)) {
		return PyUnicode_FromString("VertexArray");
	}

	if (PyObject_TypeCheck(obj, &VertexBufferType)) {
		return PyUnicode_FromString("VertexBuffer");
	}

	if (PyObject_TypeCheck(obj, &IndexBufferType)) {
		return PyUnicode_FromString("IndexBuffer");
	}

	if (PyObject_TypeCheck(obj, &UniformBufferType)) {
		return PyUnicode_FromString("UniformBuffer");
	}

	if (PyObject_TypeCheck(obj, &StorageBufferType)) {
		return PyUnicode_FromString("StorageBuffer");
	}

	if (PyObject_TypeCheck(obj, &TextureType)) {
		return PyUnicode_FromString("Texture");
	}

	if (PyObject_TypeCheck(obj, &ShaderType)) {
		return PyUnicode_FromString("Shader");
	}

	if (PyObject_TypeCheck(obj, &ProgramType)) {
		return PyUnicode_FromString("Program");
	}

	if (PyObject_TypeCheck(obj, &UniformLocationType)) {
		return PyUnicode_FromString("UniformLocation");
	}

	if (PyObject_TypeCheck(obj, &UniformBufferLocationType)) {
		return PyUnicode_FromString("UniformBufferLocation");
	}

	if (PyObject_TypeCheck(obj, &ComputeShaderType)) {
		return PyUnicode_FromString("ComputeShader");
	}

	if (PyObject_TypeCheck(obj, &EnableFlagType)) {
		return PyUnicode_FromString("EnableFlag");
	}

	PyErr_Format(ModuleError, "Type %s is not part of ModernGL", GET_OBJECT_TYPENAME(obj));
	return 0;
}


PyObject * Dummy_DebugInfo(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DebugInfo() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DebugInfo() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DebugVar(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DebugVar() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DebugVar() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod DebugMethods[] = {
	{
		301,
		(PyCFunction)DebugInfo,
		(PyCFunction)Dummy_DebugInfo,
		METH_NOARGS,
		"DebugInfo",
		""
	},
	{
		301,
		(PyCFunction)DebugVar,
		(PyCFunction)Dummy_DebugVar,
		METH_VARARGS,
		"DebugVar",
		""
	},
};

int NumDebugMethods = sizeof(DebugMethods) / sizeof(DebugMethods[0]);
