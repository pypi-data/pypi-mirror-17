#include "Methods.hpp"

#include "Methods/Buffer.hpp"
#include "Methods/Compute.hpp"
#include "Methods/Core.hpp"
#include "Methods/Debug.hpp"
#include "Methods/Framebuffer.hpp"
#include "Methods/Initialize.hpp"
#include "Methods/Program.hpp"
#include "Methods/Render.hpp"
#include "Methods/Shader.hpp"
#include "Methods/Texture.hpp"
#include "Methods/Transform.hpp"
#include "Methods/VertexArray.hpp"

#include "Utils/PythonMethod.hpp"
#include "ModernGL.hpp"

PyMethodDef moduleMethod[1024];
PythonMethod implementation[1024];
int implementations;

void RegisterMethods(PythonMethod * method, int methods) {
	for (int i = 0; i < methods; ++i) {
		if (method[i].method) {
			implementation[implementations++] = method[i];
		}
	}
}

void InitMethods() {
	RegisterMethods(InitializeMethods, NumInitializeMethods);
	RegisterMethods(BufferMethods, NumBufferMethods);
	RegisterMethods(ComputeMethods, NumComputeMethods);
	RegisterMethods(CoreMethods, NumCoreMethods);
	RegisterMethods(DebugMethods, NumDebugMethods);
	RegisterMethods(FramebufferMethods, NumFramebufferMethods);
	RegisterMethods(ProgramMethods, NumProgramMethods);
	RegisterMethods(RenderMethods, NumRenderMethods);
	RegisterMethods(ShaderMethods, NumShaderMethods);
	RegisterMethods(TextureMethods, NumTextureMethods);
	RegisterMethods(TransformMethods, NumTransformMethods);
	RegisterMethods(VertexArrayMethods, NumVertexArrayMethods);

	#ifdef EXPERIMENTAL
	RegisterMethods(ExperimentalMethods, NumExperimentalMethods);
	#endif

	for (int i = 0; i < implementations; ++i) {
		moduleMethod[i].ml_name = (char *)implementation[i].name;
		moduleMethod[i].ml_doc = (char *)implementation[i].doc;
		moduleMethod[i].ml_flags = implementation[i].flags;
		moduleMethod[i].ml_meth = implementation[i].dummy;
	}
}

void LoadMethods() {
	for (int i = 0; i < implementations; ++i) {
		if (versionNumber >= implementation[i].version) {
			moduleMethod[i].ml_meth = implementation[i].method;
		}
	}
}
