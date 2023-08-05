#pragma once

#include "Common.hpp"

#include "Types/ComputeShaderType.hpp"
#include "Types/EnableFlagType.hpp"
#include "Types/FramebufferType.hpp"
#include "Types/IndexBufferType.hpp"
#include "Types/ProgramType.hpp"
#include "Types/ShaderType.hpp"
#include "Types/StorageBufferType.hpp"
#include "Types/TextureType.hpp"
#include "Types/UniformBufferLocationType.hpp"
#include "Types/UniformBufferType.hpp"
#include "Types/UniformLocationType.hpp"
#include "Types/VertexArrayType.hpp"
#include "Types/VertexBufferType.hpp"

bool TypeReadyCheck();
void RegisterTypes(PyObject * module);
