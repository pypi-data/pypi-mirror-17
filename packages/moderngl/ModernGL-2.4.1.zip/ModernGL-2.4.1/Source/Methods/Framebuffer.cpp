#include "Framebuffer.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * NewFramebuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	int width = 0;
	int height = 0;

	int components = 4;

	bool floats = false;
	bool depth = true;

	static const char * kwlist[] = {"width", "height", "components", "floats", "depth", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|iiipp:NewFramebuffer", (char **)kwlist, &width, &height, &components, &floats, &depth)) {
		return 0;
	}

	if (!width && !height) {
		int viewport[4] = {};
		OpenGL::glGetIntegerv(OpenGL::GL_VIEWPORT, viewport);
		width = viewport[2];
		height = viewport[3];
	}

	if (width < 0 || height < 0) {
		PyErr_Format(ModuleRangeError, "NewFramebuffer() width = %d height = %d", width, height);
	}

	const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};

	int pixel_type = floats ? OpenGL::GL_FLOAT : OpenGL::GL_UNSIGNED_BYTE;
	int format = formats[components];

	int framebuffer = 0;
	int colorTexture = 0;
	int depthTexture = 0;

	int defaultFramebuffer = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_DRAW_FRAMEBUFFER_BINDING, (OpenGL::GLint *)&defaultFramebuffer);

	OpenGL::glGenFramebuffers(1, (OpenGL::GLuint *)&framebuffer);
	OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, framebuffer);

	OpenGL::glGenTextures(1, (OpenGL::GLuint *)&colorTexture);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, colorTexture);

	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	OpenGL::glTexImage2D(OpenGL::GL_TEXTURE_2D, 0, format, width, height, 0, format, pixel_type, 0);
	OpenGL::glFramebufferTexture2D(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_COLOR_ATTACHMENT0, OpenGL::GL_TEXTURE_2D, colorTexture, 0);

	if (depth) {
		OpenGL::glGenTextures(1, (OpenGL::GLuint *)&depthTexture);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, depthTexture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexImage2D(OpenGL::GL_TEXTURE_2D, 0, OpenGL::GL_DEPTH_COMPONENT, width, height, 0, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_FLOAT, 0);
		OpenGL::glFramebufferTexture2D(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_DEPTH_ATTACHMENT, OpenGL::GL_TEXTURE_2D, depthTexture, 0);
	}

	OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, defaultFramebuffer);

	PyObject * tuple = PyTuple_New(depth ? 3 : 2);

	PyTuple_SET_ITEM(tuple, 0, CreateFramebufferType(framebuffer, colorTexture, depthTexture));
	PyTuple_SET_ITEM(tuple, 1, CreateTextureType(colorTexture, width, height, 4, floats));

	if (depth) {
		PyTuple_SET_ITEM(tuple, 2, CreateTextureType(depthTexture, width, height, 1, true));
	}

	// validate fbo (https://www.opengl.org/wiki/Framebuffer_Object) (Framebuffer Completeness)

	return tuple;
}

PyObject * DeleteFramebuffer(PyObject * self, PyObject * args) {
	Framebuffer * fbo;

	if (!PyArg_ParseTuple(args, "O!:DeleteFramebuffer", &FramebufferType, &fbo)) {
		return 0;
	}

	OpenGL::glDeleteFramebuffers(1, (OpenGL::GLuint *)&fbo->fbo);

	if (fbo->color) {
		OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&fbo->color);
	}

	if (fbo->depth) {
		OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&fbo->depth);
	}

	Py_RETURN_NONE;
}

PyObject * UseFramebuffer(PyObject * self, PyObject * args) {
	Framebuffer * fbo;

	if (!PyArg_ParseTuple(args, "O!:UseFramebuffer", &FramebufferType, &fbo)) {
		return 0;
	}

	OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, fbo->fbo);

	Py_RETURN_NONE;
}

PyObject * ReadPixels(PyObject * self, PyObject * args, PyObject * kwargs) {
	int x;
	int y;
	int width;
	int height;
	int components = 3;
	bool floats = false;

	static const char * kwlist[] = {"x", "y", "width", "height", "components", "floats", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiii|ip:ReadPixels", (char **)kwlist, &x, &y, &width, &height, &components, &floats)) {
		return 0;
	}

	if (width <= 0 || height <= 0 || components < 1 || components > 4) {
		PyErr_Format(ModuleRangeError, "ReadPixels() width = %d height = %d components = %d", width, height, components);
	}

	int size = floats ? (width * height * 4) : (height * ((width * components + 3) & ~3));
	int pixel_type = floats ? OpenGL::GL_FLOAT : OpenGL::GL_UNSIGNED_BYTE;

	const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};
	int format = formats[components];

	PyObject * bytes = PyBytes_FromStringAndSize(0, size);
	char * data = PyBytes_AS_STRING(bytes);

	OpenGL::glReadPixels(x, y, width, height, format, pixel_type, data);
	data[size] = 0;

	return bytes;
}

PyObject * ReadDepthPixels(PyObject * self, PyObject * args, PyObject * kwargs) {
	int x;
	int y;
	int width;
	int height;
	bool floats = true;

	static const char * kwlist[] = {"x", "y", "width", "height", "floats", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiii|p:ReadDepthPixels", (char **)kwlist, &x, &y, &width, &height, &floats)) {
		return 0;
	}

	if (width < 0 || height < 0) {
		PyErr_Format(ModuleRangeError, "ReadDepthPixels() width = %d height = %d", width, height);
	}

	int size = floats ? (width * height * 4) : (height * ((width + 3) & ~3));
	int pixel_type = floats ? OpenGL::GL_FLOAT : OpenGL::GL_UNSIGNED_BYTE;

	PyObject * bytes = PyBytes_FromStringAndSize(0, size);
	char * data = PyBytes_AS_STRING(bytes);
	OpenGL::glReadPixels(x, y, width, height, OpenGL::GL_DEPTH_COMPONENT, pixel_type, data);
	data[size] = 0;

	return bytes;
}

PyObject * ReadPixel(PyObject * self, PyObject * args, PyObject * kwargs) {
	int x;
	int y;
	int components = 3;
	bool floats = false;

	static const char * kwlist[] = {"x", "y", "components", "floats", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ii|ip:ReadPixel", (char **)kwlist, &x, &y, &components, &floats)) {
		return 0;
	}

	if (components < 1 || components > 4) {
		// TODO:
	}

	PyObject * tuple = PyTuple_New(components);

	if (floats) {
		float rgba[4];
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_RGBA, OpenGL::GL_FLOAT, &rgba);
		for (int i = 0; i < components; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyFloat_FromDouble(rgba[i]));
		}
	} else {
		unsigned char rgba[4];
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_RGBA, OpenGL::GL_UNSIGNED_BYTE, &rgba);
		for (int i = 0; i < components; ++i) {
			PyTuple_SET_ITEM(tuple, i, PyLong_FromUnsignedLong(rgba[i]));
		}
	}

	return tuple;
}

PyObject * ReadDepthPixel(PyObject * self, PyObject * args, PyObject * kwargs) {
	int x;
	int y;
	bool floats = true;

	static const char * kwlist[] = {"x", "y", "floats", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ii|p:ReadDepthPixel", (char **)kwlist, &x, &y, &floats)) {
		return 0;
	}

	if (floats) {
		float depth = 0.0;
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_FLOAT, &depth);
		return PyFloat_FromDouble(depth);
	} else {
		unsigned depth = 0;
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_UNSIGNED_BYTE, &depth);
		return PyLong_FromUnsignedLong(depth);
	}
}


PyObject * Dummy_NewFramebuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewFramebuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewFramebuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteFramebuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteFramebuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteFramebuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UseFramebuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UseFramebuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UseFramebuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_ReadPixel(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ReadPixel() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ReadPixel() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_ReadPixels(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ReadPixels() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ReadPixels() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_ReadDepthPixel(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ReadDepthPixel() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ReadDepthPixel() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_ReadDepthPixels(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ReadDepthPixels() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ReadDepthPixels() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod FramebufferMethods[] = {
	{
		301,
		(PyCFunction)NewFramebuffer,
		(PyCFunction)Dummy_NewFramebuffer,
		METH_VARARGS | METH_KEYWORDS,
		"NewFramebuffer",
		"Creates a framebuffer with two texture attachments. (color and depth)\n"
		"The color attachment have RGBA format, 8bit for each channel.\n"
		"The depth texture contains float values.\n"
		"\n"

		"Parameters:\n"
		"\twidth (int) Width of the framebuffer. By default is 0\n"
		"\theight (int) Height of the framebuffer. By default is 0\n"
		"\tfloats (bool) Single-precision floating-point format. By default is False\n"
		"\tdepth (bool) Depth attachment. By default is True\n"
		"\n"

		"Returns:\n"
		"\tfbo (int) The index of the new framebuffer object.\n"
		"\tcolor (int) The index of the color attachment texture object.\n"
		"\tdepth (int) The index of the depth attachment texture object if depth parameter is True.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DeleteFramebuffer,
		(PyCFunction)Dummy_DeleteFramebuffer,
		METH_VARARGS,
		"DeleteFramebuffer",
		"\n"

		"Parameters:\n"
		"\tframebuffer (int) Index of the framebuffer returned by the NewFramebuffer.\n"
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
		(PyCFunction)UseFramebuffer,
		(PyCFunction)Dummy_UseFramebuffer,
		METH_VARARGS,
		"UseFramebuffer",
		"Bind a framebuffer.\n"
		"\n"

		"Parameters:\n"
		"\tframebuffer (int) Index of the framebuffer returned by the NewFramebuffer.\n"
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
		(PyCFunction)ReadPixels,
		(PyCFunction)Dummy_ReadPixels,
		METH_VARARGS | METH_KEYWORDS,
		"ReadPixels",
		"Read the pixels from the active framebuffer.\n"
		"\n"

		"Parameters:\n"
		"\tx (int) Offset of the image to read.\n"
		"\ty (int) Offset of the image to read.\n"
		"\twidth (int) Width of the image to read.\n"
		"\theight (int) Height of the image to read.\n"
		"\tcomponents (int) By default is 3\n"
		"\tfloats (bool) Single-precision floating-point format. By default is False\n"
		"\n"

		"Returns:\n"
		"\tpixels (bytes) The color channels selected by components from the active framebuffer.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)ReadDepthPixels,
		(PyCFunction)Dummy_ReadDepthPixels,
		METH_VARARGS | METH_KEYWORDS,
		"ReadDepthPixels",
		"Read the depth pixels from the active framebuffer.\n"
		"\n"

		"Parameters:\n"
		"\tx (int) Offset of the image to read.\n"
		"\ty (int) Offset of the image to read.\n"
		"\twidth (int) Width of the image to read.\n"
		"\theight (int) Height of the image to read.\n"
		"\tfloats (bool) Single-precision floating-point format. By default is True\n"
		"\n"

		"Returns:\n"
		"\tpixels (bytes) The depth channel from the active framebuffer.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)ReadPixel,
		(PyCFunction)Dummy_ReadPixel,
		METH_VARARGS | METH_KEYWORDS,
		"ReadPixel",
		"Read a single pixel from the active framebuffer.\n"
		"\n"

		"Parameters:\n"
		"\tx (int) Offset of the pixel to read.\n"
		"\ty (int) Offset of the pixel to read.\n"
		"\tfloats (bool) Single-precision floating-point format. By default is False\n"
		"\n"

		"Returns:\n"
		"\trgba (tuple) The rgba value at (x, y) from the active framebuffer.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)ReadDepthPixel,
		(PyCFunction)Dummy_ReadDepthPixel,
		METH_VARARGS | METH_KEYWORDS,
		"ReadDepthPixel",
		"Read a single depth value from the active framebuffer.\n"
		"\n"

		"Parameters:\n"
		"\tx (int) Offset of the pixel to read.\n"
		"\ty (int) Offset of the pixel to read.\n"
		"\tfloats (bool) Single-precision floating-point format. By default is True\n"
		"\n"

		"Returns:\n"
		"\tdepth (float) The depth value at (x, y) from the active framebuffer.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
};

int NumFramebufferMethods = sizeof(FramebufferMethods) / sizeof(FramebufferMethods[0]);
