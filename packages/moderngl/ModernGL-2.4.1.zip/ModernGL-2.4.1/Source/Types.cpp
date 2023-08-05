#include "Types.hpp"

#include "Errors.hpp"

bool TypeReadyCheck() {
	if (PyType_Ready(&FramebufferType) < 0) {
		return false;
	}

	if (PyType_Ready(&VertexArrayType) < 0) {
		return false;
	}

	if (PyType_Ready(&VertexBufferType) < 0) {
		return false;
	}

	if (PyType_Ready(&IndexBufferType) < 0) {
		return false;
	}

	if (PyType_Ready(&UniformBufferType) < 0) {
		return false;
	}

	if (PyType_Ready(&StorageBufferType) < 0) {
		return false;
	}

	if (PyType_Ready(&TextureType) < 0) {
		return false;
	}

	if (PyType_Ready(&ShaderType) < 0) {
		return false;
	}

	if (PyType_Ready(&ProgramType) < 0) {
		return false;
	}

	if (PyType_Ready(&UniformLocationType) < 0) {
		return false;
	}

	if (PyType_Ready(&UniformBufferLocationType) < 0) {
		return false;
	}

	if (PyType_Ready(&ComputeShaderType) < 0) {
		return false;
	}

	if (PyType_Ready(&EnableFlagType) < 0) {
		return false;
	}

	return true;
}

void RegisterTypes(PyObject * module) {
	Py_INCREF(&FramebufferType);
	Py_INCREF(&VertexArrayType);
	Py_INCREF(&VertexBufferType);
	Py_INCREF(&IndexBufferType);
	Py_INCREF(&UniformBufferType);
	Py_INCREF(&StorageBufferType);
	Py_INCREF(&TextureType);
	Py_INCREF(&ShaderType);
	Py_INCREF(&ProgramType);
	Py_INCREF(&UniformLocationType);
	Py_INCREF(&UniformBufferLocationType);
	Py_INCREF(&ComputeShaderType);
	Py_INCREF(&EnableFlagType);

	PyModule_AddObject(module, "Framebuffer", (PyObject *)&FramebufferType);
	PyModule_AddObject(module, "VertexArray", (PyObject *)&VertexArrayType);
	PyModule_AddObject(module, "VertexBuffer", (PyObject *)&VertexBufferType);
	PyModule_AddObject(module, "IndexBuffer", (PyObject *)&IndexBufferType);
	PyModule_AddObject(module, "UniformBuffer", (PyObject *)&UniformBufferType);
	PyModule_AddObject(module, "StorageBuffer", (PyObject *)&StorageBufferType);
	PyModule_AddObject(module, "Texture", (PyObject *)&TextureType);
	PyModule_AddObject(module, "Shader", (PyObject *)&ShaderType);
	PyModule_AddObject(module, "Program", (PyObject *)&ProgramType);
	PyModule_AddObject(module, "UniformLocation", (PyObject *)&UniformLocationType);
	PyModule_AddObject(module, "UniformBufferLocation", (PyObject *)&UniformBufferLocationType);
	PyModule_AddObject(module, "ComputeShader", (PyObject *)&ComputeShaderType);
	PyModule_AddObject(module, "EnableFlag", (PyObject *)&EnableFlagType);
}
