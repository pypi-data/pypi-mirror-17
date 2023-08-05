#include "VertexArray.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"

#include "Utils/BufferFormat.hpp"
#include "Utils/OpenGL.hpp"

PyObject * NewVertexArray(PyObject * self, PyObject * args, PyObject * kwargs) {
	Program * program;
	VertexBuffer * vbo;
	const char * format;
	PyObject * attributes;

	IndexBuffer * no_ibo = (IndexBuffer *)Py_None;
	IndexBuffer * ibo = no_ibo;

	static const char * kwlist[] = {"program", "vbo", "format", "attributes", "ibo", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!sO!|O:NewVertexArray", (char **)kwlist, &ProgramType, &program, &VertexBufferType, &vbo, &format, &PyList_Type, &attributes, &ibo)) {
		return 0;
	}

	if (ibo != no_ibo) {
		if (!PyObject_TypeCheck((PyObject *)ibo, &IndexBufferType)) {
			PyErr_Format(PyExc_TypeError, "NewVertexArray() ibo must be IndexBufferType not %s", GET_OBJECT_TYPENAME(ibo));
			return 0;
		}
	}

	int count = (int)PyList_Size(attributes);

	FormatIterator it = FormatIterator(format);
	FormatInfo info = it.info();

	if (!info.valid) {
		PyErr_Format(ModuleInvalidFormat, "NewVertexArray() format is invalid");
		return 0;
	}

	if (info.nodes != count) {
		PyErr_Format(ModuleInvalidFormat, "NewVertexArray() format has %d nodes but there are %d attributes", info.nodes, count);
		return 0;
	}

	FormatIterator cit = FormatIterator(format);
	for (int i = 0; i < count; ++i) {
		const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
		int location = OpenGL::glGetAttribLocation(program->program, name);

		FormatNode * node = cit.next();
		while (!node->type) {
			node = cit.next();
		}
	
		if (location < 0) {
			PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` not found", name);
			return 0;
		}

		// int size = 0;
		// unsigned type = 0;
		// char tname[20];
		// OpenGL::glGetActiveAttrib(program->program, location, 20, 0, &size, &type, tname);
		// printf("%s\n", tname); // index != location

		// switch (type) {
		// 	case OpenGL::GL_INT:
		// 	case OpenGL::GL_FLOAT:
		// 	case OpenGL::GL_DOUBLE:
		// 		if (node->count != 1) {
		// 			PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` dimension mismatch %d != 1", name, node->count);
		// 			return 0;
		// 		}
		// 		break;

		// 	case OpenGL::GL_INT_VEC2:
		// 	case OpenGL::GL_FLOAT_VEC2:
		// 	case OpenGL::GL_DOUBLE_VEC2:
		// 		if (node->count != 2) {
		// 			PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` dimension mismatch %d != 2", name, node->count);
		// 			return 0;
		// 		}
		// 		break;

		// 	case OpenGL::GL_INT_VEC3:
		// 	case OpenGL::GL_FLOAT_VEC3:
		// 	case OpenGL::GL_DOUBLE_VEC3:
		// 		if (node->count != 3) {
		// 			PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` dimension mismatch %d != 3", name, node->count);
		// 			return 0;
		// 		}
		// 		break;

		// 	case OpenGL::GL_INT_VEC4:
		// 	case OpenGL::GL_FLOAT_VEC4:
		// 	case OpenGL::GL_DOUBLE_VEC4:
		// 		if (node->count != 4) {
		// 			PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` dimension mismatch %d != 4", name, node->count);
		// 			return 0;
		// 		}
		// 		break;

		// 	default:
		// 		PyErr_Format(ModuleAttributeNotFound, "NewVertexArray() attribute `%s` unsupported type", name);
		// 		return 0;
		// }
	}

	int vao = 0;
	OpenGL::glGenVertexArrays(1, (OpenGL::GLuint *)&vao);
	OpenGL::glBindVertexArray(vao);

	if (ibo != no_ibo) {
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, ibo->ibo);
	}

	OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, vbo->vbo);

	int i = 0;
	char * ptr = 0;
	while (FormatNode * node = it.next()) {
		if (node->type) {
			const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
			int location = OpenGL::glGetAttribLocation(program->program, name);
			OpenGL::glVertexAttribPointer(location, node->count, node->type, false, info.size, ptr);
			OpenGL::glEnableVertexAttribArray(location);
			++i;
		}
		ptr += node->count * node->size;
	}

	OpenGL::glBindVertexArray(defaultVertexArray);
	return CreateVertexArrayType(vao, program->program, ibo != no_ibo);
}

PyObject * NewAdvancedVertexArray(PyObject * self, PyObject * args, PyObject * kwargs) {
	PyErr_SetString(ModuleError, "Not implemented");
	return 0;

	Program * program;
	PyObject * content;

	IndexBuffer * no_ibo = (IndexBuffer *)Py_None;
	IndexBuffer * ibo = no_ibo;

	static const char * kwlist[] = {"program", "content", "ibo", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!|O!:NewAdvancedVertexArray", (char **)kwargs, &ProgramType, &program, &PyList_Type, &content, &IndexBufferType, &ibo)) {
		return 0;
	}

	// TODO: upgrade

	int vao = 0;
	OpenGL::glGenVertexArrays(1, (OpenGL::GLuint *)&vao);
	OpenGL::glBindVertexArray(vao);

	if (ibo != no_ibo) {
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, ibo->ibo);
	}

	int size = PyList_Size(content);
	for (int k = 0; k < size; ++k) {
		PyObject * tuple = PyList_GET_ITEM(content, k);
		CHECK_AND_REPORT_ELEMENT_TYPE_ERROR("content", tuple, PyTuple_Type, k);
		if (PyTuple_Size(tuple) != 3) {
			PyErr_Format(PyExc_TypeError, "NewAdvancedVertexArray() fail");
			return 0;
		}

		VertexBuffer * vbo = (VertexBuffer *)PyTuple_GET_ITEM(tuple, 0);
		const char * format = PyUnicode_AsUTF8(PyTuple_GET_ITEM(tuple, 1));
		PyObject * attributes = PyTuple_GET_ITEM(tuple, 2);

		if (!CHECK_TYPE_ERROR(vbo, VertexBufferType)) {
			PyErr_Format(PyExc_TypeError, "NewAdvancedVertexArray() fail");
			return 0;
		}

		if (!CHECK_TYPE_ERROR(attributes, PyList_Type)) {
			PyErr_Format(PyExc_TypeError, "NewAdvancedVertexArray() fail");
			return 0;
		}

		int length = 0;
		while (format[length]) {
			if (length % 2 == 0) {
				if (format[length] < '1' || format[length] > '4') {
					PyErr_SetString(ModuleInvalidFormat, "NewAdvancedVertexArray() ERR 3");
					return 0;
				}
			} else {
				if (format[length] != 'i' && format[length] != 'f') {
					PyErr_SetString(ModuleInvalidFormat, "NewAdvancedVertexArray() ERR 3");
					return 0;
				}
			}
			++length;
		}

		if (!length || length % 2) {
			PyErr_SetString(ModuleInvalidFormat, "NewAdvancedVertexArray() ERR 3");
			return 0;
		}

		int stride = 0;
		for (int i = 0; format[i]; i += 2) {
			stride += (format[i] - '0') * 4;
		}

		int count = (int)PyList_Size(attributes);
		if (length / 2 != count) {
			PyErr_Format(ModuleInvalidFormat, "NewAdvancedVertexArray() ERR 4.");
			return 0;
		}

		char * ptr = 0;
		for (int i = 0; i < count; ++i) {
			const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
			int location = OpenGL::glGetAttribLocation(program->program, name);

			int dimension = format[i * 2] - '0';
			switch (format[i * 2 + 1]) {
				case 'f':
					OpenGL::glVertexAttribPointer(location, dimension, OpenGL::GL_FLOAT, false, stride, ptr);
					break;
				case 'i':
					OpenGL::glVertexAttribPointer(location, dimension, OpenGL::GL_INT, false, stride, ptr);
					break;
			}
			OpenGL::glEnableVertexAttribArray(location);
			ptr += dimension * 4;
		}
	}

	OpenGL::glBindVertexArray(defaultVertexArray);
	return CreateVertexArrayType(vao, program->program, ibo != no_ibo);
}

PyObject * DeleteVertexArray(PyObject * self, PyObject * args) {
	VertexArray * vao;

	if (!PyArg_ParseTuple(args, "O!:DeleteVertexArray", &VertexArrayType, &vao)) {
		return 0;
	}

	OpenGL::glDeleteVertexArrays(1, (OpenGL::GLuint *)&vao->vao);
	Py_RETURN_NONE;
}

PyObject * EnableAttributes(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexArray * vao;
	PyObject * attributes;
	bool strict = false;

	static const char * kwlist[] = {"vao", "attributes", "strict", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!|p:EnableAttributes", (char **)kwlist, &VertexArrayType, &vao, &PyList_Type, &attributes, &strict)) {
		return 0;
	}

	int count = (int)PyList_Size(attributes);
	for (int i = 0; i < count; ++i) {
		const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
		int location = OpenGL::glGetAttribLocation(vao->vao, name);
		if (strict && location < 0) {
			PyErr_Format(ModuleError, "ERR: 1");
			return 0;
		}
	}

	OpenGL::glBindVertexArray(vao->vao);
	for (int i = 0; i < count; ++i) {
		const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
		int location = OpenGL::glGetAttribLocation(vao->program, name);
		OpenGL::glEnableVertexAttribArray(location);
	}

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * DisableAttributes(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexArray * vao;
	PyObject * attributes;
	bool strict = false;

	static const char * kwlist[] = {"vao", "attributes", "strict", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!|p:DisableAttributes", (char **)kwlist, &VertexArrayType, &vao, &PyList_Type, &attributes, &strict)) {
		return 0;
	}

	int count = (int)PyList_Size(attributes);
	for (int i = 0; i < count; ++i) {
		const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
		int location = OpenGL::glGetAttribLocation(vao->program, name);
		if (strict && location < 0) {
			PyErr_Format(ModuleError, "ERR: 1");
			return 0;
		}
	}

	OpenGL::glBindVertexArray(vao->vao);
	for (int i = 0; i < count; ++i) {
		const char * name = PyUnicode_AsUTF8(PyList_GET_ITEM(attributes, i));
		int location = OpenGL::glGetAttribLocation(vao->program, name);
		OpenGL::glDisableVertexAttribArray(location);
	}

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}


PyObject * Dummy_NewVertexArray(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewVertexArray() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewVertexArray() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_NewAdvancedVertexArray(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "NewAdvancedVertexArray() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "NewAdvancedVertexArray() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DeleteVertexArray(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DeleteVertexArray() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DeleteVertexArray() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_EnableAttributes(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "EnableAttributes() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "EnableAttributes() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_DisableAttributes(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "DisableAttributes() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "DisableAttributes() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod VertexArrayMethods[] = {
	{
		301,
		(PyCFunction)NewVertexArray,
		(PyCFunction)Dummy_NewVertexArray,
		METH_VARARGS | METH_KEYWORDS,
		"NewVertexArray",
		"Create a vertex array object.\n"
		"Prepare vertex and index buffers for rendering. enable or disable attributes.\n"
		"To use more than one vertex buffer call the ModernGL.NewAdvancedVertexArray method.\n"
		"The format regex is: ([1-4][if])+\n"
		"\n"

		"Parameters:\n"
		"\tprogram (ModernGL.Program) A program object that will be used for rendering.\n"
		"\tvbo (ModernGL.VertexBuffer) A buffer containing data for the vertex attributes.\n"
		"\tformat (str) Format of the vertex array attrubites. ([1-4][if])+\n"
		"\tattributes (list) List of vertex attribute names.\n"
		"\tibo (ModernGL.IndexBuffer) Index of an index buffer object. By default is None\n"
		"\tstrict (bool) Enable AttributeNotFound error. By default is True\n"
		"\n"

		"Returns:\n"
		"\tvao (ModernGL.VertexArray) The index of the new vertex array object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\t(ModernGL.InvalidFormat) The format is invalid or the size of attributes is different.\n"
		"\t(ModernGL.AttributeNotFound) The attribute is missing (only strict enabled).\n"
		"\n"
	},
	{
		301,
		(PyCFunction)NewAdvancedVertexArray,
		(PyCFunction)Dummy_NewAdvancedVertexArray,
		METH_VARARGS,
		"NewAdvancedVertexArray",
		"Advanced version of NewVertexArray that can handle multiple VertexBuffer objects.\n"
		"\n"

		"Parameters:\n"
		"\tprogram (ModernGL.Program) A program object that will be used for rendering.\n"
		"\tcontent (list) List of tuples similar to the ModernGL.NewVertexArray parameters.\n"
		"\tibo (ModernGL.IndexBuffer) Index of an index buffer object. By default is None\n"
		"\tstrict (bool) Enable AttributeNotFound error. By default is True\n"
		"\n"

		"Returns:\n"
		"\tvao (ModernGL.VertexArray) The index of the new vertex array object.\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		301,
		(PyCFunction)DeleteVertexArray,
		(PyCFunction)Dummy_DeleteVertexArray,
		METH_VARARGS,
		"DeleteVertexArray",
		"\n"
		""
		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of the new vertex array object.\n"
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
		(PyCFunction)EnableAttributes,
		(PyCFunction)Dummy_EnableAttributes,
		METH_VARARGS | METH_KEYWORDS,
		"EnableAttributes",
		"Enable attributes in the vertex array object.\n"
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object.\n"
		"\tattribs (list) The names of the vertex attributes.\n"
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
		(PyCFunction)DisableAttributes,
		(PyCFunction)Dummy_DisableAttributes,
		METH_VARARGS | METH_KEYWORDS,
		"DisableAttributes",
		"Disable attributes in the vertex array object.\n"
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object.\n"
		"\tattribs (list) The names of the vertex attributes.\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
};

int NumVertexArrayMethods = sizeof(VertexArrayMethods) / sizeof(VertexArrayMethods[0]);
