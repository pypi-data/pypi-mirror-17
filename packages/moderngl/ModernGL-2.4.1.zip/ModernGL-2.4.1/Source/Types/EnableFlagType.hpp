#pragma once

#include "Common.hpp"

struct EnableFlag {
	PyObject_HEAD
	unsigned value;
};

extern PyTypeObject EnableFlagType;

PyObject * CreateEnableFlagType(unsigned value);
