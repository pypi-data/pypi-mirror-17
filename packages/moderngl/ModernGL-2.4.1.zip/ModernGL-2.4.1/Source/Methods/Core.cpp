#include "Core.hpp"

#include "Types.hpp"
#include "Constants.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * GetInfo(PyObject * self) {
	int major = 0;
	int minor = 0;
	int samples = 0;

	OpenGL::glGetIntegerv(OpenGL::GL_MAJOR_VERSION, &major);
	OpenGL::glGetIntegerv(OpenGL::GL_MINOR_VERSION, &minor);
	OpenGL::glGetIntegerv(OpenGL::GL_MAX_SAMPLES, &samples);
	const char * vendor = (const char *)OpenGL::glGetString(OpenGL::GL_VENDOR);
	const char * renderer = (const char *)OpenGL::glGetString(OpenGL::GL_RENDERER);

	if (!vendor) {
		vendor = "";
	}

	if (!renderer) {
		renderer = "";
	}

	PyObject * dict = PyDict_New();
	PyDict_SetItemString(dict, "version", PyTuple_Pack(2, PyLong_FromLong(major), PyLong_FromLong(minor)));
	PyDict_SetItemString(dict, "samples", PyLong_FromLong(major));
	PyDict_SetItemString(dict, "vendor", PyUnicode_FromString(vendor));
	PyDict_SetItemString(dict, "renderer", PyUnicode_FromString(renderer));
	return dict;
}

PyObject * Viewport(PyObject * self, PyObject * args, PyObject * kwargs) {
	int x;
	int y;
	int width;
	int height;

	static const char * kwlist[] = {"x", "y", "width", "height", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiii:Viewport", (char **)kwlist, &x, &y, &width, &height)) {
		return 0;
	}

	OpenGL::glViewport(x, y, width, height);
	Py_RETURN_NONE;
}

PyObject * Clear(PyObject * self, PyObject * args, PyObject * kwargs) {
	unsigned char r = 0;
	unsigned char g = 0;
	unsigned char b = 0;
	unsigned char a = 255;

	static const char * kwlist[] = {"r", "g", "b", "a", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|bbbb:Clear", (char **)kwlist, &r, &g, &b, &a)) {
		return 0;
	}

	const float c = 1.0f / 255.0f;
	OpenGL::glClearColor(r * c, g * c, b * c, a * c);
	OpenGL::glClear(OpenGL::GL_DEPTH_BUFFER_BIT | OpenGL::GL_COLOR_BUFFER_BIT);
	Py_RETURN_NONE;
}

PyObject * PointSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:PointSize", &size)) {
		return 0;
	}

	OpenGL::glPointSize(size);
	Py_RETURN_NONE;
}

PyObject * LineSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:LineSize", &size)) {
		return 0;
	}

	OpenGL::glLineWidth(size);
	Py_RETURN_NONE;
}

PyObject * EnableOnly(PyObject * self, PyObject * args) {
	EnableFlag * flags;

	if (!PyArg_ParseTuple(args, "O!:EnableOnly", &EnableFlagType, &flags)) {
		return 0;
	}

	(flags->value & ENABLE_BLEND ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_BLEND);
	(flags->value & ENABLE_CULL_FACE ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_CULL_FACE);
	(flags->value & ENABLE_DEPTH_TEST ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_DEPTH_TEST);
	(flags->value & ENABLE_MULTISAMPLE ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_MULTISAMPLE);
	Py_RETURN_NONE;
}


PyObject * EnableBlend(PyObject * self) {
	OpenGL::glEnable(OpenGL::GL_BLEND);
	Py_RETURN_NONE;
}

PyObject * DisableBlend(PyObject * self) {
	OpenGL::glDisable(OpenGL::GL_BLEND);
	Py_RETURN_NONE;
}

PyObject * EnableCullFace(PyObject * self) {
	OpenGL::glEnable(OpenGL::GL_CULL_FACE);
	Py_RETURN_NONE;
}

PyObject * DisableCullFace(PyObject * self) {
	OpenGL::glDisable(OpenGL::GL_CULL_FACE);
	Py_RETURN_NONE;
}

PyObject * EnableDepthTest(PyObject * self) {
	OpenGL::glEnable(OpenGL::GL_DEPTH_TEST);
	Py_RETURN_NONE;
}

PyObject * DisableDepthTest(PyObject * self) {
	OpenGL::glDisable(OpenGL::GL_DEPTH_TEST);
	Py_RETURN_NONE;
}

PyObject * EnableMultisample(PyObject * self) {
	OpenGL::glEnable(OpenGL::GL_MULTISAMPLE);
	Py_RETURN_NONE;
}

PyObject * DisableMultisample(PyObject * self) {
	OpenGL::glDisable(OpenGL::GL_MULTISAMPLE);
	Py_RETURN_NONE;
}


PyObject * Dummy_Viewport(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "Viewport() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "Viewport() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_Clear(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "Clear() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "Clear() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_GetInfo(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "GetInfo() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "GetInfo() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_PointSize(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "PointSize() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "PointSize() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_LineSize(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "LineSize() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "LineSize() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableOnly(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableOnly() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableOnly() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableBlend(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableBlend() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableBlend() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableCullFace(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableCullFace() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableCullFace() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableDepthTest(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableDepthTest() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableDepthTest() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableMultisample(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableMultisample() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableMultisample() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DisableBlend(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DisableBlend() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DisableBlend() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DisableCullFace(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DisableCullFace() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DisableCullFace() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DisableDepthTest(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DisableDepthTest() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DisableDepthTest() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DisableMultisample(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DisableMultisample() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DisableMultisample() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod CoreMethods[] = {
	{
		301,
		(PyCFunction)GetInfo,
		(PyCFunction)Dummy_GetInfo,
		METH_NOARGS,
		"GetInfo",
		"Get information about the OpenGL context.\n"
		"The module must be initialized first.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tinfo (dict) Dictionary with the results of the most popular queries using glGet.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)Viewport,
		(PyCFunction)Dummy_Viewport,
		METH_VARARGS | METH_KEYWORDS,
		"Viewport",
		"Set the viewport for rendering.\n"
		"\n"

		"Parameters:\n"
		"\tx (int) Position of the viewport.\n"
		"\ty (int) Position of the viewport.\n"
		"\twidth (int) Width of the viewport.\n"
		"\theight (int) Height of the viewport.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)Clear,
		(PyCFunction)Dummy_Clear,
		METH_VARARGS | METH_KEYWORDS,
		"Clear",
		"Clear the viewport with the specified colors.\n"
		"Also clears the depth attachments.\n"
		"\n"

		"Parameters:\n"
		"\tr (int) Clear value for the red channel. By default is 0\n"
		"\tg (int) Clear value for the green channel. By default is 0\n"
		"\tb (int) Clear value for the blue channel. By default is 0\n"
		"\ta (int) Clear value for the alpha channel. By default is 255\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)PointSize,
		(PyCFunction)Dummy_PointSize,
		METH_VARARGS,
		"PointSize",
		"Set the size of the point primitive.\n"
		"\n"

		"Parameters:\n"
		"\tsize (float) Size of the point.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)LineSize,
		(PyCFunction)Dummy_LineSize,
		METH_VARARGS,
		"LineSize",
		"Set the with of the line primitive.\n"
		"\n"

		"Parameters:\n"
		"\tsize (float) Width of the line.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)EnableOnly,
		(PyCFunction)Dummy_EnableOnly,
		METH_VARARGS,
		"EnableOnly",
		"Enables only the specified flags.\n"
		"The enable flags are:\n"
		"- ModernGL.ENABLE_NOTHING\n"
		"- ModernGL.ENABLE_BLEND\n"
		"- ModernGL.ENABLE_CULL_FACE\n"
		"- ModernGL.ENABLE_DEPTH_TEST\n"
		"- ModernGL.ENABLE_MULTISAMPLE\n"
		"- ModernGL.ENABLE_ALL\n"
		"\n"

		"Parameters:\n"
		"\tflags (ModernGL.EnableFlag) A combination of the enable flags using + and - operators.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)EnableBlend,
		(PyCFunction)Dummy_EnableBlend,
		METH_NOARGS,
		"EnableBlend",
		"Enable blending.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DisableBlend,
		(PyCFunction)Dummy_DisableBlend,
		METH_NOARGS,
		"DisableBlend",
		"Disable blending.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)EnableCullFace,
		(PyCFunction)Dummy_EnableCullFace,
		METH_NOARGS,
		"EnableCullFace",
		"Enable face culling.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DisableCullFace,
		(PyCFunction)Dummy_DisableCullFace,
		METH_NOARGS,
		"DisableCullFace",
		"Disable face culling.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)EnableDepthTest,
		(PyCFunction)Dummy_EnableDepthTest,
		METH_NOARGS,
		"EnableDepthTest",
		"Enable depth testing.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DisableDepthTest,
		(PyCFunction)Dummy_DisableDepthTest,
		METH_NOARGS,
		"DisableDepthTest",
		"Disable depth testing.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)EnableMultisample,
		(PyCFunction)Dummy_EnableMultisample,
		METH_NOARGS,
		"EnableMultisample",
		"Enable multisampling.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DisableMultisample,
		(PyCFunction)Dummy_DisableMultisample,
		METH_NOARGS,
		"DisableMultisample",
		"Disable multisampling.\n"
		"\n"

		"Parameters:\n"
		"\tNone\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
};

int NumCoreMethods = sizeof(CoreMethods) / sizeof(CoreMethods[0]);
