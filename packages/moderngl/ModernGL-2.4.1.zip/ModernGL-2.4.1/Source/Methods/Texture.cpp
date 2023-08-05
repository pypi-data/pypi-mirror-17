#include "Texture.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * NewTexture(PyObject * self, PyObject * args, PyObject * kwargs) {
	int width;
	int height;
	const void * data;
	int components = 3;
	int size;
	bool floats = false;

	static const char * kwlist[] = {"width", "height", "data", "components", "floats", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiy#|ip:NewTexture", (char **)kwlist, &width, &height, &data, &size, &components, &floats)) {
		return 0;
	}

	if (width <= 0 || height <= 0 || components < 1 || components > 4) {
		PyErr_Format(ModuleRangeError, "NewTexture() width = %d height = %d components = %d", width, height, components);
	}

	int expected_size = floats ? (width * height * 4) : (height * ((width * components + 3) & ~3));

	if (size != expected_size) {
		PyErr_Format(ModuleRangeError, "NewTexture() expected size is %d, not %d", expected_size, size);
		return 0;
	}

	const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};

	int pixel_type = floats ? OpenGL::GL_FLOAT : OpenGL::GL_UNSIGNED_BYTE;
	int format = formats[components];

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);

	int texture = 0;
	OpenGL::glGenTextures(1, (OpenGL::GLuint *)&texture);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	OpenGL::glTexImage2D(OpenGL::GL_TEXTURE_2D, 0, format, width, height, 0, format, pixel_type, data);
	return CreateTextureType(texture, width, height, components, floats);
}

PyObject * DeleteTexture(PyObject * self, PyObject * args) {
	Texture * texture;

	if (!PyArg_ParseTuple(args, "O!:DeleteTexture", &TextureType, &texture)) {
		return 0;
	}

	OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&texture->texture);
	Py_RETURN_NONE;
}

PyObject * UpdateTexture(PyObject * self, PyObject * args, PyObject * kwargs) {
	Texture * texture;
	int x = 0;
	int y = 0;
	int width = 0;
	int height = 0;
	const void * data;
	int size;

	static const char * kwlist[] = {"texture", "data", "x", "y", "width", "height", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!y#|iiii:UpdateTexture", (char **)kwlist, &TextureType, &texture, &data, &size, &x, &y, &width, &height)) {
		return 0;
	}

	if (width == 0) {
		width = texture->width;
	}

	if (height == 0) {
		height = texture->height;
	}

	if (x < 0 || y < 0 || width < 0 || height < 0 || x + width > texture->width || y + height > texture->height) {
		PyErr_Format(ModuleRangeError, "UpdateTexture() x = %d y = %d width = %d height = %d", x, y, width, height);
	}

	const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};

	int pixel_type = texture->floats ? OpenGL::GL_FLOAT : OpenGL::GL_UNSIGNED_BYTE;
	int format = formats[texture->components];

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	OpenGL::glTexSubImage2D(OpenGL::GL_TEXTURE_2D, 0, x, y, width, height, format, pixel_type, data);
	Py_RETURN_NONE;
}

PyObject * UseTexture(PyObject * self, PyObject * args) {
	Texture * texture;
	int location = 0;

	if (!PyArg_ParseTuple(args, "O!|i:UseTexture", &TextureType, &texture, &location)) {
		return 0;
	}

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + location);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	Py_RETURN_NONE;
}

PyObject * SetTexturePixelated(PyObject * self, PyObject * args) {
	Texture * texture;

	if (!PyArg_ParseTuple(args, "O!:SetTexturePixelated", &TextureType, &texture)) {
		return 0;
	}

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_NEAREST);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_NEAREST);
	Py_RETURN_NONE;
}

PyObject * SetTextureFiltered(PyObject * self, PyObject * args) {
	Texture * texture;

	if (!PyArg_ParseTuple(args, "O!:SetTextureFiltered", &TextureType, &texture)) {
		return 0;
	}

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	Py_RETURN_NONE;
}

PyObject * SetTextureMipmapped(PyObject * self, PyObject * args) {
	Texture * texture;

	if (!PyArg_ParseTuple(args, "O!:SetTextureMipmapped", &TextureType, &texture)) {
		return 0;
	}

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR_MIPMAP_LINEAR);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	Py_RETURN_NONE;
}

PyObject * BuildMipmaps(PyObject * self, PyObject * args, PyObject * kwargs) {
	Texture * texture;
	int base = 0;
	int max = 1000;

	static const char * kwlist[] = {"texture", "base", "max", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|ii:BuildMipmaps", (char **)kwlist, &TextureType, &texture, &base, &max)) {
		return 0;
	}

	OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
	OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture->texture);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_BASE_LEVEL, base);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAX_LEVEL, max);
	OpenGL::glGenerateMipmap(OpenGL::GL_TEXTURE_2D);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR_MIPMAP_LINEAR);
	OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	Py_RETURN_NONE;
}

PyObject * UseTextureAsImage(PyObject * self, PyObject * args, PyObject * kwargs) {
	Texture * texture;
	int binding = 0;

	static const char * kwlist[] = {"texture", "binding", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|i:UseTextureAsImage", (char **)kwlist, &TextureType, &texture, &binding)) {
		return 0;
	}

	if (texture->floats) {
		const int formats[] = {0, OpenGL::GL_R8UI, OpenGL::GL_RG8UI, OpenGL::GL_RGB8UI, OpenGL::GL_RGBA8UI};
		int format = formats[texture->components];

		OpenGL::glBindImageTexture(binding, texture->texture, 0, false, 0, OpenGL::GL_READ_WRITE, format);
	} else {
		const int formats[] = {0, OpenGL::GL_R32F, OpenGL::GL_RG32F, OpenGL::GL_RGB32F, OpenGL::GL_RGBA32F};
		int format = formats[texture->components];

		OpenGL::glBindImageTexture(binding, texture->texture, 0, false, 0, OpenGL::GL_READ_WRITE, format);
	}

	Py_RETURN_NONE;
}


PyObject * Dummy_NewTexture(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewTexture() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewTexture() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UpdateTexture(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UpdateTexture() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UpdateTexture() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteTexture(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteTexture() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteTexture() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_BuildMipmaps(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "BuildMipmaps() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "BuildMipmaps() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UseTexture(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UseTexture() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UseTexture() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UseTextureAsImage(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UseTextureAsImage() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UseTextureAsImage() function not initialized. OpenGL 4.2 is required.");
	}
	return 0;
}

PyObject * Dummy_SetTextureFiltered(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "SetTextureFiltered() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "SetTextureFiltered() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_SetTextureMipmapped(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "SetTextureMipmapped() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "SetTextureMipmapped() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_SetTexturePixelated(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "SetTexturePixelated() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "SetTexturePixelated() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod TextureMethods[] = {
	{
		301,
		(PyCFunction)NewTexture,
		(PyCFunction)Dummy_NewTexture,
		METH_VARARGS | METH_KEYWORDS,
		"NewTexture",
		"Create a new texture.\n"
		"\n"

		"Parameters:\n"
		"\twidth (int) Width of the texture.\n"
		"\theight (int) Height of the texture.\n"
		"\tdata (bytes) Pixels stored in bytes.\n"
		"\tcomponents (int) Number of color channels. By default is 3\n"
		"\tfloats (bool) Single-precision floating-point format. By default is False\n"
		"\n"

		"Returns:\n"
		"\ttexture (ModernGL.Texture) The index of the new texture object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.RangeError) The size of pixels is different.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DeleteTexture,
		(PyCFunction)Dummy_DeleteTexture,
		METH_VARARGS,
		"DeleteTexture",
		"Delete a texture created by the ModernGL.NewTexture method.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture.\n"
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
		(PyCFunction)UpdateTexture,
		(PyCFunction)Dummy_UpdateTexture,
		METH_VARARGS | METH_KEYWORDS,
		"UpdateTexture",
		"Update the content of a texture.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture.\n"
		"\tdata (bytes) Pixels stored in bytes.\n"
		"\tx (int) Offset of the new texture part. By default is 0\n"
		"\ty (int) Offset of the new texture part. By default is 0\n"
		"\twidth (int) Width of the texture. By default is 0\n"
		"\theight (int) Height of the texture. By default is 0\n"
		"\tcomponents (int) By default is 3\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.RangeError) The size of pixels is different.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)UseTexture,
		(PyCFunction)Dummy_UseTexture,
		METH_VARARGS,
		"UseTexture",
		"Bind a texture to a location.\n"
		"The default location is 0.\n"
		"Initialize sampler2D uniforms with ModernGL.SetUniform\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture function.\n"
		"\tlocation (int) Location of the texture. By default is 0\n"
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
		(PyCFunction)SetTexturePixelated,
		(PyCFunction)Dummy_SetTexturePixelated,
		METH_VARARGS,
		"SetTexturePixelated",
		"Set texture filter to nearest.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture function.\n"
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
		(PyCFunction)SetTextureFiltered,
		(PyCFunction)Dummy_SetTextureFiltered,
		METH_VARARGS,
		"SetTextureFiltered",
		"Set texture filter to linear.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture function.\n"
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
		(PyCFunction)SetTextureMipmapped,
		(PyCFunction)Dummy_SetTextureMipmapped,
		METH_VARARGS,
		"SetTextureMipmapped",
		"Set texture filter to mipmap linear.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the ModernGL.NewTexture function.\n"
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
		(PyCFunction)BuildMipmaps,
		(PyCFunction)Dummy_BuildMipmaps,
		METH_VARARGS | METH_KEYWORDS,
		"BuildMipmaps",
		"Generate the mipmaps for the texture.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Index of a texture returned by the NewTexture function.\n"
		"\tbase (int) Base mipmap level to build.\n"
		"\tmax (int) Maximum mipmap level to build.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		402,
		(PyCFunction)UseTextureAsImage,
		(PyCFunction)Dummy_UseTextureAsImage,
		METH_VARARGS | METH_KEYWORDS,
		"UseTextureAsImage",
		"To use image2D instead of sampler2D.\n"
		"\n"

		"Parameters:\n"
		"\ttexture (ModernGL.Texture) Texture.\n"
		"\tbinding (int) Image binding specified by the layout in GLSL. By default is 0\n"
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

int NumTextureMethods = sizeof(TextureMethods) / sizeof(TextureMethods[0]);
