#include "Transform.hpp"

#include "Types.hpp"
#include "Errors.hpp"
#include "ModernGL.hpp"
#include "Utils/OpenGL.hpp"

PyObject * TransformTriangles(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_TRIANGLES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_TRIANGLES, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_TRIANGLES, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformTriangleStrip(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_TRIANGLES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_TRIANGLE_STRIP, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_TRIANGLE_STRIP, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformTriangleFan(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_TRIANGLES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_TRIANGLE_FAN, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_TRIANGLE_FAN, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformLines(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_LINES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_LINES, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_LINES, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformLineStrip(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_LINES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_LINE_STRIP, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_LINE_STRIP, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformLineLoop(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_LINES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_LINE_LOOP, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_LINE_LOOP, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformPoints(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_POINTS);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_POINTS, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_POINTS, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformLineStripAdjacency(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_LINES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_LINE_STRIP_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_LINE_STRIP_ADJACENCY, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformLinesAdjacency(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_LINES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_LINES_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_LINES_ADJACENCY, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformTriangleStripAdjacency(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_TRIANGLES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_TRIANGLE_STRIP_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_TRIANGLE_STRIP_ADJACENCY, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}

PyObject * TransformTrianglesAdjacency(PyObject * self, PyObject * args, PyObject * kwargs) {
	VertexBuffer * vbo;
	VertexArray * vao;
	int count;
	int first = 0;

	static const char * kwlist[] = {"vao", "output", "count", "first", 0};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!O!i|i:RunTransformShader", (char **)kwlist, &VertexArrayType, &vao, &VertexBufferType, &vbo, &count, &first)) {
		return 0;
	}

	int activeProgram = 0;
	OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&activeProgram);
	if (activeProgram != vao->program) {
		OpenGL::glUseProgram(vao->program);
	}

	OpenGL::glBindVertexArray(vao->vao);
	OpenGL::glBindBufferBase(OpenGL::GL_TRANSFORM_FEEDBACK_BUFFER, 0, vbo->vbo);

	OpenGL::glEnable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glBeginTransformFeedback(OpenGL::GL_TRIANGLES);

	if (vao->indexed) {
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElements(OpenGL::GL_TRIANGLES_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr);
	} else {
		OpenGL::glDrawArrays(OpenGL::GL_TRIANGLES_ADJACENCY, first, count);
	}

	OpenGL::glEndTransformFeedback();
	OpenGL::glDisable(OpenGL::GL_RASTERIZER_DISCARD);
	OpenGL::glFlush();

	OpenGL::glBindVertexArray(defaultVertexArray);
	Py_RETURN_NONE;
}


PyObject * Dummy_TransformTriangles(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformTriangles() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformTriangles() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformTriangleStrip(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformTriangleStrip() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformTriangleStrip() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformTriangleFan(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformTriangleFan() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformTriangleFan() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformLines(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformLines() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformLines() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformLineStrip(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformLineStrip() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformLineStrip() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformLineLoop(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformLineLoop() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformLineLoop() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformPoints(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformPoints() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformPoints() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformLineStripAdjacency(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformLineStripAdjacency() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformLineStripAdjacency() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformLinesAdjacency(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformLinesAdjacency() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformLinesAdjacency() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformTriangleStripAdjacency(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformTriangleStripAdjacency() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformTriangleStripAdjacency() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}

PyObject * Dummy_TransformTrianglesAdjacency(PyObject * self) {
	if (!initialized) {
		PyErr_SetString(ModuleNotInitialized, "TransformTrianglesAdjacency() function not initialized.\n\nCall ModernGL.Init() first.\n\n");
	} else {
		PyErr_SetString(ModuleNotSupported, "TransformTrianglesAdjacency() function not initialized. OpenGL 3.1 is required.");
	}
	return 0;
}


PythonMethod TransformMethods[] = {
	{
		301,
		(PyCFunction)TransformTriangles,
		(PyCFunction)Dummy_TransformTriangles,
		METH_VARARGS | METH_KEYWORDS,
		"TransformTriangles",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformTriangleStrip,
		(PyCFunction)Dummy_TransformTriangleStrip,
		METH_VARARGS | METH_KEYWORDS,
		"TransformTriangleStrip",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformTriangleFan,
		(PyCFunction)Dummy_TransformTriangleFan,
		METH_VARARGS | METH_KEYWORDS,
		"TransformTriangleFan",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformLines,
		(PyCFunction)Dummy_TransformLines,
		METH_VARARGS | METH_KEYWORDS,
		"TransformLines",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformLineStrip,
		(PyCFunction)Dummy_TransformLineStrip,
		METH_VARARGS | METH_KEYWORDS,
		"TransformLineStrip",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformLineLoop,
		(PyCFunction)Dummy_TransformLineLoop,
		METH_VARARGS | METH_KEYWORDS,
		"TransformLineLoop",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
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
		(PyCFunction)TransformPoints,
		(PyCFunction)Dummy_TransformPoints,
		METH_VARARGS | METH_KEYWORDS,
		"TransformPoints",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		302,
		(PyCFunction)TransformLineStripAdjacency,
		(PyCFunction)Dummy_TransformLineStripAdjacency,
		METH_VARARGS | METH_KEYWORDS,
		"TransformLineStripAdjacency",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		302,
		(PyCFunction)TransformLinesAdjacency,
		(PyCFunction)Dummy_TransformLinesAdjacency,
		METH_VARARGS | METH_KEYWORDS,
		"TransformLinesAdjacency",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		302,
		(PyCFunction)TransformTriangleStripAdjacency,
		(PyCFunction)Dummy_TransformTriangleStripAdjacency,
		METH_VARARGS | METH_KEYWORDS,
		"TransformTriangleStripAdjacency",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
	{
		302,
		(PyCFunction)TransformTrianglesAdjacency,
		(PyCFunction)Dummy_TransformTrianglesAdjacency,
		METH_VARARGS | METH_KEYWORDS,
		"TransformTrianglesAdjacency",
		"\n"

		"Parameters:\n"
		"\tvao (ModernGL.VertexArray) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"
		"\n"

		"Returns:\n"
		"\tNone\n"
		"\n"

		"Errors:\n"
		"\t(ModernGL.NotInitialized) The module must be initialized first.\n"
		"\n"
	},
};

int NumTransformMethods = sizeof(TransformMethods) / sizeof(TransformMethods[0]);
