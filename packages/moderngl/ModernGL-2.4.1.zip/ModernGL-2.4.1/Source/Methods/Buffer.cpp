#include "Buffer.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * NewVertexBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	const void * data;
	int size;
	bool dynamic = false;

	static const char * kwlist[] = {"data", "dynamic", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y#|p:NewVertexBuffer", (char **)kwlist, &data, &size, &dynamic)) {
		return 0;
	}

	int vbo = 0;
	OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&vbo);
	OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, vbo);
	OpenGL::glBufferData(OpenGL::GL_ARRAY_BUFFER, size, data, dynamic ? OpenGL::GL_DYNAMIC_DRAW : OpenGL::GL_STATIC_DRAW);
	return CreateVertexBufferType(vbo, size);
}

PyObject * NewIndexBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	const void * data;
	int size;
	bool dynamic = false;

	static const char * kwlist[] = {"data", "dynamic", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y#|p:NewIndexBuffer", (char **)kwlist, &data, &size, &dynamic)) {
		return 0;
	}

	int ibo = 0;
	OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&ibo);
	OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, ibo);
	OpenGL::glBufferData(OpenGL::GL_ELEMENT_ARRAY_BUFFER, size, data, dynamic ? OpenGL::GL_DYNAMIC_DRAW : OpenGL::GL_STATIC_DRAW);
	return CreateIndexBufferType(ibo, size);
}

PyObject * NewUniformBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	const void * data;
	int size;
	bool dynamic = false;

	static const char * kwlist[] = {"data", "dynamic", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y#|p:NewUniformBuffer", (char **)kwlist, &data, &size, &dynamic)) {
		return 0;
	}

	int ubo = 0;
	OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&ubo);
	OpenGL::glBindBuffer(OpenGL::GL_UNIFORM_BUFFER, ubo);
	OpenGL::glBufferData(OpenGL::GL_UNIFORM_BUFFER, size, data, dynamic ? OpenGL::GL_DYNAMIC_DRAW : OpenGL::GL_STATIC_DRAW);
	return CreateUniformBufferType(ubo, size);
}

PyObject * NewStorageBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	const void * data;
	int size;
	bool dynamic = false;

	static const char * kwlist[] = {"data", "dynamic", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y#|p:NewStorageBuffer", (char **)kwlist, &data, &size, &dynamic)) {
		return 0;
	}

	int sbo = 0;
	OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&sbo);
	OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, sbo);
	OpenGL::glBufferData(OpenGL::GL_SHADER_STORAGE_BUFFER, size, data, dynamic ? OpenGL::GL_DYNAMIC_DRAW : OpenGL::GL_STATIC_DRAW);
	return CreateStorageBufferType(sbo, size);
}

PyObject * DeleteVertexBuffer(PyObject * self, PyObject * args) {
	VertexBuffer * vbo;

	if (!PyArg_ParseTuple(args, "O!:DeleteVertexBuffer", &VertexBufferType, &vbo)) {
		return 0;
	}

	OpenGL::glDeleteBuffers(1, (OpenGL::GLuint *)&vbo->vbo);
	Py_RETURN_NONE;
}

PyObject * DeleteIndexBuffer(PyObject * self, PyObject * args) {
	IndexBuffer * ibo;

	if (!PyArg_ParseTuple(args, "O!:DeleteIndexBuffer", &IndexBufferType, &ibo)) {
		return 0;
	}

	OpenGL::glDeleteBuffers(1, (OpenGL::GLuint *)&ibo->ibo);
	Py_RETURN_NONE;
}

PyObject * DeleteUniformBuffer(PyObject * self, PyObject * args) {
	UniformBuffer * ubo;

	if (!PyArg_ParseTuple(args, "O!:DeleteUniformBuffer", &UniformBufferType, &ubo)) {
		return 0;
	}

	OpenGL::glDeleteBuffers(1, (OpenGL::GLuint *)&ubo->ubo);
	Py_RETURN_NONE;
}

PyObject * DeleteStorageBuffer(PyObject * self, PyObject * args) {
	StorageBuffer * sbo;

	if (!PyArg_ParseTuple(args, "O!:DeleteStorageBuffer", &StorageBufferType, &sbo)) {
		return 0;
	}

	OpenGL::glDeleteBuffers(1, (OpenGL::GLuint *)&sbo->sbo);
	Py_RETURN_NONE;
}

PyObject * UpdateVertexBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	int offset;
	const void * data;
	int size;

	static const char * kwlist[] = {"vbo", "offset", "data", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!iy#:UpdateVertexBuffer", (char **)kwlist, &VertexBufferType, &vbo, &offset, &data, &size)) {
		return 0;
	}

	if (offset < 0 || offset + size > vbo->size) {
		PyErr_Format(ModuleRangeError, "UpdateVertexBuffer() data.offset = %d data.size = %d vbo.size = %d", offset, size, vbo->size);
	}

	OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, vbo->vbo);
	OpenGL::glBufferSubData(OpenGL::GL_ARRAY_BUFFER, (OpenGL::GLintptr)offset, size, data);
	Py_RETURN_NONE;
}

PyObject * UpdateIndexBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	IndexBuffer * ibo;
	int offset;
	const void * data;
	int size;

	static const char * kwlist[] = {"ibo", "offset", "data", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!iy#:UpdateIndexBuffer", (char **)kwlist, &IndexBufferType, &ibo, &offset, &data, &size)) {
		return 0;
	}

	if (offset < 0 || offset + size > ibo->size) {
		PyErr_Format(ModuleRangeError, "UpdateIndexBuffer() data.offset = %d data.size = %d ibo.size = %d", offset, size, ibo->size);
	}

	OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, ibo->ibo);
	OpenGL::glBufferSubData(OpenGL::GL_ELEMENT_ARRAY_BUFFER, (OpenGL::GLintptr)offset, size, data);
	Py_RETURN_NONE;
}

PyObject * UpdateUniformBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	UniformBuffer * ubo;
	int offset;
	const void * data;
	int size;

	static const char * kwlist[] = {"ubo", "offset", "data", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!iy#:UpdateUniformBuffer", (char **)kwlist, &UniformBufferType, &ubo, &offset, &data, &size)) {
		return 0;
	}

	if (offset < 0 || offset + size > ubo->size) {
		PyErr_Format(ModuleRangeError, "UpdateUniformBuffer() data.offset = %d data.size = %d ubo.size = %d", offset, size, ubo->size);
	}

	OpenGL::glBindBuffer(OpenGL::GL_UNIFORM_BUFFER, ubo->ubo);
	OpenGL::glBufferSubData(OpenGL::GL_UNIFORM_BUFFER, (OpenGL::GLintptr)offset, size, data);
	Py_RETURN_NONE;
}

PyObject * UpdateStorageBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	StorageBuffer * sbo;
	int offset;
	const void * data;
	int size;

	static const char * kwlist[] = {"sbo", "offset", "data", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!iy#:UpdateStorageBuffer", (char **)kwlist, &StorageBufferType, &sbo, &offset, &data, &size)) {
		return 0;
	}

	if (offset < 0 || offset + size > sbo->size) {
		PyErr_Format(ModuleRangeError, "UpdateStorageBuffer() data.offset = %d data.size = %d sbo.size = %d", offset, size, sbo->size);
	}

	OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, sbo->sbo);
	OpenGL::glBufferSubData(OpenGL::GL_SHADER_STORAGE_BUFFER, (OpenGL::GLintptr)offset, size, data);
	Py_RETURN_NONE;
}

PyObject * UseUniformBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	UniformBuffer * ubo;
	UniformBufferLocation * location;

	static const char * kwlist[] = {"ubo", "location", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!:UseUniformBuffer", (char **)kwlist, &UniformBufferType, &ubo, &UniformBufferLocationType, &location)) {
		return 0;
	}

	OpenGL::glBindBufferBase(OpenGL::GL_UNIFORM_BUFFER, location->location, ubo->ubo);
	Py_RETURN_NONE;
}

PyObject * UseStorageBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	StorageBuffer * sbo;
	int binding = 0;

	static const char * kwlist[] = {"sbo", "binding", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|i:UseStorageBuffer", (char **)kwlist, &StorageBufferType, &sbo, &binding)) {
		return 0;
	}

	OpenGL::glBindBufferBase(OpenGL::GL_SHADER_STORAGE_BUFFER, binding, sbo->sbo);
	Py_RETURN_NONE;
}

PyObject * ReadStorageBuffer(PyObject * self, PyObject * args, PyObject * kwargs) {
	StorageBuffer * sbo;
	int offset = 0;
	int size = 0;

	static const char * kwlist[] = {"sbo", "offset", "size", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|ii:ReadStorageBuffer", (char **)kwlist, &StorageBufferType, &sbo, &offset, &size)) {
		return 0;
	}

	if (size == 0) {
		size = sbo->size - offset;
	}

	if (offset < 0 || offset + size > sbo->size) {
		PyErr_Format(ModuleRangeError, "ReadStorageBuffer() data.offset = %d data.size = %d sbo.size = %d", offset, size, sbo->size);
	}

	OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, sbo->sbo);
	void * map = OpenGL::glMapBufferRange(OpenGL::GL_SHADER_STORAGE_BUFFER, offset, size, OpenGL::GL_MAP_READ_BIT);
	if (!map) {
		PyErr_SetString(ModuleError, "ReadStorageBuffer() cannot map the buffer");
		return 0;
	}

	PyObject * data = PyBytes_FromStringAndSize((const char *)map, size);

	OpenGL::glUnmapBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER);
	return data;
}


PyObject * Dummy_NewVertexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewVertexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewVertexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_NewIndexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewIndexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewIndexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_NewUniformBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewUniformBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewUniformBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_NewStorageBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewStorageBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewStorageBuffer() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteVertexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteVertexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteVertexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteIndexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteIndexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteIndexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteUniformBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteUniformBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteUniformBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteStorageBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteStorageBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteStorageBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UpdateVertexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UpdateVertexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UpdateVertexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UpdateUniformBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UpdateUniformBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UpdateUniformBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UpdateIndexBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UpdateIndexBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UpdateIndexBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UpdateStorageBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UpdateStorageBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UpdateStorageBuffer() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}

PyObject * Dummy_UseUniformBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UseUniformBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UseUniformBuffer() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_UseStorageBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "UseStorageBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "UseStorageBuffer() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}

PyObject * Dummy_ReadStorageBuffer(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "ReadStorageBuffer() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "ReadStorageBuffer() function not initialized. OpenGL 4.3 is required.");
	}
	return 0;
}


PythonMethod BufferMethods[] = {
	{
		301,
		(PyCFunction)NewVertexBuffer,
		(PyCFunction)Dummy_NewVertexBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"NewVertexBuffer",
		"Create a vertex buffer.\n"
		"\n"

		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"
		"\n"

		"Returns:\n"
		"\tvbo (ModernGL.VertexBuffer) The index of the new vertex buffer object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)NewIndexBuffer,
		(PyCFunction)Dummy_NewIndexBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"NewIndexBuffer",
		"Create an index buffer.\n"
		"\n"

		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"
		"\n"

		"Returns:\n"
		"\tibo (ModernGL.IndexBuffer) The index of the new index buffer object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)NewUniformBuffer,
		(PyCFunction)Dummy_NewUniformBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"NewUniformBuffer",
		"Create a uniform buffer.\n"
		"\n"

		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"
		"\n"

		"Returns:\n"
		"\tubo (int) The index of the new uniform buffer object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		403,
		(PyCFunction)NewStorageBuffer,
		(PyCFunction)Dummy_NewStorageBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"NewStorageBuffer",
		"Create a shader storage buffer.\n"
		"\n"

		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"
		"\n"

		"Returns:\n"
		"\tsbo (ModernGL.StorageBuffer) The index of the new shader storage buffer object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DeleteVertexBuffer,
		(PyCFunction)Dummy_DeleteVertexBuffer,
		METH_VARARGS,
		"DeleteVertexBuffer",
		"Delete a vertex buffer created by the ModernGL.NewVertexBuffer.\n"
		"\n"

		"Parameters:\n"
		"\tbuffer (int) The index of any buffer object except the framebuffer object.\n"
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
		(PyCFunction)DeleteIndexBuffer,
		(PyCFunction)Dummy_DeleteIndexBuffer,
		METH_VARARGS,
		"DeleteIndexBuffer",
		"Delete an index buffer created by the ModernGL.NewIndexBuffer.\n"
		"\n"

		"Parameters:\n"
		"\tbuffer (int) The index of any buffer object except the framebuffer object.\n"
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
		(PyCFunction)DeleteUniformBuffer,
		(PyCFunction)Dummy_DeleteUniformBuffer,
		METH_VARARGS,
		"DeleteUniformBuffer",
		"Delete a uniform buffer created by the ModernGL.NewUniformBuffer.\n"
		"\n"

		"Parameters:\n"
		"\tbuffer (int) The index of any buffer object except the framebuffer object.\n"
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
		(PyCFunction)DeleteStorageBuffer,
		(PyCFunction)Dummy_DeleteStorageBuffer,
		METH_VARARGS,
		"DeleteStorageBuffer",
		"Delete a shader storage buffer created by the ModernGL.NewStorageBuffer.\n"
		"\n"

		"Parameters:\n"
		"\tbuffer (int) The index of any buffer object except the framebuffer object.\n"
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
		(PyCFunction)UpdateVertexBuffer,
		(PyCFunction)Dummy_UpdateVertexBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UpdateVertexBuffer",
		"Update the content of the buffer.\n"
		"\n"

		"Parameters:\n"
		"\tbuffer (int) The index of a vertex buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.RangeError) The offset or size of data is out of the buffer bounds.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)UpdateIndexBuffer,
		(PyCFunction)Dummy_UpdateIndexBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UpdateIndexBuffer",
		"Update the content of the buffer.\n"
		"\n"

		"Parameters:\n"
		"\tibo (ModernGL.IndexBuffer) The index of an index buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.RangeError) The offset or size of data is out of the buffer bounds.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)UpdateUniformBuffer,
		(PyCFunction)Dummy_UpdateUniformBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UpdateUniformBuffer",
		"Update the content of the buffer.\n"
		"\n"

		"Parameters:\n"
		"\tubo (ModernGL.UniformBuffer) The index of a uniform buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.RangeError) The offset or size of data is out of the buffer bounds.\n"
		"\n"
	},
	{
		403,
		(PyCFunction)UpdateStorageBuffer,
		(PyCFunction)Dummy_UpdateStorageBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UpdateStorageBuffer",
		"Update the content of a shader storage buffer.\n"
		"\n"

		"Parameters:\n"
		"\tsbo (ModernGL.StorageBuffer) The index of a shader storage buffer object returned by the NewStorageBuffer.\n"
		"\toffset (int) The offset of the data in the buffer to update.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\t(ModernGL.RangeError) The offset or size of data is out of the buffer bounds.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)UseUniformBuffer,
		(PyCFunction)Dummy_UseUniformBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UseUniformBuffer",
		"Bind a unirom buffer to a location in the program.\n"
		"\n"

		"Parameters:\n"
		"\tubo (ModernGL.UniformBuffer) Index of a uniform buffer.\n"
		"\tlocation (ModernGL.UniformBufferLocation) Location of the uniform buffer.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		403,
		(PyCFunction)UseStorageBuffer,
		(PyCFunction)Dummy_UseStorageBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"UseStorageBuffer",
		"Bind a shader storage buffer to a location specified in the GLSL layout.\n"
		"\n"

		"Parameters:\n"
		"\tsbo (ModernGL.StorageBuffer) The index of a shader storage buffer object returned by the NewStorageBuffer.\n"
		"\tbinding (int) Buffer binding specified by the layout in GLSL. By default is 0\n"
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
		(PyCFunction)ReadStorageBuffer,
		(PyCFunction)Dummy_ReadStorageBuffer,
		METH_VARARGS | METH_KEYWORDS,
		"ReadStorageBuffer",
		"Read the content of a shader storage buffer.\n"
		"If the size parameter is 0 the remaining size will be used.\n"
		"\n"

		"Parameters:\n"
		"\tsbo (ModernGL.StorageBuffer) The index of a shader storage buffer object returned by the ModernGL.NewStorageBuffer.\n"
		"\toffset (int) The offset of the data in the buffer to read. By default is 0\n"
		"\tsize (int) The size of the data to read from the buffer. By default is 0\n"
		"\n"

		"Returns:\n"
		"\tdata (bytes) The content of the shader storage buffer.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.NotSupported) The OpenGL version is below the required.\n"
		"\t(ModernGL.RangeError) The offset or size is out of the buffer bounds.\n"
		"\n"
	},
};

int NumBufferMethods = sizeof(BufferMethods) / sizeof(BufferMethods[0]);
