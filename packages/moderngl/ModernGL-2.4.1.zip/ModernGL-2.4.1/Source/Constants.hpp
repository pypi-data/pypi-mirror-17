#pragma once

#include "Common.hpp"

const int ENABLE_NOTHING = 0x00;
const int ENABLE_BLEND = 0x01;
const int ENABLE_CULL_FACE = 0x02;
const int ENABLE_DEPTH_TEST = 0x04;
const int ENABLE_MULTISAMPLE = 0x08;
const int ENABLE_ALL = 0x0F;

extern PyObject * SCREEN;

void RegisterConstants(PyObject * module);
