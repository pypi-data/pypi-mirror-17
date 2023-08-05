#include "Constants.hpp"

#include "Types.hpp"

PyObject * SCREEN;

#define STR_VERSION(ver) # ver

void RegisterConstants(PyObject * module) {
	SCREEN = CreateFramebufferType(0, 0, 0);

	PyModule_AddObject(module, "ENABLE_NOTHING", CreateEnableFlagType(ENABLE_NOTHING));
	PyModule_AddObject(module, "ENABLE_BLEND", CreateEnableFlagType(ENABLE_BLEND));
	PyModule_AddObject(module, "ENABLE_CULL_FACE", CreateEnableFlagType(ENABLE_CULL_FACE));
	PyModule_AddObject(module, "ENABLE_DEPTH_TEST", CreateEnableFlagType(ENABLE_DEPTH_TEST));
	PyModule_AddObject(module, "ENABLE_MULTISAMPLE", CreateEnableFlagType(ENABLE_MULTISAMPLE));
	PyModule_AddObject(module, "ENABLE_ALL", CreateEnableFlagType(ENABLE_ALL));

	PyModule_AddObject(module, "SCREEN", SCREEN);

	PyModule_AddStringConstant(module, "VERSION", STR_VERSION(MODERN_GL_VERSION));

	PyModule_AddStringConstant(module, "__AUTHOR_NAME__", "Szabolcs Dombi");
	PyModule_AddStringConstant(module, "__AUTHOR_EMAIL__", "cprogrammer1994@gmail.com");
}

#undef STR_VERSION
