#include "OpenGL.hpp"

namespace OpenGL {

	const void * GetOpenGLFunction(const char * name);

	bool LoadCoreOpenGLFunctions() {

		glCullFace = (PROC_glCullFace)GetOpenGLFunction("glCullFace");
		glFrontFace = (PROC_glFrontFace)GetOpenGLFunction("glFrontFace");
		glHint = (PROC_glHint)GetOpenGLFunction("glHint");
		glLineWidth = (PROC_glLineWidth)GetOpenGLFunction("glLineWidth");
		glPointSize = (PROC_glPointSize)GetOpenGLFunction("glPointSize");
		glPolygonMode = (PROC_glPolygonMode)GetOpenGLFunction("glPolygonMode");
		glScissor = (PROC_glScissor)GetOpenGLFunction("glScissor");
		glTexParameterf = (PROC_glTexParameterf)GetOpenGLFunction("glTexParameterf");
		glTexParameterfv = (PROC_glTexParameterfv)GetOpenGLFunction("glTexParameterfv");
		glTexParameteri = (PROC_glTexParameteri)GetOpenGLFunction("glTexParameteri");
		glTexParameteriv = (PROC_glTexParameteriv)GetOpenGLFunction("glTexParameteriv");
		glTexImage1D = (PROC_glTexImage1D)GetOpenGLFunction("glTexImage1D");
		glTexImage2D = (PROC_glTexImage2D)GetOpenGLFunction("glTexImage2D");
		glDrawBuffer = (PROC_glDrawBuffer)GetOpenGLFunction("glDrawBuffer");
		glClear = (PROC_glClear)GetOpenGLFunction("glClear");
		glClearColor = (PROC_glClearColor)GetOpenGLFunction("glClearColor");
		glClearStencil = (PROC_glClearStencil)GetOpenGLFunction("glClearStencil");
		glClearDepth = (PROC_glClearDepth)GetOpenGLFunction("glClearDepth");
		glStencilMask = (PROC_glStencilMask)GetOpenGLFunction("glStencilMask");
		glColorMask = (PROC_glColorMask)GetOpenGLFunction("glColorMask");
		glDepthMask = (PROC_glDepthMask)GetOpenGLFunction("glDepthMask");
		glDisable = (PROC_glDisable)GetOpenGLFunction("glDisable");
		glEnable = (PROC_glEnable)GetOpenGLFunction("glEnable");
		glFinish = (PROC_glFinish)GetOpenGLFunction("glFinish");
		glFlush = (PROC_glFlush)GetOpenGLFunction("glFlush");
		glBlendFunc = (PROC_glBlendFunc)GetOpenGLFunction("glBlendFunc");
		glLogicOp = (PROC_glLogicOp)GetOpenGLFunction("glLogicOp");
		glStencilFunc = (PROC_glStencilFunc)GetOpenGLFunction("glStencilFunc");
		glStencilOp = (PROC_glStencilOp)GetOpenGLFunction("glStencilOp");
		glDepthFunc = (PROC_glDepthFunc)GetOpenGLFunction("glDepthFunc");
		glPixelStoref = (PROC_glPixelStoref)GetOpenGLFunction("glPixelStoref");
		glPixelStorei = (PROC_glPixelStorei)GetOpenGLFunction("glPixelStorei");
		glReadBuffer = (PROC_glReadBuffer)GetOpenGLFunction("glReadBuffer");
		glReadPixels = (PROC_glReadPixels)GetOpenGLFunction("glReadPixels");
		glGetBooleanv = (PROC_glGetBooleanv)GetOpenGLFunction("glGetBooleanv");
		glGetDoublev = (PROC_glGetDoublev)GetOpenGLFunction("glGetDoublev");
		glGetError = (PROC_glGetError)GetOpenGLFunction("glGetError");
		glGetFloatv = (PROC_glGetFloatv)GetOpenGLFunction("glGetFloatv");
		glGetIntegerv = (PROC_glGetIntegerv)GetOpenGLFunction("glGetIntegerv");
		glGetString = (PROC_glGetString)GetOpenGLFunction("glGetString");
		glGetTexImage = (PROC_glGetTexImage)GetOpenGLFunction("glGetTexImage");
		glGetTexParameterfv = (PROC_glGetTexParameterfv)GetOpenGLFunction("glGetTexParameterfv");
		glGetTexParameteriv = (PROC_glGetTexParameteriv)GetOpenGLFunction("glGetTexParameteriv");
		glGetTexLevelParameterfv = (PROC_glGetTexLevelParameterfv)GetOpenGLFunction("glGetTexLevelParameterfv");
		glGetTexLevelParameteriv = (PROC_glGetTexLevelParameteriv)GetOpenGLFunction("glGetTexLevelParameteriv");
		glIsEnabled = (PROC_glIsEnabled)GetOpenGLFunction("glIsEnabled");
		glDepthRange = (PROC_glDepthRange)GetOpenGLFunction("glDepthRange");
		glViewport = (PROC_glViewport)GetOpenGLFunction("glViewport");
		glDrawArrays = (PROC_glDrawArrays)GetOpenGLFunction("glDrawArrays");
		glDrawElements = (PROC_glDrawElements)GetOpenGLFunction("glDrawElements");
		glGetPointerv = (PROC_glGetPointerv)GetOpenGLFunction("glGetPointerv");
		glPolygonOffset = (PROC_glPolygonOffset)GetOpenGLFunction("glPolygonOffset");
		glCopyTexImage1D = (PROC_glCopyTexImage1D)GetOpenGLFunction("glCopyTexImage1D");
		glCopyTexImage2D = (PROC_glCopyTexImage2D)GetOpenGLFunction("glCopyTexImage2D");
		glCopyTexSubImage1D = (PROC_glCopyTexSubImage1D)GetOpenGLFunction("glCopyTexSubImage1D");
		glCopyTexSubImage2D = (PROC_glCopyTexSubImage2D)GetOpenGLFunction("glCopyTexSubImage2D");
		glTexSubImage1D = (PROC_glTexSubImage1D)GetOpenGLFunction("glTexSubImage1D");
		glTexSubImage2D = (PROC_glTexSubImage2D)GetOpenGLFunction("glTexSubImage2D");
		glBindTexture = (PROC_glBindTexture)GetOpenGLFunction("glBindTexture");
		glDeleteTextures = (PROC_glDeleteTextures)GetOpenGLFunction("glDeleteTextures");
		glGenTextures = (PROC_glGenTextures)GetOpenGLFunction("glGenTextures");
		glIsTexture = (PROC_glIsTexture)GetOpenGLFunction("glIsTexture");
		glDrawRangeElements = (PROC_glDrawRangeElements)GetOpenGLFunction("glDrawRangeElements");
		glTexImage3D = (PROC_glTexImage3D)GetOpenGLFunction("glTexImage3D");
		glTexSubImage3D = (PROC_glTexSubImage3D)GetOpenGLFunction("glTexSubImage3D");
		glCopyTexSubImage3D = (PROC_glCopyTexSubImage3D)GetOpenGLFunction("glCopyTexSubImage3D");
		glActiveTexture = (PROC_glActiveTexture)GetOpenGLFunction("glActiveTexture");
		glSampleCoverage = (PROC_glSampleCoverage)GetOpenGLFunction("glSampleCoverage");
		glCompressedTexImage3D = (PROC_glCompressedTexImage3D)GetOpenGLFunction("glCompressedTexImage3D");
		glCompressedTexImage2D = (PROC_glCompressedTexImage2D)GetOpenGLFunction("glCompressedTexImage2D");
		glCompressedTexImage1D = (PROC_glCompressedTexImage1D)GetOpenGLFunction("glCompressedTexImage1D");
		glCompressedTexSubImage3D = (PROC_glCompressedTexSubImage3D)GetOpenGLFunction("glCompressedTexSubImage3D");
		glCompressedTexSubImage2D = (PROC_glCompressedTexSubImage2D)GetOpenGLFunction("glCompressedTexSubImage2D");
		glCompressedTexSubImage1D = (PROC_glCompressedTexSubImage1D)GetOpenGLFunction("glCompressedTexSubImage1D");
		glGetCompressedTexImage = (PROC_glGetCompressedTexImage)GetOpenGLFunction("glGetCompressedTexImage");
		glBlendFuncSeparate = (PROC_glBlendFuncSeparate)GetOpenGLFunction("glBlendFuncSeparate");
		glMultiDrawArrays = (PROC_glMultiDrawArrays)GetOpenGLFunction("glMultiDrawArrays");
		glMultiDrawElements = (PROC_glMultiDrawElements)GetOpenGLFunction("glMultiDrawElements");
		glPointParameterf = (PROC_glPointParameterf)GetOpenGLFunction("glPointParameterf");
		glPointParameterfv = (PROC_glPointParameterfv)GetOpenGLFunction("glPointParameterfv");
		glPointParameteri = (PROC_glPointParameteri)GetOpenGLFunction("glPointParameteri");
		glPointParameteriv = (PROC_glPointParameteriv)GetOpenGLFunction("glPointParameteriv");
		glBlendColor = (PROC_glBlendColor)GetOpenGLFunction("glBlendColor");
		glBlendEquation = (PROC_glBlendEquation)GetOpenGLFunction("glBlendEquation");
		glGenQueries = (PROC_glGenQueries)GetOpenGLFunction("glGenQueries");
		glDeleteQueries = (PROC_glDeleteQueries)GetOpenGLFunction("glDeleteQueries");
		glIsQuery = (PROC_glIsQuery)GetOpenGLFunction("glIsQuery");
		glBeginQuery = (PROC_glBeginQuery)GetOpenGLFunction("glBeginQuery");
		glEndQuery = (PROC_glEndQuery)GetOpenGLFunction("glEndQuery");
		glGetQueryiv = (PROC_glGetQueryiv)GetOpenGLFunction("glGetQueryiv");
		glGetQueryObjectiv = (PROC_glGetQueryObjectiv)GetOpenGLFunction("glGetQueryObjectiv");
		glGetQueryObjectuiv = (PROC_glGetQueryObjectuiv)GetOpenGLFunction("glGetQueryObjectuiv");
		glBindBuffer = (PROC_glBindBuffer)GetOpenGLFunction("glBindBuffer");
		glDeleteBuffers = (PROC_glDeleteBuffers)GetOpenGLFunction("glDeleteBuffers");
		glGenBuffers = (PROC_glGenBuffers)GetOpenGLFunction("glGenBuffers");
		glIsBuffer = (PROC_glIsBuffer)GetOpenGLFunction("glIsBuffer");
		glBufferData = (PROC_glBufferData)GetOpenGLFunction("glBufferData");
		glBufferSubData = (PROC_glBufferSubData)GetOpenGLFunction("glBufferSubData");
		glGetBufferSubData = (PROC_glGetBufferSubData)GetOpenGLFunction("glGetBufferSubData");
		glMapBuffer = (PROC_glMapBuffer)GetOpenGLFunction("glMapBuffer");
		glUnmapBuffer = (PROC_glUnmapBuffer)GetOpenGLFunction("glUnmapBuffer");
		glGetBufferParameteriv = (PROC_glGetBufferParameteriv)GetOpenGLFunction("glGetBufferParameteriv");
		glGetBufferPointerv = (PROC_glGetBufferPointerv)GetOpenGLFunction("glGetBufferPointerv");
		glBlendEquationSeparate = (PROC_glBlendEquationSeparate)GetOpenGLFunction("glBlendEquationSeparate");
		glDrawBuffers = (PROC_glDrawBuffers)GetOpenGLFunction("glDrawBuffers");
		glStencilOpSeparate = (PROC_glStencilOpSeparate)GetOpenGLFunction("glStencilOpSeparate");
		glStencilFuncSeparate = (PROC_glStencilFuncSeparate)GetOpenGLFunction("glStencilFuncSeparate");
		glStencilMaskSeparate = (PROC_glStencilMaskSeparate)GetOpenGLFunction("glStencilMaskSeparate");
		glAttachShader = (PROC_glAttachShader)GetOpenGLFunction("glAttachShader");
		glBindAttribLocation = (PROC_glBindAttribLocation)GetOpenGLFunction("glBindAttribLocation");
		glCompileShader = (PROC_glCompileShader)GetOpenGLFunction("glCompileShader");
		glCreateProgram = (PROC_glCreateProgram)GetOpenGLFunction("glCreateProgram");
		glCreateShader = (PROC_glCreateShader)GetOpenGLFunction("glCreateShader");
		glDeleteProgram = (PROC_glDeleteProgram)GetOpenGLFunction("glDeleteProgram");
		glDeleteShader = (PROC_glDeleteShader)GetOpenGLFunction("glDeleteShader");
		glDetachShader = (PROC_glDetachShader)GetOpenGLFunction("glDetachShader");
		glDisableVertexAttribArray = (PROC_glDisableVertexAttribArray)GetOpenGLFunction("glDisableVertexAttribArray");
		glEnableVertexAttribArray = (PROC_glEnableVertexAttribArray)GetOpenGLFunction("glEnableVertexAttribArray");
		glGetActiveAttrib = (PROC_glGetActiveAttrib)GetOpenGLFunction("glGetActiveAttrib");
		glGetActiveUniform = (PROC_glGetActiveUniform)GetOpenGLFunction("glGetActiveUniform");
		glGetAttachedShaders = (PROC_glGetAttachedShaders)GetOpenGLFunction("glGetAttachedShaders");
		glGetAttribLocation = (PROC_glGetAttribLocation)GetOpenGLFunction("glGetAttribLocation");
		glGetProgramiv = (PROC_glGetProgramiv)GetOpenGLFunction("glGetProgramiv");
		glGetProgramInfoLog = (PROC_glGetProgramInfoLog)GetOpenGLFunction("glGetProgramInfoLog");
		glGetShaderiv = (PROC_glGetShaderiv)GetOpenGLFunction("glGetShaderiv");
		glGetShaderInfoLog = (PROC_glGetShaderInfoLog)GetOpenGLFunction("glGetShaderInfoLog");
		glGetShaderSource = (PROC_glGetShaderSource)GetOpenGLFunction("glGetShaderSource");
		glGetUniformLocation = (PROC_glGetUniformLocation)GetOpenGLFunction("glGetUniformLocation");
		glGetUniformfv = (PROC_glGetUniformfv)GetOpenGLFunction("glGetUniformfv");
		glGetUniformiv = (PROC_glGetUniformiv)GetOpenGLFunction("glGetUniformiv");
		glGetVertexAttribdv = (PROC_glGetVertexAttribdv)GetOpenGLFunction("glGetVertexAttribdv");
		glGetVertexAttribfv = (PROC_glGetVertexAttribfv)GetOpenGLFunction("glGetVertexAttribfv");
		glGetVertexAttribiv = (PROC_glGetVertexAttribiv)GetOpenGLFunction("glGetVertexAttribiv");
		glGetVertexAttribPointerv = (PROC_glGetVertexAttribPointerv)GetOpenGLFunction("glGetVertexAttribPointerv");
		glIsProgram = (PROC_glIsProgram)GetOpenGLFunction("glIsProgram");
		glIsShader = (PROC_glIsShader)GetOpenGLFunction("glIsShader");
		glLinkProgram = (PROC_glLinkProgram)GetOpenGLFunction("glLinkProgram");
		glShaderSource = (PROC_glShaderSource)GetOpenGLFunction("glShaderSource");
		glUseProgram = (PROC_glUseProgram)GetOpenGLFunction("glUseProgram");
		glUniform1f = (PROC_glUniform1f)GetOpenGLFunction("glUniform1f");
		glUniform2f = (PROC_glUniform2f)GetOpenGLFunction("glUniform2f");
		glUniform3f = (PROC_glUniform3f)GetOpenGLFunction("glUniform3f");
		glUniform4f = (PROC_glUniform4f)GetOpenGLFunction("glUniform4f");
		glUniform1i = (PROC_glUniform1i)GetOpenGLFunction("glUniform1i");
		glUniform2i = (PROC_glUniform2i)GetOpenGLFunction("glUniform2i");
		glUniform3i = (PROC_glUniform3i)GetOpenGLFunction("glUniform3i");
		glUniform4i = (PROC_glUniform4i)GetOpenGLFunction("glUniform4i");
		glUniform1fv = (PROC_glUniform1fv)GetOpenGLFunction("glUniform1fv");
		glUniform2fv = (PROC_glUniform2fv)GetOpenGLFunction("glUniform2fv");
		glUniform3fv = (PROC_glUniform3fv)GetOpenGLFunction("glUniform3fv");
		glUniform4fv = (PROC_glUniform4fv)GetOpenGLFunction("glUniform4fv");
		glUniform1iv = (PROC_glUniform1iv)GetOpenGLFunction("glUniform1iv");
		glUniform2iv = (PROC_glUniform2iv)GetOpenGLFunction("glUniform2iv");
		glUniform3iv = (PROC_glUniform3iv)GetOpenGLFunction("glUniform3iv");
		glUniform4iv = (PROC_glUniform4iv)GetOpenGLFunction("glUniform4iv");
		glUniformMatrix2fv = (PROC_glUniformMatrix2fv)GetOpenGLFunction("glUniformMatrix2fv");
		glUniformMatrix3fv = (PROC_glUniformMatrix3fv)GetOpenGLFunction("glUniformMatrix3fv");
		glUniformMatrix4fv = (PROC_glUniformMatrix4fv)GetOpenGLFunction("glUniformMatrix4fv");
		glValidateProgram = (PROC_glValidateProgram)GetOpenGLFunction("glValidateProgram");
		glVertexAttrib1d = (PROC_glVertexAttrib1d)GetOpenGLFunction("glVertexAttrib1d");
		glVertexAttrib1dv = (PROC_glVertexAttrib1dv)GetOpenGLFunction("glVertexAttrib1dv");
		glVertexAttrib1f = (PROC_glVertexAttrib1f)GetOpenGLFunction("glVertexAttrib1f");
		glVertexAttrib1fv = (PROC_glVertexAttrib1fv)GetOpenGLFunction("glVertexAttrib1fv");
		glVertexAttrib1s = (PROC_glVertexAttrib1s)GetOpenGLFunction("glVertexAttrib1s");
		glVertexAttrib1sv = (PROC_glVertexAttrib1sv)GetOpenGLFunction("glVertexAttrib1sv");
		glVertexAttrib2d = (PROC_glVertexAttrib2d)GetOpenGLFunction("glVertexAttrib2d");
		glVertexAttrib2dv = (PROC_glVertexAttrib2dv)GetOpenGLFunction("glVertexAttrib2dv");
		glVertexAttrib2f = (PROC_glVertexAttrib2f)GetOpenGLFunction("glVertexAttrib2f");
		glVertexAttrib2fv = (PROC_glVertexAttrib2fv)GetOpenGLFunction("glVertexAttrib2fv");
		glVertexAttrib2s = (PROC_glVertexAttrib2s)GetOpenGLFunction("glVertexAttrib2s");
		glVertexAttrib2sv = (PROC_glVertexAttrib2sv)GetOpenGLFunction("glVertexAttrib2sv");
		glVertexAttrib3d = (PROC_glVertexAttrib3d)GetOpenGLFunction("glVertexAttrib3d");
		glVertexAttrib3dv = (PROC_glVertexAttrib3dv)GetOpenGLFunction("glVertexAttrib3dv");
		glVertexAttrib3f = (PROC_glVertexAttrib3f)GetOpenGLFunction("glVertexAttrib3f");
		glVertexAttrib3fv = (PROC_glVertexAttrib3fv)GetOpenGLFunction("glVertexAttrib3fv");
		glVertexAttrib3s = (PROC_glVertexAttrib3s)GetOpenGLFunction("glVertexAttrib3s");
		glVertexAttrib3sv = (PROC_glVertexAttrib3sv)GetOpenGLFunction("glVertexAttrib3sv");
		glVertexAttrib4Nbv = (PROC_glVertexAttrib4Nbv)GetOpenGLFunction("glVertexAttrib4Nbv");
		glVertexAttrib4Niv = (PROC_glVertexAttrib4Niv)GetOpenGLFunction("glVertexAttrib4Niv");
		glVertexAttrib4Nsv = (PROC_glVertexAttrib4Nsv)GetOpenGLFunction("glVertexAttrib4Nsv");
		glVertexAttrib4Nub = (PROC_glVertexAttrib4Nub)GetOpenGLFunction("glVertexAttrib4Nub");
		glVertexAttrib4Nubv = (PROC_glVertexAttrib4Nubv)GetOpenGLFunction("glVertexAttrib4Nubv");
		glVertexAttrib4Nuiv = (PROC_glVertexAttrib4Nuiv)GetOpenGLFunction("glVertexAttrib4Nuiv");
		glVertexAttrib4Nusv = (PROC_glVertexAttrib4Nusv)GetOpenGLFunction("glVertexAttrib4Nusv");
		glVertexAttrib4bv = (PROC_glVertexAttrib4bv)GetOpenGLFunction("glVertexAttrib4bv");
		glVertexAttrib4d = (PROC_glVertexAttrib4d)GetOpenGLFunction("glVertexAttrib4d");
		glVertexAttrib4dv = (PROC_glVertexAttrib4dv)GetOpenGLFunction("glVertexAttrib4dv");
		glVertexAttrib4f = (PROC_glVertexAttrib4f)GetOpenGLFunction("glVertexAttrib4f");
		glVertexAttrib4fv = (PROC_glVertexAttrib4fv)GetOpenGLFunction("glVertexAttrib4fv");
		glVertexAttrib4iv = (PROC_glVertexAttrib4iv)GetOpenGLFunction("glVertexAttrib4iv");
		glVertexAttrib4s = (PROC_glVertexAttrib4s)GetOpenGLFunction("glVertexAttrib4s");
		glVertexAttrib4sv = (PROC_glVertexAttrib4sv)GetOpenGLFunction("glVertexAttrib4sv");
		glVertexAttrib4ubv = (PROC_glVertexAttrib4ubv)GetOpenGLFunction("glVertexAttrib4ubv");
		glVertexAttrib4uiv = (PROC_glVertexAttrib4uiv)GetOpenGLFunction("glVertexAttrib4uiv");
		glVertexAttrib4usv = (PROC_glVertexAttrib4usv)GetOpenGLFunction("glVertexAttrib4usv");
		glVertexAttribPointer = (PROC_glVertexAttribPointer)GetOpenGLFunction("glVertexAttribPointer");
		glUniformMatrix2x3fv = (PROC_glUniformMatrix2x3fv)GetOpenGLFunction("glUniformMatrix2x3fv");
		glUniformMatrix3x2fv = (PROC_glUniformMatrix3x2fv)GetOpenGLFunction("glUniformMatrix3x2fv");
		glUniformMatrix2x4fv = (PROC_glUniformMatrix2x4fv)GetOpenGLFunction("glUniformMatrix2x4fv");
		glUniformMatrix4x2fv = (PROC_glUniformMatrix4x2fv)GetOpenGLFunction("glUniformMatrix4x2fv");
		glUniformMatrix3x4fv = (PROC_glUniformMatrix3x4fv)GetOpenGLFunction("glUniformMatrix3x4fv");
		glUniformMatrix4x3fv = (PROC_glUniformMatrix4x3fv)GetOpenGLFunction("glUniformMatrix4x3fv");
		glColorMaski = (PROC_glColorMaski)GetOpenGLFunction("glColorMaski");
		glGetBooleani_v = (PROC_glGetBooleani_v)GetOpenGLFunction("glGetBooleani_v");
		glGetIntegeri_v = (PROC_glGetIntegeri_v)GetOpenGLFunction("glGetIntegeri_v");
		glEnablei = (PROC_glEnablei)GetOpenGLFunction("glEnablei");
		glDisablei = (PROC_glDisablei)GetOpenGLFunction("glDisablei");
		glIsEnabledi = (PROC_glIsEnabledi)GetOpenGLFunction("glIsEnabledi");
		glBeginTransformFeedback = (PROC_glBeginTransformFeedback)GetOpenGLFunction("glBeginTransformFeedback");
		glEndTransformFeedback = (PROC_glEndTransformFeedback)GetOpenGLFunction("glEndTransformFeedback");
		glBindBufferRange = (PROC_glBindBufferRange)GetOpenGLFunction("glBindBufferRange");
		glBindBufferBase = (PROC_glBindBufferBase)GetOpenGLFunction("glBindBufferBase");
		glTransformFeedbackVaryings = (PROC_glTransformFeedbackVaryings)GetOpenGLFunction("glTransformFeedbackVaryings");
		glGetTransformFeedbackVarying = (PROC_glGetTransformFeedbackVarying)GetOpenGLFunction("glGetTransformFeedbackVarying");
		glClampColor = (PROC_glClampColor)GetOpenGLFunction("glClampColor");
		glBeginConditionalRender = (PROC_glBeginConditionalRender)GetOpenGLFunction("glBeginConditionalRender");
		glEndConditionalRender = (PROC_glEndConditionalRender)GetOpenGLFunction("glEndConditionalRender");
		glVertexAttribIPointer = (PROC_glVertexAttribIPointer)GetOpenGLFunction("glVertexAttribIPointer");
		glGetVertexAttribIiv = (PROC_glGetVertexAttribIiv)GetOpenGLFunction("glGetVertexAttribIiv");
		glGetVertexAttribIuiv = (PROC_glGetVertexAttribIuiv)GetOpenGLFunction("glGetVertexAttribIuiv");
		glVertexAttribI1i = (PROC_glVertexAttribI1i)GetOpenGLFunction("glVertexAttribI1i");
		glVertexAttribI2i = (PROC_glVertexAttribI2i)GetOpenGLFunction("glVertexAttribI2i");
		glVertexAttribI3i = (PROC_glVertexAttribI3i)GetOpenGLFunction("glVertexAttribI3i");
		glVertexAttribI4i = (PROC_glVertexAttribI4i)GetOpenGLFunction("glVertexAttribI4i");
		glVertexAttribI1ui = (PROC_glVertexAttribI1ui)GetOpenGLFunction("glVertexAttribI1ui");
		glVertexAttribI2ui = (PROC_glVertexAttribI2ui)GetOpenGLFunction("glVertexAttribI2ui");
		glVertexAttribI3ui = (PROC_glVertexAttribI3ui)GetOpenGLFunction("glVertexAttribI3ui");
		glVertexAttribI4ui = (PROC_glVertexAttribI4ui)GetOpenGLFunction("glVertexAttribI4ui");
		glVertexAttribI1iv = (PROC_glVertexAttribI1iv)GetOpenGLFunction("glVertexAttribI1iv");
		glVertexAttribI2iv = (PROC_glVertexAttribI2iv)GetOpenGLFunction("glVertexAttribI2iv");
		glVertexAttribI3iv = (PROC_glVertexAttribI3iv)GetOpenGLFunction("glVertexAttribI3iv");
		glVertexAttribI4iv = (PROC_glVertexAttribI4iv)GetOpenGLFunction("glVertexAttribI4iv");
		glVertexAttribI1uiv = (PROC_glVertexAttribI1uiv)GetOpenGLFunction("glVertexAttribI1uiv");
		glVertexAttribI2uiv = (PROC_glVertexAttribI2uiv)GetOpenGLFunction("glVertexAttribI2uiv");
		glVertexAttribI3uiv = (PROC_glVertexAttribI3uiv)GetOpenGLFunction("glVertexAttribI3uiv");
		glVertexAttribI4uiv = (PROC_glVertexAttribI4uiv)GetOpenGLFunction("glVertexAttribI4uiv");
		glVertexAttribI4bv = (PROC_glVertexAttribI4bv)GetOpenGLFunction("glVertexAttribI4bv");
		glVertexAttribI4sv = (PROC_glVertexAttribI4sv)GetOpenGLFunction("glVertexAttribI4sv");
		glVertexAttribI4ubv = (PROC_glVertexAttribI4ubv)GetOpenGLFunction("glVertexAttribI4ubv");
		glVertexAttribI4usv = (PROC_glVertexAttribI4usv)GetOpenGLFunction("glVertexAttribI4usv");
		glGetUniformuiv = (PROC_glGetUniformuiv)GetOpenGLFunction("glGetUniformuiv");
		glBindFragDataLocation = (PROC_glBindFragDataLocation)GetOpenGLFunction("glBindFragDataLocation");
		glGetFragDataLocation = (PROC_glGetFragDataLocation)GetOpenGLFunction("glGetFragDataLocation");
		glUniform1ui = (PROC_glUniform1ui)GetOpenGLFunction("glUniform1ui");
		glUniform2ui = (PROC_glUniform2ui)GetOpenGLFunction("glUniform2ui");
		glUniform3ui = (PROC_glUniform3ui)GetOpenGLFunction("glUniform3ui");
		glUniform4ui = (PROC_glUniform4ui)GetOpenGLFunction("glUniform4ui");
		glUniform1uiv = (PROC_glUniform1uiv)GetOpenGLFunction("glUniform1uiv");
		glUniform2uiv = (PROC_glUniform2uiv)GetOpenGLFunction("glUniform2uiv");
		glUniform3uiv = (PROC_glUniform3uiv)GetOpenGLFunction("glUniform3uiv");
		glUniform4uiv = (PROC_glUniform4uiv)GetOpenGLFunction("glUniform4uiv");
		glTexParameterIiv = (PROC_glTexParameterIiv)GetOpenGLFunction("glTexParameterIiv");
		glTexParameterIuiv = (PROC_glTexParameterIuiv)GetOpenGLFunction("glTexParameterIuiv");
		glGetTexParameterIiv = (PROC_glGetTexParameterIiv)GetOpenGLFunction("glGetTexParameterIiv");
		glGetTexParameterIuiv = (PROC_glGetTexParameterIuiv)GetOpenGLFunction("glGetTexParameterIuiv");
		glClearBufferiv = (PROC_glClearBufferiv)GetOpenGLFunction("glClearBufferiv");
		glClearBufferuiv = (PROC_glClearBufferuiv)GetOpenGLFunction("glClearBufferuiv");
		glClearBufferfv = (PROC_glClearBufferfv)GetOpenGLFunction("glClearBufferfv");
		glClearBufferfi = (PROC_glClearBufferfi)GetOpenGLFunction("glClearBufferfi");
		glGetStringi = (PROC_glGetStringi)GetOpenGLFunction("glGetStringi");
		glIsRenderbuffer = (PROC_glIsRenderbuffer)GetOpenGLFunction("glIsRenderbuffer");
		glBindRenderbuffer = (PROC_glBindRenderbuffer)GetOpenGLFunction("glBindRenderbuffer");
		glDeleteRenderbuffers = (PROC_glDeleteRenderbuffers)GetOpenGLFunction("glDeleteRenderbuffers");
		glGenRenderbuffers = (PROC_glGenRenderbuffers)GetOpenGLFunction("glGenRenderbuffers");
		glRenderbufferStorage = (PROC_glRenderbufferStorage)GetOpenGLFunction("glRenderbufferStorage");
		glGetRenderbufferParameteriv = (PROC_glGetRenderbufferParameteriv)GetOpenGLFunction("glGetRenderbufferParameteriv");
		glIsFramebuffer = (PROC_glIsFramebuffer)GetOpenGLFunction("glIsFramebuffer");
		glBindFramebuffer = (PROC_glBindFramebuffer)GetOpenGLFunction("glBindFramebuffer");
		glDeleteFramebuffers = (PROC_glDeleteFramebuffers)GetOpenGLFunction("glDeleteFramebuffers");
		glGenFramebuffers = (PROC_glGenFramebuffers)GetOpenGLFunction("glGenFramebuffers");
		glCheckFramebufferStatus = (PROC_glCheckFramebufferStatus)GetOpenGLFunction("glCheckFramebufferStatus");
		glFramebufferTexture1D = (PROC_glFramebufferTexture1D)GetOpenGLFunction("glFramebufferTexture1D");
		glFramebufferTexture2D = (PROC_glFramebufferTexture2D)GetOpenGLFunction("glFramebufferTexture2D");
		glFramebufferTexture3D = (PROC_glFramebufferTexture3D)GetOpenGLFunction("glFramebufferTexture3D");
		glFramebufferRenderbuffer = (PROC_glFramebufferRenderbuffer)GetOpenGLFunction("glFramebufferRenderbuffer");
		glGetFramebufferAttachmentParameteriv = (PROC_glGetFramebufferAttachmentParameteriv)GetOpenGLFunction("glGetFramebufferAttachmentParameteriv");
		glGenerateMipmap = (PROC_glGenerateMipmap)GetOpenGLFunction("glGenerateMipmap");
		glBlitFramebuffer = (PROC_glBlitFramebuffer)GetOpenGLFunction("glBlitFramebuffer");
		glRenderbufferStorageMultisample = (PROC_glRenderbufferStorageMultisample)GetOpenGLFunction("glRenderbufferStorageMultisample");
		glFramebufferTextureLayer = (PROC_glFramebufferTextureLayer)GetOpenGLFunction("glFramebufferTextureLayer");
		glMapBufferRange = (PROC_glMapBufferRange)GetOpenGLFunction("glMapBufferRange");
		glFlushMappedBufferRange = (PROC_glFlushMappedBufferRange)GetOpenGLFunction("glFlushMappedBufferRange");
		glBindVertexArray = (PROC_glBindVertexArray)GetOpenGLFunction("glBindVertexArray");
		glDeleteVertexArrays = (PROC_glDeleteVertexArrays)GetOpenGLFunction("glDeleteVertexArrays");
		glGenVertexArrays = (PROC_glGenVertexArrays)GetOpenGLFunction("glGenVertexArrays");
		glIsVertexArray = (PROC_glIsVertexArray)GetOpenGLFunction("glIsVertexArray");
		glDrawArraysInstanced = (PROC_glDrawArraysInstanced)GetOpenGLFunction("glDrawArraysInstanced");
		glDrawElementsInstanced = (PROC_glDrawElementsInstanced)GetOpenGLFunction("glDrawElementsInstanced");
		glTexBuffer = (PROC_glTexBuffer)GetOpenGLFunction("glTexBuffer");
		glPrimitiveRestartIndex = (PROC_glPrimitiveRestartIndex)GetOpenGLFunction("glPrimitiveRestartIndex");
		glCopyBufferSubData = (PROC_glCopyBufferSubData)GetOpenGLFunction("glCopyBufferSubData");
		glGetUniformIndices = (PROC_glGetUniformIndices)GetOpenGLFunction("glGetUniformIndices");
		glGetActiveUniformsiv = (PROC_glGetActiveUniformsiv)GetOpenGLFunction("glGetActiveUniformsiv");
		glGetActiveUniformName = (PROC_glGetActiveUniformName)GetOpenGLFunction("glGetActiveUniformName");
		glGetUniformBlockIndex = (PROC_glGetUniformBlockIndex)GetOpenGLFunction("glGetUniformBlockIndex");
		glGetActiveUniformBlockiv = (PROC_glGetActiveUniformBlockiv)GetOpenGLFunction("glGetActiveUniformBlockiv");
		glGetActiveUniformBlockName = (PROC_glGetActiveUniformBlockName)GetOpenGLFunction("glGetActiveUniformBlockName");
		glUniformBlockBinding = (PROC_glUniformBlockBinding)GetOpenGLFunction("glUniformBlockBinding");
		glDrawElementsBaseVertex = (PROC_glDrawElementsBaseVertex)GetOpenGLFunction("glDrawElementsBaseVertex");
		glDrawRangeElementsBaseVertex = (PROC_glDrawRangeElementsBaseVertex)GetOpenGLFunction("glDrawRangeElementsBaseVertex");
		glDrawElementsInstancedBaseVertex = (PROC_glDrawElementsInstancedBaseVertex)GetOpenGLFunction("glDrawElementsInstancedBaseVertex");
		glMultiDrawElementsBaseVertex = (PROC_glMultiDrawElementsBaseVertex)GetOpenGLFunction("glMultiDrawElementsBaseVertex");
		glProvokingVertex = (PROC_glProvokingVertex)GetOpenGLFunction("glProvokingVertex");
		glFenceSync = (PROC_glFenceSync)GetOpenGLFunction("glFenceSync");
		glIsSync = (PROC_glIsSync)GetOpenGLFunction("glIsSync");
		glDeleteSync = (PROC_glDeleteSync)GetOpenGLFunction("glDeleteSync");
		glClientWaitSync = (PROC_glClientWaitSync)GetOpenGLFunction("glClientWaitSync");
		glWaitSync = (PROC_glWaitSync)GetOpenGLFunction("glWaitSync");
		glGetInteger64v = (PROC_glGetInteger64v)GetOpenGLFunction("glGetInteger64v");
		glGetSynciv = (PROC_glGetSynciv)GetOpenGLFunction("glGetSynciv");
		glGetInteger64i_v = (PROC_glGetInteger64i_v)GetOpenGLFunction("glGetInteger64i_v");
		glGetBufferParameteri64v = (PROC_glGetBufferParameteri64v)GetOpenGLFunction("glGetBufferParameteri64v");
		glFramebufferTexture = (PROC_glFramebufferTexture)GetOpenGLFunction("glFramebufferTexture");
		glTexImage2DMultisample = (PROC_glTexImage2DMultisample)GetOpenGLFunction("glTexImage2DMultisample");
		glTexImage3DMultisample = (PROC_glTexImage3DMultisample)GetOpenGLFunction("glTexImage3DMultisample");
		glGetMultisamplefv = (PROC_glGetMultisamplefv)GetOpenGLFunction("glGetMultisamplefv");
		glSampleMaski = (PROC_glSampleMaski)GetOpenGLFunction("glSampleMaski");
		glBindFragDataLocationIndexed = (PROC_glBindFragDataLocationIndexed)GetOpenGLFunction("glBindFragDataLocationIndexed");
		glGetFragDataIndex = (PROC_glGetFragDataIndex)GetOpenGLFunction("glGetFragDataIndex");
		glGenSamplers = (PROC_glGenSamplers)GetOpenGLFunction("glGenSamplers");
		glDeleteSamplers = (PROC_glDeleteSamplers)GetOpenGLFunction("glDeleteSamplers");
		glIsSampler = (PROC_glIsSampler)GetOpenGLFunction("glIsSampler");
		glBindSampler = (PROC_glBindSampler)GetOpenGLFunction("glBindSampler");
		glSamplerParameteri = (PROC_glSamplerParameteri)GetOpenGLFunction("glSamplerParameteri");
		glSamplerParameteriv = (PROC_glSamplerParameteriv)GetOpenGLFunction("glSamplerParameteriv");
		glSamplerParameterf = (PROC_glSamplerParameterf)GetOpenGLFunction("glSamplerParameterf");
		glSamplerParameterfv = (PROC_glSamplerParameterfv)GetOpenGLFunction("glSamplerParameterfv");
		glSamplerParameterIiv = (PROC_glSamplerParameterIiv)GetOpenGLFunction("glSamplerParameterIiv");
		glSamplerParameterIuiv = (PROC_glSamplerParameterIuiv)GetOpenGLFunction("glSamplerParameterIuiv");
		glGetSamplerParameteriv = (PROC_glGetSamplerParameteriv)GetOpenGLFunction("glGetSamplerParameteriv");
		glGetSamplerParameterIiv = (PROC_glGetSamplerParameterIiv)GetOpenGLFunction("glGetSamplerParameterIiv");
		glGetSamplerParameterfv = (PROC_glGetSamplerParameterfv)GetOpenGLFunction("glGetSamplerParameterfv");
		glGetSamplerParameterIuiv = (PROC_glGetSamplerParameterIuiv)GetOpenGLFunction("glGetSamplerParameterIuiv");
		glQueryCounter = (PROC_glQueryCounter)GetOpenGLFunction("glQueryCounter");
		glGetQueryObjecti64v = (PROC_glGetQueryObjecti64v)GetOpenGLFunction("glGetQueryObjecti64v");
		glGetQueryObjectui64v = (PROC_glGetQueryObjectui64v)GetOpenGLFunction("glGetQueryObjectui64v");
		glVertexAttribDivisor = (PROC_glVertexAttribDivisor)GetOpenGLFunction("glVertexAttribDivisor");
		glVertexAttribP1ui = (PROC_glVertexAttribP1ui)GetOpenGLFunction("glVertexAttribP1ui");
		glVertexAttribP1uiv = (PROC_glVertexAttribP1uiv)GetOpenGLFunction("glVertexAttribP1uiv");
		glVertexAttribP2ui = (PROC_glVertexAttribP2ui)GetOpenGLFunction("glVertexAttribP2ui");
		glVertexAttribP2uiv = (PROC_glVertexAttribP2uiv)GetOpenGLFunction("glVertexAttribP2uiv");
		glVertexAttribP3ui = (PROC_glVertexAttribP3ui)GetOpenGLFunction("glVertexAttribP3ui");
		glVertexAttribP3uiv = (PROC_glVertexAttribP3uiv)GetOpenGLFunction("glVertexAttribP3uiv");
		glVertexAttribP4ui = (PROC_glVertexAttribP4ui)GetOpenGLFunction("glVertexAttribP4ui");
		glVertexAttribP4uiv = (PROC_glVertexAttribP4uiv)GetOpenGLFunction("glVertexAttribP4uiv");
		glMinSampleShading = (PROC_glMinSampleShading)GetOpenGLFunction("glMinSampleShading");
		glBlendEquationi = (PROC_glBlendEquationi)GetOpenGLFunction("glBlendEquationi");
		glBlendEquationSeparatei = (PROC_glBlendEquationSeparatei)GetOpenGLFunction("glBlendEquationSeparatei");
		glBlendFunci = (PROC_glBlendFunci)GetOpenGLFunction("glBlendFunci");
		glBlendFuncSeparatei = (PROC_glBlendFuncSeparatei)GetOpenGLFunction("glBlendFuncSeparatei");
		glDrawArraysIndirect = (PROC_glDrawArraysIndirect)GetOpenGLFunction("glDrawArraysIndirect");
		glDrawElementsIndirect = (PROC_glDrawElementsIndirect)GetOpenGLFunction("glDrawElementsIndirect");
		glUniform1d = (PROC_glUniform1d)GetOpenGLFunction("glUniform1d");
		glUniform2d = (PROC_glUniform2d)GetOpenGLFunction("glUniform2d");
		glUniform3d = (PROC_glUniform3d)GetOpenGLFunction("glUniform3d");
		glUniform4d = (PROC_glUniform4d)GetOpenGLFunction("glUniform4d");
		glUniform1dv = (PROC_glUniform1dv)GetOpenGLFunction("glUniform1dv");
		glUniform2dv = (PROC_glUniform2dv)GetOpenGLFunction("glUniform2dv");
		glUniform3dv = (PROC_glUniform3dv)GetOpenGLFunction("glUniform3dv");
		glUniform4dv = (PROC_glUniform4dv)GetOpenGLFunction("glUniform4dv");
		glUniformMatrix2dv = (PROC_glUniformMatrix2dv)GetOpenGLFunction("glUniformMatrix2dv");
		glUniformMatrix3dv = (PROC_glUniformMatrix3dv)GetOpenGLFunction("glUniformMatrix3dv");
		glUniformMatrix4dv = (PROC_glUniformMatrix4dv)GetOpenGLFunction("glUniformMatrix4dv");
		glUniformMatrix2x3dv = (PROC_glUniformMatrix2x3dv)GetOpenGLFunction("glUniformMatrix2x3dv");
		glUniformMatrix2x4dv = (PROC_glUniformMatrix2x4dv)GetOpenGLFunction("glUniformMatrix2x4dv");
		glUniformMatrix3x2dv = (PROC_glUniformMatrix3x2dv)GetOpenGLFunction("glUniformMatrix3x2dv");
		glUniformMatrix3x4dv = (PROC_glUniformMatrix3x4dv)GetOpenGLFunction("glUniformMatrix3x4dv");
		glUniformMatrix4x2dv = (PROC_glUniformMatrix4x2dv)GetOpenGLFunction("glUniformMatrix4x2dv");
		glUniformMatrix4x3dv = (PROC_glUniformMatrix4x3dv)GetOpenGLFunction("glUniformMatrix4x3dv");
		glGetUniformdv = (PROC_glGetUniformdv)GetOpenGLFunction("glGetUniformdv");
		glGetSubroutineUniformLocation = (PROC_glGetSubroutineUniformLocation)GetOpenGLFunction("glGetSubroutineUniformLocation");
		glGetSubroutineIndex = (PROC_glGetSubroutineIndex)GetOpenGLFunction("glGetSubroutineIndex");
		glGetActiveSubroutineUniformiv = (PROC_glGetActiveSubroutineUniformiv)GetOpenGLFunction("glGetActiveSubroutineUniformiv");
		glGetActiveSubroutineUniformName = (PROC_glGetActiveSubroutineUniformName)GetOpenGLFunction("glGetActiveSubroutineUniformName");
		glGetActiveSubroutineName = (PROC_glGetActiveSubroutineName)GetOpenGLFunction("glGetActiveSubroutineName");
		glUniformSubroutinesuiv = (PROC_glUniformSubroutinesuiv)GetOpenGLFunction("glUniformSubroutinesuiv");
		glGetUniformSubroutineuiv = (PROC_glGetUniformSubroutineuiv)GetOpenGLFunction("glGetUniformSubroutineuiv");
		glGetProgramStageiv = (PROC_glGetProgramStageiv)GetOpenGLFunction("glGetProgramStageiv");
		glPatchParameteri = (PROC_glPatchParameteri)GetOpenGLFunction("glPatchParameteri");
		glPatchParameterfv = (PROC_glPatchParameterfv)GetOpenGLFunction("glPatchParameterfv");
		glBindTransformFeedback = (PROC_glBindTransformFeedback)GetOpenGLFunction("glBindTransformFeedback");
		glDeleteTransformFeedbacks = (PROC_glDeleteTransformFeedbacks)GetOpenGLFunction("glDeleteTransformFeedbacks");
		glGenTransformFeedbacks = (PROC_glGenTransformFeedbacks)GetOpenGLFunction("glGenTransformFeedbacks");
		glIsTransformFeedback = (PROC_glIsTransformFeedback)GetOpenGLFunction("glIsTransformFeedback");
		glPauseTransformFeedback = (PROC_glPauseTransformFeedback)GetOpenGLFunction("glPauseTransformFeedback");
		glResumeTransformFeedback = (PROC_glResumeTransformFeedback)GetOpenGLFunction("glResumeTransformFeedback");
		glDrawTransformFeedback = (PROC_glDrawTransformFeedback)GetOpenGLFunction("glDrawTransformFeedback");
		glDrawTransformFeedbackStream = (PROC_glDrawTransformFeedbackStream)GetOpenGLFunction("glDrawTransformFeedbackStream");
		glBeginQueryIndexed = (PROC_glBeginQueryIndexed)GetOpenGLFunction("glBeginQueryIndexed");
		glEndQueryIndexed = (PROC_glEndQueryIndexed)GetOpenGLFunction("glEndQueryIndexed");
		glGetQueryIndexediv = (PROC_glGetQueryIndexediv)GetOpenGLFunction("glGetQueryIndexediv");
		glReleaseShaderCompiler = (PROC_glReleaseShaderCompiler)GetOpenGLFunction("glReleaseShaderCompiler");
		glShaderBinary = (PROC_glShaderBinary)GetOpenGLFunction("glShaderBinary");
		glGetShaderPrecisionFormat = (PROC_glGetShaderPrecisionFormat)GetOpenGLFunction("glGetShaderPrecisionFormat");
		glDepthRangef = (PROC_glDepthRangef)GetOpenGLFunction("glDepthRangef");
		glClearDepthf = (PROC_glClearDepthf)GetOpenGLFunction("glClearDepthf");
		glGetProgramBinary = (PROC_glGetProgramBinary)GetOpenGLFunction("glGetProgramBinary");
		glProgramBinary = (PROC_glProgramBinary)GetOpenGLFunction("glProgramBinary");
		glProgramParameteri = (PROC_glProgramParameteri)GetOpenGLFunction("glProgramParameteri");
		glUseProgramStages = (PROC_glUseProgramStages)GetOpenGLFunction("glUseProgramStages");
		glActiveShaderProgram = (PROC_glActiveShaderProgram)GetOpenGLFunction("glActiveShaderProgram");
		glCreateShaderProgramv = (PROC_glCreateShaderProgramv)GetOpenGLFunction("glCreateShaderProgramv");
		glBindProgramPipeline = (PROC_glBindProgramPipeline)GetOpenGLFunction("glBindProgramPipeline");
		glDeleteProgramPipelines = (PROC_glDeleteProgramPipelines)GetOpenGLFunction("glDeleteProgramPipelines");
		glGenProgramPipelines = (PROC_glGenProgramPipelines)GetOpenGLFunction("glGenProgramPipelines");
		glIsProgramPipeline = (PROC_glIsProgramPipeline)GetOpenGLFunction("glIsProgramPipeline");
		glGetProgramPipelineiv = (PROC_glGetProgramPipelineiv)GetOpenGLFunction("glGetProgramPipelineiv");
		glProgramUniform1i = (PROC_glProgramUniform1i)GetOpenGLFunction("glProgramUniform1i");
		glProgramUniform1iv = (PROC_glProgramUniform1iv)GetOpenGLFunction("glProgramUniform1iv");
		glProgramUniform1f = (PROC_glProgramUniform1f)GetOpenGLFunction("glProgramUniform1f");
		glProgramUniform1fv = (PROC_glProgramUniform1fv)GetOpenGLFunction("glProgramUniform1fv");
		glProgramUniform1d = (PROC_glProgramUniform1d)GetOpenGLFunction("glProgramUniform1d");
		glProgramUniform1dv = (PROC_glProgramUniform1dv)GetOpenGLFunction("glProgramUniform1dv");
		glProgramUniform1ui = (PROC_glProgramUniform1ui)GetOpenGLFunction("glProgramUniform1ui");
		glProgramUniform1uiv = (PROC_glProgramUniform1uiv)GetOpenGLFunction("glProgramUniform1uiv");
		glProgramUniform2i = (PROC_glProgramUniform2i)GetOpenGLFunction("glProgramUniform2i");
		glProgramUniform2iv = (PROC_glProgramUniform2iv)GetOpenGLFunction("glProgramUniform2iv");
		glProgramUniform2f = (PROC_glProgramUniform2f)GetOpenGLFunction("glProgramUniform2f");
		glProgramUniform2fv = (PROC_glProgramUniform2fv)GetOpenGLFunction("glProgramUniform2fv");
		glProgramUniform2d = (PROC_glProgramUniform2d)GetOpenGLFunction("glProgramUniform2d");
		glProgramUniform2dv = (PROC_glProgramUniform2dv)GetOpenGLFunction("glProgramUniform2dv");
		glProgramUniform2ui = (PROC_glProgramUniform2ui)GetOpenGLFunction("glProgramUniform2ui");
		glProgramUniform2uiv = (PROC_glProgramUniform2uiv)GetOpenGLFunction("glProgramUniform2uiv");
		glProgramUniform3i = (PROC_glProgramUniform3i)GetOpenGLFunction("glProgramUniform3i");
		glProgramUniform3iv = (PROC_glProgramUniform3iv)GetOpenGLFunction("glProgramUniform3iv");
		glProgramUniform3f = (PROC_glProgramUniform3f)GetOpenGLFunction("glProgramUniform3f");
		glProgramUniform3fv = (PROC_glProgramUniform3fv)GetOpenGLFunction("glProgramUniform3fv");
		glProgramUniform3d = (PROC_glProgramUniform3d)GetOpenGLFunction("glProgramUniform3d");
		glProgramUniform3dv = (PROC_glProgramUniform3dv)GetOpenGLFunction("glProgramUniform3dv");
		glProgramUniform3ui = (PROC_glProgramUniform3ui)GetOpenGLFunction("glProgramUniform3ui");
		glProgramUniform3uiv = (PROC_glProgramUniform3uiv)GetOpenGLFunction("glProgramUniform3uiv");
		glProgramUniform4i = (PROC_glProgramUniform4i)GetOpenGLFunction("glProgramUniform4i");
		glProgramUniform4iv = (PROC_glProgramUniform4iv)GetOpenGLFunction("glProgramUniform4iv");
		glProgramUniform4f = (PROC_glProgramUniform4f)GetOpenGLFunction("glProgramUniform4f");
		glProgramUniform4fv = (PROC_glProgramUniform4fv)GetOpenGLFunction("glProgramUniform4fv");
		glProgramUniform4d = (PROC_glProgramUniform4d)GetOpenGLFunction("glProgramUniform4d");
		glProgramUniform4dv = (PROC_glProgramUniform4dv)GetOpenGLFunction("glProgramUniform4dv");
		glProgramUniform4ui = (PROC_glProgramUniform4ui)GetOpenGLFunction("glProgramUniform4ui");
		glProgramUniform4uiv = (PROC_glProgramUniform4uiv)GetOpenGLFunction("glProgramUniform4uiv");
		glProgramUniformMatrix2fv = (PROC_glProgramUniformMatrix2fv)GetOpenGLFunction("glProgramUniformMatrix2fv");
		glProgramUniformMatrix3fv = (PROC_glProgramUniformMatrix3fv)GetOpenGLFunction("glProgramUniformMatrix3fv");
		glProgramUniformMatrix4fv = (PROC_glProgramUniformMatrix4fv)GetOpenGLFunction("glProgramUniformMatrix4fv");
		glProgramUniformMatrix2dv = (PROC_glProgramUniformMatrix2dv)GetOpenGLFunction("glProgramUniformMatrix2dv");
		glProgramUniformMatrix3dv = (PROC_glProgramUniformMatrix3dv)GetOpenGLFunction("glProgramUniformMatrix3dv");
		glProgramUniformMatrix4dv = (PROC_glProgramUniformMatrix4dv)GetOpenGLFunction("glProgramUniformMatrix4dv");
		glProgramUniformMatrix2x3fv = (PROC_glProgramUniformMatrix2x3fv)GetOpenGLFunction("glProgramUniformMatrix2x3fv");
		glProgramUniformMatrix3x2fv = (PROC_glProgramUniformMatrix3x2fv)GetOpenGLFunction("glProgramUniformMatrix3x2fv");
		glProgramUniformMatrix2x4fv = (PROC_glProgramUniformMatrix2x4fv)GetOpenGLFunction("glProgramUniformMatrix2x4fv");
		glProgramUniformMatrix4x2fv = (PROC_glProgramUniformMatrix4x2fv)GetOpenGLFunction("glProgramUniformMatrix4x2fv");
		glProgramUniformMatrix3x4fv = (PROC_glProgramUniformMatrix3x4fv)GetOpenGLFunction("glProgramUniformMatrix3x4fv");
		glProgramUniformMatrix4x3fv = (PROC_glProgramUniformMatrix4x3fv)GetOpenGLFunction("glProgramUniformMatrix4x3fv");
		glProgramUniformMatrix2x3dv = (PROC_glProgramUniformMatrix2x3dv)GetOpenGLFunction("glProgramUniformMatrix2x3dv");
		glProgramUniformMatrix3x2dv = (PROC_glProgramUniformMatrix3x2dv)GetOpenGLFunction("glProgramUniformMatrix3x2dv");
		glProgramUniformMatrix2x4dv = (PROC_glProgramUniformMatrix2x4dv)GetOpenGLFunction("glProgramUniformMatrix2x4dv");
		glProgramUniformMatrix4x2dv = (PROC_glProgramUniformMatrix4x2dv)GetOpenGLFunction("glProgramUniformMatrix4x2dv");
		glProgramUniformMatrix3x4dv = (PROC_glProgramUniformMatrix3x4dv)GetOpenGLFunction("glProgramUniformMatrix3x4dv");
		glProgramUniformMatrix4x3dv = (PROC_glProgramUniformMatrix4x3dv)GetOpenGLFunction("glProgramUniformMatrix4x3dv");
		glValidateProgramPipeline = (PROC_glValidateProgramPipeline)GetOpenGLFunction("glValidateProgramPipeline");
		glGetProgramPipelineInfoLog = (PROC_glGetProgramPipelineInfoLog)GetOpenGLFunction("glGetProgramPipelineInfoLog");
		glVertexAttribL1d = (PROC_glVertexAttribL1d)GetOpenGLFunction("glVertexAttribL1d");
		glVertexAttribL2d = (PROC_glVertexAttribL2d)GetOpenGLFunction("glVertexAttribL2d");
		glVertexAttribL3d = (PROC_glVertexAttribL3d)GetOpenGLFunction("glVertexAttribL3d");
		glVertexAttribL4d = (PROC_glVertexAttribL4d)GetOpenGLFunction("glVertexAttribL4d");
		glVertexAttribL1dv = (PROC_glVertexAttribL1dv)GetOpenGLFunction("glVertexAttribL1dv");
		glVertexAttribL2dv = (PROC_glVertexAttribL2dv)GetOpenGLFunction("glVertexAttribL2dv");
		glVertexAttribL3dv = (PROC_glVertexAttribL3dv)GetOpenGLFunction("glVertexAttribL3dv");
		glVertexAttribL4dv = (PROC_glVertexAttribL4dv)GetOpenGLFunction("glVertexAttribL4dv");
		glVertexAttribLPointer = (PROC_glVertexAttribLPointer)GetOpenGLFunction("glVertexAttribLPointer");
		glGetVertexAttribLdv = (PROC_glGetVertexAttribLdv)GetOpenGLFunction("glGetVertexAttribLdv");
		glViewportArrayv = (PROC_glViewportArrayv)GetOpenGLFunction("glViewportArrayv");
		glViewportIndexedf = (PROC_glViewportIndexedf)GetOpenGLFunction("glViewportIndexedf");
		glViewportIndexedfv = (PROC_glViewportIndexedfv)GetOpenGLFunction("glViewportIndexedfv");
		glScissorArrayv = (PROC_glScissorArrayv)GetOpenGLFunction("glScissorArrayv");
		glScissorIndexed = (PROC_glScissorIndexed)GetOpenGLFunction("glScissorIndexed");
		glScissorIndexedv = (PROC_glScissorIndexedv)GetOpenGLFunction("glScissorIndexedv");
		glDepthRangeArrayv = (PROC_glDepthRangeArrayv)GetOpenGLFunction("glDepthRangeArrayv");
		glDepthRangeIndexed = (PROC_glDepthRangeIndexed)GetOpenGLFunction("glDepthRangeIndexed");
		glGetFloati_v = (PROC_glGetFloati_v)GetOpenGLFunction("glGetFloati_v");
		glGetDoublei_v = (PROC_glGetDoublei_v)GetOpenGLFunction("glGetDoublei_v");
		glDrawArraysInstancedBaseInstance = (PROC_glDrawArraysInstancedBaseInstance)GetOpenGLFunction("glDrawArraysInstancedBaseInstance");
		glDrawElementsInstancedBaseInstance = (PROC_glDrawElementsInstancedBaseInstance)GetOpenGLFunction("glDrawElementsInstancedBaseInstance");
		glDrawElementsInstancedBaseVertexBaseInstance = (PROC_glDrawElementsInstancedBaseVertexBaseInstance)GetOpenGLFunction("glDrawElementsInstancedBaseVertexBaseInstance");
		glGetInternalformativ = (PROC_glGetInternalformativ)GetOpenGLFunction("glGetInternalformativ");
		glGetActiveAtomicCounterBufferiv = (PROC_glGetActiveAtomicCounterBufferiv)GetOpenGLFunction("glGetActiveAtomicCounterBufferiv");
		glBindImageTexture = (PROC_glBindImageTexture)GetOpenGLFunction("glBindImageTexture");
		glMemoryBarrier = (PROC_glMemoryBarrier)GetOpenGLFunction("glMemoryBarrier");
		glTexStorage1D = (PROC_glTexStorage1D)GetOpenGLFunction("glTexStorage1D");
		glTexStorage2D = (PROC_glTexStorage2D)GetOpenGLFunction("glTexStorage2D");
		glTexStorage3D = (PROC_glTexStorage3D)GetOpenGLFunction("glTexStorage3D");
		glDrawTransformFeedbackInstanced = (PROC_glDrawTransformFeedbackInstanced)GetOpenGLFunction("glDrawTransformFeedbackInstanced");
		glDrawTransformFeedbackStreamInstanced = (PROC_glDrawTransformFeedbackStreamInstanced)GetOpenGLFunction("glDrawTransformFeedbackStreamInstanced");
		glClearBufferData = (PROC_glClearBufferData)GetOpenGLFunction("glClearBufferData");
		glClearBufferSubData = (PROC_glClearBufferSubData)GetOpenGLFunction("glClearBufferSubData");
		glDispatchCompute = (PROC_glDispatchCompute)GetOpenGLFunction("glDispatchCompute");
		glDispatchComputeIndirect = (PROC_glDispatchComputeIndirect)GetOpenGLFunction("glDispatchComputeIndirect");
		glCopyImageSubData = (PROC_glCopyImageSubData)GetOpenGLFunction("glCopyImageSubData");
		glFramebufferParameteri = (PROC_glFramebufferParameteri)GetOpenGLFunction("glFramebufferParameteri");
		glGetFramebufferParameteriv = (PROC_glGetFramebufferParameteriv)GetOpenGLFunction("glGetFramebufferParameteriv");
		glGetInternalformati64v = (PROC_glGetInternalformati64v)GetOpenGLFunction("glGetInternalformati64v");
		glInvalidateTexSubImage = (PROC_glInvalidateTexSubImage)GetOpenGLFunction("glInvalidateTexSubImage");
		glInvalidateTexImage = (PROC_glInvalidateTexImage)GetOpenGLFunction("glInvalidateTexImage");
		glInvalidateBufferSubData = (PROC_glInvalidateBufferSubData)GetOpenGLFunction("glInvalidateBufferSubData");
		glInvalidateBufferData = (PROC_glInvalidateBufferData)GetOpenGLFunction("glInvalidateBufferData");
		glInvalidateFramebuffer = (PROC_glInvalidateFramebuffer)GetOpenGLFunction("glInvalidateFramebuffer");
		glInvalidateSubFramebuffer = (PROC_glInvalidateSubFramebuffer)GetOpenGLFunction("glInvalidateSubFramebuffer");
		glMultiDrawArraysIndirect = (PROC_glMultiDrawArraysIndirect)GetOpenGLFunction("glMultiDrawArraysIndirect");
		glMultiDrawElementsIndirect = (PROC_glMultiDrawElementsIndirect)GetOpenGLFunction("glMultiDrawElementsIndirect");
		glGetProgramInterfaceiv = (PROC_glGetProgramInterfaceiv)GetOpenGLFunction("glGetProgramInterfaceiv");
		glGetProgramResourceIndex = (PROC_glGetProgramResourceIndex)GetOpenGLFunction("glGetProgramResourceIndex");
		glGetProgramResourceName = (PROC_glGetProgramResourceName)GetOpenGLFunction("glGetProgramResourceName");
		glGetProgramResourceiv = (PROC_glGetProgramResourceiv)GetOpenGLFunction("glGetProgramResourceiv");
		glGetProgramResourceLocation = (PROC_glGetProgramResourceLocation)GetOpenGLFunction("glGetProgramResourceLocation");
		glGetProgramResourceLocationIndex = (PROC_glGetProgramResourceLocationIndex)GetOpenGLFunction("glGetProgramResourceLocationIndex");
		glShaderStorageBlockBinding = (PROC_glShaderStorageBlockBinding)GetOpenGLFunction("glShaderStorageBlockBinding");
		glTexBufferRange = (PROC_glTexBufferRange)GetOpenGLFunction("glTexBufferRange");
		glTexStorage2DMultisample = (PROC_glTexStorage2DMultisample)GetOpenGLFunction("glTexStorage2DMultisample");
		glTexStorage3DMultisample = (PROC_glTexStorage3DMultisample)GetOpenGLFunction("glTexStorage3DMultisample");
		glTextureView = (PROC_glTextureView)GetOpenGLFunction("glTextureView");
		glBindVertexBuffer = (PROC_glBindVertexBuffer)GetOpenGLFunction("glBindVertexBuffer");
		glVertexAttribFormat = (PROC_glVertexAttribFormat)GetOpenGLFunction("glVertexAttribFormat");
		glVertexAttribIFormat = (PROC_glVertexAttribIFormat)GetOpenGLFunction("glVertexAttribIFormat");
		glVertexAttribLFormat = (PROC_glVertexAttribLFormat)GetOpenGLFunction("glVertexAttribLFormat");
		glVertexAttribBinding = (PROC_glVertexAttribBinding)GetOpenGLFunction("glVertexAttribBinding");
		glVertexBindingDivisor = (PROC_glVertexBindingDivisor)GetOpenGLFunction("glVertexBindingDivisor");
		glDebugMessageControl = (PROC_glDebugMessageControl)GetOpenGLFunction("glDebugMessageControl");
		glDebugMessageInsert = (PROC_glDebugMessageInsert)GetOpenGLFunction("glDebugMessageInsert");
		glDebugMessageCallback = (PROC_glDebugMessageCallback)GetOpenGLFunction("glDebugMessageCallback");
		glGetDebugMessageLog = (PROC_glGetDebugMessageLog)GetOpenGLFunction("glGetDebugMessageLog");
		glPushDebugGroup = (PROC_glPushDebugGroup)GetOpenGLFunction("glPushDebugGroup");
		glPopDebugGroup = (PROC_glPopDebugGroup)GetOpenGLFunction("glPopDebugGroup");
		glObjectLabel = (PROC_glObjectLabel)GetOpenGLFunction("glObjectLabel");
		glGetObjectLabel = (PROC_glGetObjectLabel)GetOpenGLFunction("glGetObjectLabel");
		glObjectPtrLabel = (PROC_glObjectPtrLabel)GetOpenGLFunction("glObjectPtrLabel");
		glGetObjectPtrLabel = (PROC_glGetObjectPtrLabel)GetOpenGLFunction("glGetObjectPtrLabel");
		glBufferStorage = (PROC_glBufferStorage)GetOpenGLFunction("glBufferStorage");
		glClearTexImage = (PROC_glClearTexImage)GetOpenGLFunction("glClearTexImage");
		glClearTexSubImage = (PROC_glClearTexSubImage)GetOpenGLFunction("glClearTexSubImage");
		glBindBuffersBase = (PROC_glBindBuffersBase)GetOpenGLFunction("glBindBuffersBase");
		glBindBuffersRange = (PROC_glBindBuffersRange)GetOpenGLFunction("glBindBuffersRange");
		glBindTextures = (PROC_glBindTextures)GetOpenGLFunction("glBindTextures");
		glBindSamplers = (PROC_glBindSamplers)GetOpenGLFunction("glBindSamplers");
		glBindImageTextures = (PROC_glBindImageTextures)GetOpenGLFunction("glBindImageTextures");
		glBindVertexBuffers = (PROC_glBindVertexBuffers)GetOpenGLFunction("glBindVertexBuffers");
		glClipControl = (PROC_glClipControl)GetOpenGLFunction("glClipControl");
		glCreateTransformFeedbacks = (PROC_glCreateTransformFeedbacks)GetOpenGLFunction("glCreateTransformFeedbacks");
		glTransformFeedbackBufferBase = (PROC_glTransformFeedbackBufferBase)GetOpenGLFunction("glTransformFeedbackBufferBase");
		glTransformFeedbackBufferRange = (PROC_glTransformFeedbackBufferRange)GetOpenGLFunction("glTransformFeedbackBufferRange");
		glGetTransformFeedbackiv = (PROC_glGetTransformFeedbackiv)GetOpenGLFunction("glGetTransformFeedbackiv");
		glGetTransformFeedbacki_v = (PROC_glGetTransformFeedbacki_v)GetOpenGLFunction("glGetTransformFeedbacki_v");
		glGetTransformFeedbacki64_v = (PROC_glGetTransformFeedbacki64_v)GetOpenGLFunction("glGetTransformFeedbacki64_v");
		glCreateBuffers = (PROC_glCreateBuffers)GetOpenGLFunction("glCreateBuffers");
		glNamedBufferStorage = (PROC_glNamedBufferStorage)GetOpenGLFunction("glNamedBufferStorage");
		glNamedBufferData = (PROC_glNamedBufferData)GetOpenGLFunction("glNamedBufferData");
		glNamedBufferSubData = (PROC_glNamedBufferSubData)GetOpenGLFunction("glNamedBufferSubData");
		glCopyNamedBufferSubData = (PROC_glCopyNamedBufferSubData)GetOpenGLFunction("glCopyNamedBufferSubData");
		glClearNamedBufferData = (PROC_glClearNamedBufferData)GetOpenGLFunction("glClearNamedBufferData");
		glClearNamedBufferSubData = (PROC_glClearNamedBufferSubData)GetOpenGLFunction("glClearNamedBufferSubData");
		glMapNamedBuffer = (PROC_glMapNamedBuffer)GetOpenGLFunction("glMapNamedBuffer");
		glMapNamedBufferRange = (PROC_glMapNamedBufferRange)GetOpenGLFunction("glMapNamedBufferRange");
		glUnmapNamedBuffer = (PROC_glUnmapNamedBuffer)GetOpenGLFunction("glUnmapNamedBuffer");
		glFlushMappedNamedBufferRange = (PROC_glFlushMappedNamedBufferRange)GetOpenGLFunction("glFlushMappedNamedBufferRange");
		glGetNamedBufferParameteriv = (PROC_glGetNamedBufferParameteriv)GetOpenGLFunction("glGetNamedBufferParameteriv");
		glGetNamedBufferParameteri64v = (PROC_glGetNamedBufferParameteri64v)GetOpenGLFunction("glGetNamedBufferParameteri64v");
		glGetNamedBufferPointerv = (PROC_glGetNamedBufferPointerv)GetOpenGLFunction("glGetNamedBufferPointerv");
		glGetNamedBufferSubData = (PROC_glGetNamedBufferSubData)GetOpenGLFunction("glGetNamedBufferSubData");
		glCreateFramebuffers = (PROC_glCreateFramebuffers)GetOpenGLFunction("glCreateFramebuffers");
		glNamedFramebufferRenderbuffer = (PROC_glNamedFramebufferRenderbuffer)GetOpenGLFunction("glNamedFramebufferRenderbuffer");
		glNamedFramebufferParameteri = (PROC_glNamedFramebufferParameteri)GetOpenGLFunction("glNamedFramebufferParameteri");
		glNamedFramebufferTexture = (PROC_glNamedFramebufferTexture)GetOpenGLFunction("glNamedFramebufferTexture");
		glNamedFramebufferTextureLayer = (PROC_glNamedFramebufferTextureLayer)GetOpenGLFunction("glNamedFramebufferTextureLayer");
		glNamedFramebufferDrawBuffer = (PROC_glNamedFramebufferDrawBuffer)GetOpenGLFunction("glNamedFramebufferDrawBuffer");
		glNamedFramebufferDrawBuffers = (PROC_glNamedFramebufferDrawBuffers)GetOpenGLFunction("glNamedFramebufferDrawBuffers");
		glNamedFramebufferReadBuffer = (PROC_glNamedFramebufferReadBuffer)GetOpenGLFunction("glNamedFramebufferReadBuffer");
		glInvalidateNamedFramebufferData = (PROC_glInvalidateNamedFramebufferData)GetOpenGLFunction("glInvalidateNamedFramebufferData");
		glInvalidateNamedFramebufferSubData = (PROC_glInvalidateNamedFramebufferSubData)GetOpenGLFunction("glInvalidateNamedFramebufferSubData");
		glClearNamedFramebufferiv = (PROC_glClearNamedFramebufferiv)GetOpenGLFunction("glClearNamedFramebufferiv");
		glClearNamedFramebufferuiv = (PROC_glClearNamedFramebufferuiv)GetOpenGLFunction("glClearNamedFramebufferuiv");
		glClearNamedFramebufferfv = (PROC_glClearNamedFramebufferfv)GetOpenGLFunction("glClearNamedFramebufferfv");
		glClearNamedFramebufferfi = (PROC_glClearNamedFramebufferfi)GetOpenGLFunction("glClearNamedFramebufferfi");
		glBlitNamedFramebuffer = (PROC_glBlitNamedFramebuffer)GetOpenGLFunction("glBlitNamedFramebuffer");
		glCheckNamedFramebufferStatus = (PROC_glCheckNamedFramebufferStatus)GetOpenGLFunction("glCheckNamedFramebufferStatus");
		glGetNamedFramebufferParameteriv = (PROC_glGetNamedFramebufferParameteriv)GetOpenGLFunction("glGetNamedFramebufferParameteriv");
		glGetNamedFramebufferAttachmentParameteriv = (PROC_glGetNamedFramebufferAttachmentParameteriv)GetOpenGLFunction("glGetNamedFramebufferAttachmentParameteriv");
		glCreateRenderbuffers = (PROC_glCreateRenderbuffers)GetOpenGLFunction("glCreateRenderbuffers");
		glNamedRenderbufferStorage = (PROC_glNamedRenderbufferStorage)GetOpenGLFunction("glNamedRenderbufferStorage");
		glNamedRenderbufferStorageMultisample = (PROC_glNamedRenderbufferStorageMultisample)GetOpenGLFunction("glNamedRenderbufferStorageMultisample");
		glGetNamedRenderbufferParameteriv = (PROC_glGetNamedRenderbufferParameteriv)GetOpenGLFunction("glGetNamedRenderbufferParameteriv");
		glCreateTextures = (PROC_glCreateTextures)GetOpenGLFunction("glCreateTextures");
		glTextureBuffer = (PROC_glTextureBuffer)GetOpenGLFunction("glTextureBuffer");
		glTextureBufferRange = (PROC_glTextureBufferRange)GetOpenGLFunction("glTextureBufferRange");
		glTextureStorage1D = (PROC_glTextureStorage1D)GetOpenGLFunction("glTextureStorage1D");
		glTextureStorage2D = (PROC_glTextureStorage2D)GetOpenGLFunction("glTextureStorage2D");
		glTextureStorage3D = (PROC_glTextureStorage3D)GetOpenGLFunction("glTextureStorage3D");
		glTextureStorage2DMultisample = (PROC_glTextureStorage2DMultisample)GetOpenGLFunction("glTextureStorage2DMultisample");
		glTextureStorage3DMultisample = (PROC_glTextureStorage3DMultisample)GetOpenGLFunction("glTextureStorage3DMultisample");
		glTextureSubImage1D = (PROC_glTextureSubImage1D)GetOpenGLFunction("glTextureSubImage1D");
		glTextureSubImage2D = (PROC_glTextureSubImage2D)GetOpenGLFunction("glTextureSubImage2D");
		glTextureSubImage3D = (PROC_glTextureSubImage3D)GetOpenGLFunction("glTextureSubImage3D");
		glCompressedTextureSubImage1D = (PROC_glCompressedTextureSubImage1D)GetOpenGLFunction("glCompressedTextureSubImage1D");
		glCompressedTextureSubImage2D = (PROC_glCompressedTextureSubImage2D)GetOpenGLFunction("glCompressedTextureSubImage2D");
		glCompressedTextureSubImage3D = (PROC_glCompressedTextureSubImage3D)GetOpenGLFunction("glCompressedTextureSubImage3D");
		glCopyTextureSubImage1D = (PROC_glCopyTextureSubImage1D)GetOpenGLFunction("glCopyTextureSubImage1D");
		glCopyTextureSubImage2D = (PROC_glCopyTextureSubImage2D)GetOpenGLFunction("glCopyTextureSubImage2D");
		glCopyTextureSubImage3D = (PROC_glCopyTextureSubImage3D)GetOpenGLFunction("glCopyTextureSubImage3D");
		glTextureParameterf = (PROC_glTextureParameterf)GetOpenGLFunction("glTextureParameterf");
		glTextureParameterfv = (PROC_glTextureParameterfv)GetOpenGLFunction("glTextureParameterfv");
		glTextureParameteri = (PROC_glTextureParameteri)GetOpenGLFunction("glTextureParameteri");
		glTextureParameterIiv = (PROC_glTextureParameterIiv)GetOpenGLFunction("glTextureParameterIiv");
		glTextureParameterIuiv = (PROC_glTextureParameterIuiv)GetOpenGLFunction("glTextureParameterIuiv");
		glTextureParameteriv = (PROC_glTextureParameteriv)GetOpenGLFunction("glTextureParameteriv");
		glGenerateTextureMipmap = (PROC_glGenerateTextureMipmap)GetOpenGLFunction("glGenerateTextureMipmap");
		glBindTextureUnit = (PROC_glBindTextureUnit)GetOpenGLFunction("glBindTextureUnit");
		glGetTextureImage = (PROC_glGetTextureImage)GetOpenGLFunction("glGetTextureImage");
		glGetCompressedTextureImage = (PROC_glGetCompressedTextureImage)GetOpenGLFunction("glGetCompressedTextureImage");
		glGetTextureLevelParameterfv = (PROC_glGetTextureLevelParameterfv)GetOpenGLFunction("glGetTextureLevelParameterfv");
		glGetTextureLevelParameteriv = (PROC_glGetTextureLevelParameteriv)GetOpenGLFunction("glGetTextureLevelParameteriv");
		glGetTextureParameterfv = (PROC_glGetTextureParameterfv)GetOpenGLFunction("glGetTextureParameterfv");
		glGetTextureParameterIiv = (PROC_glGetTextureParameterIiv)GetOpenGLFunction("glGetTextureParameterIiv");
		glGetTextureParameterIuiv = (PROC_glGetTextureParameterIuiv)GetOpenGLFunction("glGetTextureParameterIuiv");
		glGetTextureParameteriv = (PROC_glGetTextureParameteriv)GetOpenGLFunction("glGetTextureParameteriv");
		glCreateVertexArrays = (PROC_glCreateVertexArrays)GetOpenGLFunction("glCreateVertexArrays");
		glDisableVertexArrayAttrib = (PROC_glDisableVertexArrayAttrib)GetOpenGLFunction("glDisableVertexArrayAttrib");
		glEnableVertexArrayAttrib = (PROC_glEnableVertexArrayAttrib)GetOpenGLFunction("glEnableVertexArrayAttrib");
		glVertexArrayElementBuffer = (PROC_glVertexArrayElementBuffer)GetOpenGLFunction("glVertexArrayElementBuffer");
		glVertexArrayVertexBuffer = (PROC_glVertexArrayVertexBuffer)GetOpenGLFunction("glVertexArrayVertexBuffer");
		glVertexArrayVertexBuffers = (PROC_glVertexArrayVertexBuffers)GetOpenGLFunction("glVertexArrayVertexBuffers");
		glVertexArrayAttribBinding = (PROC_glVertexArrayAttribBinding)GetOpenGLFunction("glVertexArrayAttribBinding");
		glVertexArrayAttribFormat = (PROC_glVertexArrayAttribFormat)GetOpenGLFunction("glVertexArrayAttribFormat");
		glVertexArrayAttribIFormat = (PROC_glVertexArrayAttribIFormat)GetOpenGLFunction("glVertexArrayAttribIFormat");
		glVertexArrayAttribLFormat = (PROC_glVertexArrayAttribLFormat)GetOpenGLFunction("glVertexArrayAttribLFormat");
		glVertexArrayBindingDivisor = (PROC_glVertexArrayBindingDivisor)GetOpenGLFunction("glVertexArrayBindingDivisor");
		glGetVertexArrayiv = (PROC_glGetVertexArrayiv)GetOpenGLFunction("glGetVertexArrayiv");
		glGetVertexArrayIndexediv = (PROC_glGetVertexArrayIndexediv)GetOpenGLFunction("glGetVertexArrayIndexediv");
		glGetVertexArrayIndexed64iv = (PROC_glGetVertexArrayIndexed64iv)GetOpenGLFunction("glGetVertexArrayIndexed64iv");
		glCreateSamplers = (PROC_glCreateSamplers)GetOpenGLFunction("glCreateSamplers");
		glCreateProgramPipelines = (PROC_glCreateProgramPipelines)GetOpenGLFunction("glCreateProgramPipelines");
		glCreateQueries = (PROC_glCreateQueries)GetOpenGLFunction("glCreateQueries");
		glGetQueryBufferObjecti64v = (PROC_glGetQueryBufferObjecti64v)GetOpenGLFunction("glGetQueryBufferObjecti64v");
		glGetQueryBufferObjectiv = (PROC_glGetQueryBufferObjectiv)GetOpenGLFunction("glGetQueryBufferObjectiv");
		glGetQueryBufferObjectui64v = (PROC_glGetQueryBufferObjectui64v)GetOpenGLFunction("glGetQueryBufferObjectui64v");
		glGetQueryBufferObjectuiv = (PROC_glGetQueryBufferObjectuiv)GetOpenGLFunction("glGetQueryBufferObjectuiv");
		glMemoryBarrierByRegion = (PROC_glMemoryBarrierByRegion)GetOpenGLFunction("glMemoryBarrierByRegion");
		glGetTextureSubImage = (PROC_glGetTextureSubImage)GetOpenGLFunction("glGetTextureSubImage");
		glGetCompressedTextureSubImage = (PROC_glGetCompressedTextureSubImage)GetOpenGLFunction("glGetCompressedTextureSubImage");
		glGetGraphicsResetStatus = (PROC_glGetGraphicsResetStatus)GetOpenGLFunction("glGetGraphicsResetStatus");
		glGetnCompressedTexImage = (PROC_glGetnCompressedTexImage)GetOpenGLFunction("glGetnCompressedTexImage");
		glGetnTexImage = (PROC_glGetnTexImage)GetOpenGLFunction("glGetnTexImage");
		glGetnUniformdv = (PROC_glGetnUniformdv)GetOpenGLFunction("glGetnUniformdv");
		glGetnUniformfv = (PROC_glGetnUniformfv)GetOpenGLFunction("glGetnUniformfv");
		glGetnUniformiv = (PROC_glGetnUniformiv)GetOpenGLFunction("glGetnUniformiv");
		glGetnUniformuiv = (PROC_glGetnUniformuiv)GetOpenGLFunction("glGetnUniformuiv");
		glReadnPixels = (PROC_glReadnPixels)GetOpenGLFunction("glReadnPixels");
		glTextureBarrier = (PROC_glTextureBarrier)GetOpenGLFunction("glTextureBarrier");

		return true;
	}

	bool isglCullFace() {
		return glCullFace != 0;
	}

	bool isglFrontFace() {
		return glFrontFace != 0;
	}

	bool isglHint() {
		return glHint != 0;
	}

	bool isglLineWidth() {
		return glLineWidth != 0;
	}

	bool isglPointSize() {
		return glPointSize != 0;
	}

	bool isglPolygonMode() {
		return glPolygonMode != 0;
	}

	bool isglScissor() {
		return glScissor != 0;
	}

	bool isglTexParameterf() {
		return glTexParameterf != 0;
	}

	bool isglTexParameterfv() {
		return glTexParameterfv != 0;
	}

	bool isglTexParameteri() {
		return glTexParameteri != 0;
	}

	bool isglTexParameteriv() {
		return glTexParameteriv != 0;
	}

	bool isglTexImage1D() {
		return glTexImage1D != 0;
	}

	bool isglTexImage2D() {
		return glTexImage2D != 0;
	}

	bool isglDrawBuffer() {
		return glDrawBuffer != 0;
	}

	bool isglClear() {
		return glClear != 0;
	}

	bool isglClearColor() {
		return glClearColor != 0;
	}

	bool isglClearStencil() {
		return glClearStencil != 0;
	}

	bool isglClearDepth() {
		return glClearDepth != 0;
	}

	bool isglStencilMask() {
		return glStencilMask != 0;
	}

	bool isglColorMask() {
		return glColorMask != 0;
	}

	bool isglDepthMask() {
		return glDepthMask != 0;
	}

	bool isglDisable() {
		return glDisable != 0;
	}

	bool isglEnable() {
		return glEnable != 0;
	}

	bool isglFinish() {
		return glFinish != 0;
	}

	bool isglFlush() {
		return glFlush != 0;
	}

	bool isglBlendFunc() {
		return glBlendFunc != 0;
	}

	bool isglLogicOp() {
		return glLogicOp != 0;
	}

	bool isglStencilFunc() {
		return glStencilFunc != 0;
	}

	bool isglStencilOp() {
		return glStencilOp != 0;
	}

	bool isglDepthFunc() {
		return glDepthFunc != 0;
	}

	bool isglPixelStoref() {
		return glPixelStoref != 0;
	}

	bool isglPixelStorei() {
		return glPixelStorei != 0;
	}

	bool isglReadBuffer() {
		return glReadBuffer != 0;
	}

	bool isglReadPixels() {
		return glReadPixels != 0;
	}

	bool isglGetBooleanv() {
		return glGetBooleanv != 0;
	}

	bool isglGetDoublev() {
		return glGetDoublev != 0;
	}

	bool isglGetError() {
		return glGetError != 0;
	}

	bool isglGetFloatv() {
		return glGetFloatv != 0;
	}

	bool isglGetIntegerv() {
		return glGetIntegerv != 0;
	}

	bool isglGetString() {
		return glGetString != 0;
	}

	bool isglGetTexImage() {
		return glGetTexImage != 0;
	}

	bool isglGetTexParameterfv() {
		return glGetTexParameterfv != 0;
	}

	bool isglGetTexParameteriv() {
		return glGetTexParameteriv != 0;
	}

	bool isglGetTexLevelParameterfv() {
		return glGetTexLevelParameterfv != 0;
	}

	bool isglGetTexLevelParameteriv() {
		return glGetTexLevelParameteriv != 0;
	}

	bool isglIsEnabled() {
		return glIsEnabled != 0;
	}

	bool isglDepthRange() {
		return glDepthRange != 0;
	}

	bool isglViewport() {
		return glViewport != 0;
	}

	bool isglDrawArrays() {
		return glDrawArrays != 0;
	}

	bool isglDrawElements() {
		return glDrawElements != 0;
	}

	bool isglGetPointerv() {
		return glGetPointerv != 0;
	}

	bool isglPolygonOffset() {
		return glPolygonOffset != 0;
	}

	bool isglCopyTexImage1D() {
		return glCopyTexImage1D != 0;
	}

	bool isglCopyTexImage2D() {
		return glCopyTexImage2D != 0;
	}

	bool isglCopyTexSubImage1D() {
		return glCopyTexSubImage1D != 0;
	}

	bool isglCopyTexSubImage2D() {
		return glCopyTexSubImage2D != 0;
	}

	bool isglTexSubImage1D() {
		return glTexSubImage1D != 0;
	}

	bool isglTexSubImage2D() {
		return glTexSubImage2D != 0;
	}

	bool isglBindTexture() {
		return glBindTexture != 0;
	}

	bool isglDeleteTextures() {
		return glDeleteTextures != 0;
	}

	bool isglGenTextures() {
		return glGenTextures != 0;
	}

	bool isglIsTexture() {
		return glIsTexture != 0;
	}

	bool isglDrawRangeElements() {
		return glDrawRangeElements != 0;
	}

	bool isglTexImage3D() {
		return glTexImage3D != 0;
	}

	bool isglTexSubImage3D() {
		return glTexSubImage3D != 0;
	}

	bool isglCopyTexSubImage3D() {
		return glCopyTexSubImage3D != 0;
	}

	bool isglActiveTexture() {
		return glActiveTexture != 0;
	}

	bool isglSampleCoverage() {
		return glSampleCoverage != 0;
	}

	bool isglCompressedTexImage3D() {
		return glCompressedTexImage3D != 0;
	}

	bool isglCompressedTexImage2D() {
		return glCompressedTexImage2D != 0;
	}

	bool isglCompressedTexImage1D() {
		return glCompressedTexImage1D != 0;
	}

	bool isglCompressedTexSubImage3D() {
		return glCompressedTexSubImage3D != 0;
	}

	bool isglCompressedTexSubImage2D() {
		return glCompressedTexSubImage2D != 0;
	}

	bool isglCompressedTexSubImage1D() {
		return glCompressedTexSubImage1D != 0;
	}

	bool isglGetCompressedTexImage() {
		return glGetCompressedTexImage != 0;
	}

	bool isglBlendFuncSeparate() {
		return glBlendFuncSeparate != 0;
	}

	bool isglMultiDrawArrays() {
		return glMultiDrawArrays != 0;
	}

	bool isglMultiDrawElements() {
		return glMultiDrawElements != 0;
	}

	bool isglPointParameterf() {
		return glPointParameterf != 0;
	}

	bool isglPointParameterfv() {
		return glPointParameterfv != 0;
	}

	bool isglPointParameteri() {
		return glPointParameteri != 0;
	}

	bool isglPointParameteriv() {
		return glPointParameteriv != 0;
	}

	bool isglBlendColor() {
		return glBlendColor != 0;
	}

	bool isglBlendEquation() {
		return glBlendEquation != 0;
	}

	bool isglGenQueries() {
		return glGenQueries != 0;
	}

	bool isglDeleteQueries() {
		return glDeleteQueries != 0;
	}

	bool isglIsQuery() {
		return glIsQuery != 0;
	}

	bool isglBeginQuery() {
		return glBeginQuery != 0;
	}

	bool isglEndQuery() {
		return glEndQuery != 0;
	}

	bool isglGetQueryiv() {
		return glGetQueryiv != 0;
	}

	bool isglGetQueryObjectiv() {
		return glGetQueryObjectiv != 0;
	}

	bool isglGetQueryObjectuiv() {
		return glGetQueryObjectuiv != 0;
	}

	bool isglBindBuffer() {
		return glBindBuffer != 0;
	}

	bool isglDeleteBuffers() {
		return glDeleteBuffers != 0;
	}

	bool isglGenBuffers() {
		return glGenBuffers != 0;
	}

	bool isglIsBuffer() {
		return glIsBuffer != 0;
	}

	bool isglBufferData() {
		return glBufferData != 0;
	}

	bool isglBufferSubData() {
		return glBufferSubData != 0;
	}

	bool isglGetBufferSubData() {
		return glGetBufferSubData != 0;
	}

	bool isglMapBuffer() {
		return glMapBuffer != 0;
	}

	bool isglUnmapBuffer() {
		return glUnmapBuffer != 0;
	}

	bool isglGetBufferParameteriv() {
		return glGetBufferParameteriv != 0;
	}

	bool isglGetBufferPointerv() {
		return glGetBufferPointerv != 0;
	}

	bool isglBlendEquationSeparate() {
		return glBlendEquationSeparate != 0;
	}

	bool isglDrawBuffers() {
		return glDrawBuffers != 0;
	}

	bool isglStencilOpSeparate() {
		return glStencilOpSeparate != 0;
	}

	bool isglStencilFuncSeparate() {
		return glStencilFuncSeparate != 0;
	}

	bool isglStencilMaskSeparate() {
		return glStencilMaskSeparate != 0;
	}

	bool isglAttachShader() {
		return glAttachShader != 0;
	}

	bool isglBindAttribLocation() {
		return glBindAttribLocation != 0;
	}

	bool isglCompileShader() {
		return glCompileShader != 0;
	}

	bool isglCreateProgram() {
		return glCreateProgram != 0;
	}

	bool isglCreateShader() {
		return glCreateShader != 0;
	}

	bool isglDeleteProgram() {
		return glDeleteProgram != 0;
	}

	bool isglDeleteShader() {
		return glDeleteShader != 0;
	}

	bool isglDetachShader() {
		return glDetachShader != 0;
	}

	bool isglDisableVertexAttribArray() {
		return glDisableVertexAttribArray != 0;
	}

	bool isglEnableVertexAttribArray() {
		return glEnableVertexAttribArray != 0;
	}

	bool isglGetActiveAttrib() {
		return glGetActiveAttrib != 0;
	}

	bool isglGetActiveUniform() {
		return glGetActiveUniform != 0;
	}

	bool isglGetAttachedShaders() {
		return glGetAttachedShaders != 0;
	}

	bool isglGetAttribLocation() {
		return glGetAttribLocation != 0;
	}

	bool isglGetProgramiv() {
		return glGetProgramiv != 0;
	}

	bool isglGetProgramInfoLog() {
		return glGetProgramInfoLog != 0;
	}

	bool isglGetShaderiv() {
		return glGetShaderiv != 0;
	}

	bool isglGetShaderInfoLog() {
		return glGetShaderInfoLog != 0;
	}

	bool isglGetShaderSource() {
		return glGetShaderSource != 0;
	}

	bool isglGetUniformLocation() {
		return glGetUniformLocation != 0;
	}

	bool isglGetUniformfv() {
		return glGetUniformfv != 0;
	}

	bool isglGetUniformiv() {
		return glGetUniformiv != 0;
	}

	bool isglGetVertexAttribdv() {
		return glGetVertexAttribdv != 0;
	}

	bool isglGetVertexAttribfv() {
		return glGetVertexAttribfv != 0;
	}

	bool isglGetVertexAttribiv() {
		return glGetVertexAttribiv != 0;
	}

	bool isglGetVertexAttribPointerv() {
		return glGetVertexAttribPointerv != 0;
	}

	bool isglIsProgram() {
		return glIsProgram != 0;
	}

	bool isglIsShader() {
		return glIsShader != 0;
	}

	bool isglLinkProgram() {
		return glLinkProgram != 0;
	}

	bool isglShaderSource() {
		return glShaderSource != 0;
	}

	bool isglUseProgram() {
		return glUseProgram != 0;
	}

	bool isglUniform1f() {
		return glUniform1f != 0;
	}

	bool isglUniform2f() {
		return glUniform2f != 0;
	}

	bool isglUniform3f() {
		return glUniform3f != 0;
	}

	bool isglUniform4f() {
		return glUniform4f != 0;
	}

	bool isglUniform1i() {
		return glUniform1i != 0;
	}

	bool isglUniform2i() {
		return glUniform2i != 0;
	}

	bool isglUniform3i() {
		return glUniform3i != 0;
	}

	bool isglUniform4i() {
		return glUniform4i != 0;
	}

	bool isglUniform1fv() {
		return glUniform1fv != 0;
	}

	bool isglUniform2fv() {
		return glUniform2fv != 0;
	}

	bool isglUniform3fv() {
		return glUniform3fv != 0;
	}

	bool isglUniform4fv() {
		return glUniform4fv != 0;
	}

	bool isglUniform1iv() {
		return glUniform1iv != 0;
	}

	bool isglUniform2iv() {
		return glUniform2iv != 0;
	}

	bool isglUniform3iv() {
		return glUniform3iv != 0;
	}

	bool isglUniform4iv() {
		return glUniform4iv != 0;
	}

	bool isglUniformMatrix2fv() {
		return glUniformMatrix2fv != 0;
	}

	bool isglUniformMatrix3fv() {
		return glUniformMatrix3fv != 0;
	}

	bool isglUniformMatrix4fv() {
		return glUniformMatrix4fv != 0;
	}

	bool isglValidateProgram() {
		return glValidateProgram != 0;
	}

	bool isglVertexAttrib1d() {
		return glVertexAttrib1d != 0;
	}

	bool isglVertexAttrib1dv() {
		return glVertexAttrib1dv != 0;
	}

	bool isglVertexAttrib1f() {
		return glVertexAttrib1f != 0;
	}

	bool isglVertexAttrib1fv() {
		return glVertexAttrib1fv != 0;
	}

	bool isglVertexAttrib1s() {
		return glVertexAttrib1s != 0;
	}

	bool isglVertexAttrib1sv() {
		return glVertexAttrib1sv != 0;
	}

	bool isglVertexAttrib2d() {
		return glVertexAttrib2d != 0;
	}

	bool isglVertexAttrib2dv() {
		return glVertexAttrib2dv != 0;
	}

	bool isglVertexAttrib2f() {
		return glVertexAttrib2f != 0;
	}

	bool isglVertexAttrib2fv() {
		return glVertexAttrib2fv != 0;
	}

	bool isglVertexAttrib2s() {
		return glVertexAttrib2s != 0;
	}

	bool isglVertexAttrib2sv() {
		return glVertexAttrib2sv != 0;
	}

	bool isglVertexAttrib3d() {
		return glVertexAttrib3d != 0;
	}

	bool isglVertexAttrib3dv() {
		return glVertexAttrib3dv != 0;
	}

	bool isglVertexAttrib3f() {
		return glVertexAttrib3f != 0;
	}

	bool isglVertexAttrib3fv() {
		return glVertexAttrib3fv != 0;
	}

	bool isglVertexAttrib3s() {
		return glVertexAttrib3s != 0;
	}

	bool isglVertexAttrib3sv() {
		return glVertexAttrib3sv != 0;
	}

	bool isglVertexAttrib4Nbv() {
		return glVertexAttrib4Nbv != 0;
	}

	bool isglVertexAttrib4Niv() {
		return glVertexAttrib4Niv != 0;
	}

	bool isglVertexAttrib4Nsv() {
		return glVertexAttrib4Nsv != 0;
	}

	bool isglVertexAttrib4Nub() {
		return glVertexAttrib4Nub != 0;
	}

	bool isglVertexAttrib4Nubv() {
		return glVertexAttrib4Nubv != 0;
	}

	bool isglVertexAttrib4Nuiv() {
		return glVertexAttrib4Nuiv != 0;
	}

	bool isglVertexAttrib4Nusv() {
		return glVertexAttrib4Nusv != 0;
	}

	bool isglVertexAttrib4bv() {
		return glVertexAttrib4bv != 0;
	}

	bool isglVertexAttrib4d() {
		return glVertexAttrib4d != 0;
	}

	bool isglVertexAttrib4dv() {
		return glVertexAttrib4dv != 0;
	}

	bool isglVertexAttrib4f() {
		return glVertexAttrib4f != 0;
	}

	bool isglVertexAttrib4fv() {
		return glVertexAttrib4fv != 0;
	}

	bool isglVertexAttrib4iv() {
		return glVertexAttrib4iv != 0;
	}

	bool isglVertexAttrib4s() {
		return glVertexAttrib4s != 0;
	}

	bool isglVertexAttrib4sv() {
		return glVertexAttrib4sv != 0;
	}

	bool isglVertexAttrib4ubv() {
		return glVertexAttrib4ubv != 0;
	}

	bool isglVertexAttrib4uiv() {
		return glVertexAttrib4uiv != 0;
	}

	bool isglVertexAttrib4usv() {
		return glVertexAttrib4usv != 0;
	}

	bool isglVertexAttribPointer() {
		return glVertexAttribPointer != 0;
	}

	bool isglUniformMatrix2x3fv() {
		return glUniformMatrix2x3fv != 0;
	}

	bool isglUniformMatrix3x2fv() {
		return glUniformMatrix3x2fv != 0;
	}

	bool isglUniformMatrix2x4fv() {
		return glUniformMatrix2x4fv != 0;
	}

	bool isglUniformMatrix4x2fv() {
		return glUniformMatrix4x2fv != 0;
	}

	bool isglUniformMatrix3x4fv() {
		return glUniformMatrix3x4fv != 0;
	}

	bool isglUniformMatrix4x3fv() {
		return glUniformMatrix4x3fv != 0;
	}

	bool isglColorMaski() {
		return glColorMaski != 0;
	}

	bool isglGetBooleani_v() {
		return glGetBooleani_v != 0;
	}

	bool isglGetIntegeri_v() {
		return glGetIntegeri_v != 0;
	}

	bool isglEnablei() {
		return glEnablei != 0;
	}

	bool isglDisablei() {
		return glDisablei != 0;
	}

	bool isglIsEnabledi() {
		return glIsEnabledi != 0;
	}

	bool isglBeginTransformFeedback() {
		return glBeginTransformFeedback != 0;
	}

	bool isglEndTransformFeedback() {
		return glEndTransformFeedback != 0;
	}

	bool isglBindBufferRange() {
		return glBindBufferRange != 0;
	}

	bool isglBindBufferBase() {
		return glBindBufferBase != 0;
	}

	bool isglTransformFeedbackVaryings() {
		return glTransformFeedbackVaryings != 0;
	}

	bool isglGetTransformFeedbackVarying() {
		return glGetTransformFeedbackVarying != 0;
	}

	bool isglClampColor() {
		return glClampColor != 0;
	}

	bool isglBeginConditionalRender() {
		return glBeginConditionalRender != 0;
	}

	bool isglEndConditionalRender() {
		return glEndConditionalRender != 0;
	}

	bool isglVertexAttribIPointer() {
		return glVertexAttribIPointer != 0;
	}

	bool isglGetVertexAttribIiv() {
		return glGetVertexAttribIiv != 0;
	}

	bool isglGetVertexAttribIuiv() {
		return glGetVertexAttribIuiv != 0;
	}

	bool isglVertexAttribI1i() {
		return glVertexAttribI1i != 0;
	}

	bool isglVertexAttribI2i() {
		return glVertexAttribI2i != 0;
	}

	bool isglVertexAttribI3i() {
		return glVertexAttribI3i != 0;
	}

	bool isglVertexAttribI4i() {
		return glVertexAttribI4i != 0;
	}

	bool isglVertexAttribI1ui() {
		return glVertexAttribI1ui != 0;
	}

	bool isglVertexAttribI2ui() {
		return glVertexAttribI2ui != 0;
	}

	bool isglVertexAttribI3ui() {
		return glVertexAttribI3ui != 0;
	}

	bool isglVertexAttribI4ui() {
		return glVertexAttribI4ui != 0;
	}

	bool isglVertexAttribI1iv() {
		return glVertexAttribI1iv != 0;
	}

	bool isglVertexAttribI2iv() {
		return glVertexAttribI2iv != 0;
	}

	bool isglVertexAttribI3iv() {
		return glVertexAttribI3iv != 0;
	}

	bool isglVertexAttribI4iv() {
		return glVertexAttribI4iv != 0;
	}

	bool isglVertexAttribI1uiv() {
		return glVertexAttribI1uiv != 0;
	}

	bool isglVertexAttribI2uiv() {
		return glVertexAttribI2uiv != 0;
	}

	bool isglVertexAttribI3uiv() {
		return glVertexAttribI3uiv != 0;
	}

	bool isglVertexAttribI4uiv() {
		return glVertexAttribI4uiv != 0;
	}

	bool isglVertexAttribI4bv() {
		return glVertexAttribI4bv != 0;
	}

	bool isglVertexAttribI4sv() {
		return glVertexAttribI4sv != 0;
	}

	bool isglVertexAttribI4ubv() {
		return glVertexAttribI4ubv != 0;
	}

	bool isglVertexAttribI4usv() {
		return glVertexAttribI4usv != 0;
	}

	bool isglGetUniformuiv() {
		return glGetUniformuiv != 0;
	}

	bool isglBindFragDataLocation() {
		return glBindFragDataLocation != 0;
	}

	bool isglGetFragDataLocation() {
		return glGetFragDataLocation != 0;
	}

	bool isglUniform1ui() {
		return glUniform1ui != 0;
	}

	bool isglUniform2ui() {
		return glUniform2ui != 0;
	}

	bool isglUniform3ui() {
		return glUniform3ui != 0;
	}

	bool isglUniform4ui() {
		return glUniform4ui != 0;
	}

	bool isglUniform1uiv() {
		return glUniform1uiv != 0;
	}

	bool isglUniform2uiv() {
		return glUniform2uiv != 0;
	}

	bool isglUniform3uiv() {
		return glUniform3uiv != 0;
	}

	bool isglUniform4uiv() {
		return glUniform4uiv != 0;
	}

	bool isglTexParameterIiv() {
		return glTexParameterIiv != 0;
	}

	bool isglTexParameterIuiv() {
		return glTexParameterIuiv != 0;
	}

	bool isglGetTexParameterIiv() {
		return glGetTexParameterIiv != 0;
	}

	bool isglGetTexParameterIuiv() {
		return glGetTexParameterIuiv != 0;
	}

	bool isglClearBufferiv() {
		return glClearBufferiv != 0;
	}

	bool isglClearBufferuiv() {
		return glClearBufferuiv != 0;
	}

	bool isglClearBufferfv() {
		return glClearBufferfv != 0;
	}

	bool isglClearBufferfi() {
		return glClearBufferfi != 0;
	}

	bool isglGetStringi() {
		return glGetStringi != 0;
	}

	bool isglIsRenderbuffer() {
		return glIsRenderbuffer != 0;
	}

	bool isglBindRenderbuffer() {
		return glBindRenderbuffer != 0;
	}

	bool isglDeleteRenderbuffers() {
		return glDeleteRenderbuffers != 0;
	}

	bool isglGenRenderbuffers() {
		return glGenRenderbuffers != 0;
	}

	bool isglRenderbufferStorage() {
		return glRenderbufferStorage != 0;
	}

	bool isglGetRenderbufferParameteriv() {
		return glGetRenderbufferParameteriv != 0;
	}

	bool isglIsFramebuffer() {
		return glIsFramebuffer != 0;
	}

	bool isglBindFramebuffer() {
		return glBindFramebuffer != 0;
	}

	bool isglDeleteFramebuffers() {
		return glDeleteFramebuffers != 0;
	}

	bool isglGenFramebuffers() {
		return glGenFramebuffers != 0;
	}

	bool isglCheckFramebufferStatus() {
		return glCheckFramebufferStatus != 0;
	}

	bool isglFramebufferTexture1D() {
		return glFramebufferTexture1D != 0;
	}

	bool isglFramebufferTexture2D() {
		return glFramebufferTexture2D != 0;
	}

	bool isglFramebufferTexture3D() {
		return glFramebufferTexture3D != 0;
	}

	bool isglFramebufferRenderbuffer() {
		return glFramebufferRenderbuffer != 0;
	}

	bool isglGetFramebufferAttachmentParameteriv() {
		return glGetFramebufferAttachmentParameteriv != 0;
	}

	bool isglGenerateMipmap() {
		return glGenerateMipmap != 0;
	}

	bool isglBlitFramebuffer() {
		return glBlitFramebuffer != 0;
	}

	bool isglRenderbufferStorageMultisample() {
		return glRenderbufferStorageMultisample != 0;
	}

	bool isglFramebufferTextureLayer() {
		return glFramebufferTextureLayer != 0;
	}

	bool isglMapBufferRange() {
		return glMapBufferRange != 0;
	}

	bool isglFlushMappedBufferRange() {
		return glFlushMappedBufferRange != 0;
	}

	bool isglBindVertexArray() {
		return glBindVertexArray != 0;
	}

	bool isglDeleteVertexArrays() {
		return glDeleteVertexArrays != 0;
	}

	bool isglGenVertexArrays() {
		return glGenVertexArrays != 0;
	}

	bool isglIsVertexArray() {
		return glIsVertexArray != 0;
	}

	bool isglDrawArraysInstanced() {
		return glDrawArraysInstanced != 0;
	}

	bool isglDrawElementsInstanced() {
		return glDrawElementsInstanced != 0;
	}

	bool isglTexBuffer() {
		return glTexBuffer != 0;
	}

	bool isglPrimitiveRestartIndex() {
		return glPrimitiveRestartIndex != 0;
	}

	bool isglCopyBufferSubData() {
		return glCopyBufferSubData != 0;
	}

	bool isglGetUniformIndices() {
		return glGetUniformIndices != 0;
	}

	bool isglGetActiveUniformsiv() {
		return glGetActiveUniformsiv != 0;
	}

	bool isglGetActiveUniformName() {
		return glGetActiveUniformName != 0;
	}

	bool isglGetUniformBlockIndex() {
		return glGetUniformBlockIndex != 0;
	}

	bool isglGetActiveUniformBlockiv() {
		return glGetActiveUniformBlockiv != 0;
	}

	bool isglGetActiveUniformBlockName() {
		return glGetActiveUniformBlockName != 0;
	}

	bool isglUniformBlockBinding() {
		return glUniformBlockBinding != 0;
	}

	bool isglDrawElementsBaseVertex() {
		return glDrawElementsBaseVertex != 0;
	}

	bool isglDrawRangeElementsBaseVertex() {
		return glDrawRangeElementsBaseVertex != 0;
	}

	bool isglDrawElementsInstancedBaseVertex() {
		return glDrawElementsInstancedBaseVertex != 0;
	}

	bool isglMultiDrawElementsBaseVertex() {
		return glMultiDrawElementsBaseVertex != 0;
	}

	bool isglProvokingVertex() {
		return glProvokingVertex != 0;
	}

	bool isglFenceSync() {
		return glFenceSync != 0;
	}

	bool isglIsSync() {
		return glIsSync != 0;
	}

	bool isglDeleteSync() {
		return glDeleteSync != 0;
	}

	bool isglClientWaitSync() {
		return glClientWaitSync != 0;
	}

	bool isglWaitSync() {
		return glWaitSync != 0;
	}

	bool isglGetInteger64v() {
		return glGetInteger64v != 0;
	}

	bool isglGetSynciv() {
		return glGetSynciv != 0;
	}

	bool isglGetInteger64i_v() {
		return glGetInteger64i_v != 0;
	}

	bool isglGetBufferParameteri64v() {
		return glGetBufferParameteri64v != 0;
	}

	bool isglFramebufferTexture() {
		return glFramebufferTexture != 0;
	}

	bool isglTexImage2DMultisample() {
		return glTexImage2DMultisample != 0;
	}

	bool isglTexImage3DMultisample() {
		return glTexImage3DMultisample != 0;
	}

	bool isglGetMultisamplefv() {
		return glGetMultisamplefv != 0;
	}

	bool isglSampleMaski() {
		return glSampleMaski != 0;
	}

	bool isglBindFragDataLocationIndexed() {
		return glBindFragDataLocationIndexed != 0;
	}

	bool isglGetFragDataIndex() {
		return glGetFragDataIndex != 0;
	}

	bool isglGenSamplers() {
		return glGenSamplers != 0;
	}

	bool isglDeleteSamplers() {
		return glDeleteSamplers != 0;
	}

	bool isglIsSampler() {
		return glIsSampler != 0;
	}

	bool isglBindSampler() {
		return glBindSampler != 0;
	}

	bool isglSamplerParameteri() {
		return glSamplerParameteri != 0;
	}

	bool isglSamplerParameteriv() {
		return glSamplerParameteriv != 0;
	}

	bool isglSamplerParameterf() {
		return glSamplerParameterf != 0;
	}

	bool isglSamplerParameterfv() {
		return glSamplerParameterfv != 0;
	}

	bool isglSamplerParameterIiv() {
		return glSamplerParameterIiv != 0;
	}

	bool isglSamplerParameterIuiv() {
		return glSamplerParameterIuiv != 0;
	}

	bool isglGetSamplerParameteriv() {
		return glGetSamplerParameteriv != 0;
	}

	bool isglGetSamplerParameterIiv() {
		return glGetSamplerParameterIiv != 0;
	}

	bool isglGetSamplerParameterfv() {
		return glGetSamplerParameterfv != 0;
	}

	bool isglGetSamplerParameterIuiv() {
		return glGetSamplerParameterIuiv != 0;
	}

	bool isglQueryCounter() {
		return glQueryCounter != 0;
	}

	bool isglGetQueryObjecti64v() {
		return glGetQueryObjecti64v != 0;
	}

	bool isglGetQueryObjectui64v() {
		return glGetQueryObjectui64v != 0;
	}

	bool isglVertexAttribDivisor() {
		return glVertexAttribDivisor != 0;
	}

	bool isglVertexAttribP1ui() {
		return glVertexAttribP1ui != 0;
	}

	bool isglVertexAttribP1uiv() {
		return glVertexAttribP1uiv != 0;
	}

	bool isglVertexAttribP2ui() {
		return glVertexAttribP2ui != 0;
	}

	bool isglVertexAttribP2uiv() {
		return glVertexAttribP2uiv != 0;
	}

	bool isglVertexAttribP3ui() {
		return glVertexAttribP3ui != 0;
	}

	bool isglVertexAttribP3uiv() {
		return glVertexAttribP3uiv != 0;
	}

	bool isglVertexAttribP4ui() {
		return glVertexAttribP4ui != 0;
	}

	bool isglVertexAttribP4uiv() {
		return glVertexAttribP4uiv != 0;
	}

	bool isglMinSampleShading() {
		return glMinSampleShading != 0;
	}

	bool isglBlendEquationi() {
		return glBlendEquationi != 0;
	}

	bool isglBlendEquationSeparatei() {
		return glBlendEquationSeparatei != 0;
	}

	bool isglBlendFunci() {
		return glBlendFunci != 0;
	}

	bool isglBlendFuncSeparatei() {
		return glBlendFuncSeparatei != 0;
	}

	bool isglDrawArraysIndirect() {
		return glDrawArraysIndirect != 0;
	}

	bool isglDrawElementsIndirect() {
		return glDrawElementsIndirect != 0;
	}

	bool isglUniform1d() {
		return glUniform1d != 0;
	}

	bool isglUniform2d() {
		return glUniform2d != 0;
	}

	bool isglUniform3d() {
		return glUniform3d != 0;
	}

	bool isglUniform4d() {
		return glUniform4d != 0;
	}

	bool isglUniform1dv() {
		return glUniform1dv != 0;
	}

	bool isglUniform2dv() {
		return glUniform2dv != 0;
	}

	bool isglUniform3dv() {
		return glUniform3dv != 0;
	}

	bool isglUniform4dv() {
		return glUniform4dv != 0;
	}

	bool isglUniformMatrix2dv() {
		return glUniformMatrix2dv != 0;
	}

	bool isglUniformMatrix3dv() {
		return glUniformMatrix3dv != 0;
	}

	bool isglUniformMatrix4dv() {
		return glUniformMatrix4dv != 0;
	}

	bool isglUniformMatrix2x3dv() {
		return glUniformMatrix2x3dv != 0;
	}

	bool isglUniformMatrix2x4dv() {
		return glUniformMatrix2x4dv != 0;
	}

	bool isglUniformMatrix3x2dv() {
		return glUniformMatrix3x2dv != 0;
	}

	bool isglUniformMatrix3x4dv() {
		return glUniformMatrix3x4dv != 0;
	}

	bool isglUniformMatrix4x2dv() {
		return glUniformMatrix4x2dv != 0;
	}

	bool isglUniformMatrix4x3dv() {
		return glUniformMatrix4x3dv != 0;
	}

	bool isglGetUniformdv() {
		return glGetUniformdv != 0;
	}

	bool isglGetSubroutineUniformLocation() {
		return glGetSubroutineUniformLocation != 0;
	}

	bool isglGetSubroutineIndex() {
		return glGetSubroutineIndex != 0;
	}

	bool isglGetActiveSubroutineUniformiv() {
		return glGetActiveSubroutineUniformiv != 0;
	}

	bool isglGetActiveSubroutineUniformName() {
		return glGetActiveSubroutineUniformName != 0;
	}

	bool isglGetActiveSubroutineName() {
		return glGetActiveSubroutineName != 0;
	}

	bool isglUniformSubroutinesuiv() {
		return glUniformSubroutinesuiv != 0;
	}

	bool isglGetUniformSubroutineuiv() {
		return glGetUniformSubroutineuiv != 0;
	}

	bool isglGetProgramStageiv() {
		return glGetProgramStageiv != 0;
	}

	bool isglPatchParameteri() {
		return glPatchParameteri != 0;
	}

	bool isglPatchParameterfv() {
		return glPatchParameterfv != 0;
	}

	bool isglBindTransformFeedback() {
		return glBindTransformFeedback != 0;
	}

	bool isglDeleteTransformFeedbacks() {
		return glDeleteTransformFeedbacks != 0;
	}

	bool isglGenTransformFeedbacks() {
		return glGenTransformFeedbacks != 0;
	}

	bool isglIsTransformFeedback() {
		return glIsTransformFeedback != 0;
	}

	bool isglPauseTransformFeedback() {
		return glPauseTransformFeedback != 0;
	}

	bool isglResumeTransformFeedback() {
		return glResumeTransformFeedback != 0;
	}

	bool isglDrawTransformFeedback() {
		return glDrawTransformFeedback != 0;
	}

	bool isglDrawTransformFeedbackStream() {
		return glDrawTransformFeedbackStream != 0;
	}

	bool isglBeginQueryIndexed() {
		return glBeginQueryIndexed != 0;
	}

	bool isglEndQueryIndexed() {
		return glEndQueryIndexed != 0;
	}

	bool isglGetQueryIndexediv() {
		return glGetQueryIndexediv != 0;
	}

	bool isglReleaseShaderCompiler() {
		return glReleaseShaderCompiler != 0;
	}

	bool isglShaderBinary() {
		return glShaderBinary != 0;
	}

	bool isglGetShaderPrecisionFormat() {
		return glGetShaderPrecisionFormat != 0;
	}

	bool isglDepthRangef() {
		return glDepthRangef != 0;
	}

	bool isglClearDepthf() {
		return glClearDepthf != 0;
	}

	bool isglGetProgramBinary() {
		return glGetProgramBinary != 0;
	}

	bool isglProgramBinary() {
		return glProgramBinary != 0;
	}

	bool isglProgramParameteri() {
		return glProgramParameteri != 0;
	}

	bool isglUseProgramStages() {
		return glUseProgramStages != 0;
	}

	bool isglActiveShaderProgram() {
		return glActiveShaderProgram != 0;
	}

	bool isglCreateShaderProgramv() {
		return glCreateShaderProgramv != 0;
	}

	bool isglBindProgramPipeline() {
		return glBindProgramPipeline != 0;
	}

	bool isglDeleteProgramPipelines() {
		return glDeleteProgramPipelines != 0;
	}

	bool isglGenProgramPipelines() {
		return glGenProgramPipelines != 0;
	}

	bool isglIsProgramPipeline() {
		return glIsProgramPipeline != 0;
	}

	bool isglGetProgramPipelineiv() {
		return glGetProgramPipelineiv != 0;
	}

	bool isglProgramUniform1i() {
		return glProgramUniform1i != 0;
	}

	bool isglProgramUniform1iv() {
		return glProgramUniform1iv != 0;
	}

	bool isglProgramUniform1f() {
		return glProgramUniform1f != 0;
	}

	bool isglProgramUniform1fv() {
		return glProgramUniform1fv != 0;
	}

	bool isglProgramUniform1d() {
		return glProgramUniform1d != 0;
	}

	bool isglProgramUniform1dv() {
		return glProgramUniform1dv != 0;
	}

	bool isglProgramUniform1ui() {
		return glProgramUniform1ui != 0;
	}

	bool isglProgramUniform1uiv() {
		return glProgramUniform1uiv != 0;
	}

	bool isglProgramUniform2i() {
		return glProgramUniform2i != 0;
	}

	bool isglProgramUniform2iv() {
		return glProgramUniform2iv != 0;
	}

	bool isglProgramUniform2f() {
		return glProgramUniform2f != 0;
	}

	bool isglProgramUniform2fv() {
		return glProgramUniform2fv != 0;
	}

	bool isglProgramUniform2d() {
		return glProgramUniform2d != 0;
	}

	bool isglProgramUniform2dv() {
		return glProgramUniform2dv != 0;
	}

	bool isglProgramUniform2ui() {
		return glProgramUniform2ui != 0;
	}

	bool isglProgramUniform2uiv() {
		return glProgramUniform2uiv != 0;
	}

	bool isglProgramUniform3i() {
		return glProgramUniform3i != 0;
	}

	bool isglProgramUniform3iv() {
		return glProgramUniform3iv != 0;
	}

	bool isglProgramUniform3f() {
		return glProgramUniform3f != 0;
	}

	bool isglProgramUniform3fv() {
		return glProgramUniform3fv != 0;
	}

	bool isglProgramUniform3d() {
		return glProgramUniform3d != 0;
	}

	bool isglProgramUniform3dv() {
		return glProgramUniform3dv != 0;
	}

	bool isglProgramUniform3ui() {
		return glProgramUniform3ui != 0;
	}

	bool isglProgramUniform3uiv() {
		return glProgramUniform3uiv != 0;
	}

	bool isglProgramUniform4i() {
		return glProgramUniform4i != 0;
	}

	bool isglProgramUniform4iv() {
		return glProgramUniform4iv != 0;
	}

	bool isglProgramUniform4f() {
		return glProgramUniform4f != 0;
	}

	bool isglProgramUniform4fv() {
		return glProgramUniform4fv != 0;
	}

	bool isglProgramUniform4d() {
		return glProgramUniform4d != 0;
	}

	bool isglProgramUniform4dv() {
		return glProgramUniform4dv != 0;
	}

	bool isglProgramUniform4ui() {
		return glProgramUniform4ui != 0;
	}

	bool isglProgramUniform4uiv() {
		return glProgramUniform4uiv != 0;
	}

	bool isglProgramUniformMatrix2fv() {
		return glProgramUniformMatrix2fv != 0;
	}

	bool isglProgramUniformMatrix3fv() {
		return glProgramUniformMatrix3fv != 0;
	}

	bool isglProgramUniformMatrix4fv() {
		return glProgramUniformMatrix4fv != 0;
	}

	bool isglProgramUniformMatrix2dv() {
		return glProgramUniformMatrix2dv != 0;
	}

	bool isglProgramUniformMatrix3dv() {
		return glProgramUniformMatrix3dv != 0;
	}

	bool isglProgramUniformMatrix4dv() {
		return glProgramUniformMatrix4dv != 0;
	}

	bool isglProgramUniformMatrix2x3fv() {
		return glProgramUniformMatrix2x3fv != 0;
	}

	bool isglProgramUniformMatrix3x2fv() {
		return glProgramUniformMatrix3x2fv != 0;
	}

	bool isglProgramUniformMatrix2x4fv() {
		return glProgramUniformMatrix2x4fv != 0;
	}

	bool isglProgramUniformMatrix4x2fv() {
		return glProgramUniformMatrix4x2fv != 0;
	}

	bool isglProgramUniformMatrix3x4fv() {
		return glProgramUniformMatrix3x4fv != 0;
	}

	bool isglProgramUniformMatrix4x3fv() {
		return glProgramUniformMatrix4x3fv != 0;
	}

	bool isglProgramUniformMatrix2x3dv() {
		return glProgramUniformMatrix2x3dv != 0;
	}

	bool isglProgramUniformMatrix3x2dv() {
		return glProgramUniformMatrix3x2dv != 0;
	}

	bool isglProgramUniformMatrix2x4dv() {
		return glProgramUniformMatrix2x4dv != 0;
	}

	bool isglProgramUniformMatrix4x2dv() {
		return glProgramUniformMatrix4x2dv != 0;
	}

	bool isglProgramUniformMatrix3x4dv() {
		return glProgramUniformMatrix3x4dv != 0;
	}

	bool isglProgramUniformMatrix4x3dv() {
		return glProgramUniformMatrix4x3dv != 0;
	}

	bool isglValidateProgramPipeline() {
		return glValidateProgramPipeline != 0;
	}

	bool isglGetProgramPipelineInfoLog() {
		return glGetProgramPipelineInfoLog != 0;
	}

	bool isglVertexAttribL1d() {
		return glVertexAttribL1d != 0;
	}

	bool isglVertexAttribL2d() {
		return glVertexAttribL2d != 0;
	}

	bool isglVertexAttribL3d() {
		return glVertexAttribL3d != 0;
	}

	bool isglVertexAttribL4d() {
		return glVertexAttribL4d != 0;
	}

	bool isglVertexAttribL1dv() {
		return glVertexAttribL1dv != 0;
	}

	bool isglVertexAttribL2dv() {
		return glVertexAttribL2dv != 0;
	}

	bool isglVertexAttribL3dv() {
		return glVertexAttribL3dv != 0;
	}

	bool isglVertexAttribL4dv() {
		return glVertexAttribL4dv != 0;
	}

	bool isglVertexAttribLPointer() {
		return glVertexAttribLPointer != 0;
	}

	bool isglGetVertexAttribLdv() {
		return glGetVertexAttribLdv != 0;
	}

	bool isglViewportArrayv() {
		return glViewportArrayv != 0;
	}

	bool isglViewportIndexedf() {
		return glViewportIndexedf != 0;
	}

	bool isglViewportIndexedfv() {
		return glViewportIndexedfv != 0;
	}

	bool isglScissorArrayv() {
		return glScissorArrayv != 0;
	}

	bool isglScissorIndexed() {
		return glScissorIndexed != 0;
	}

	bool isglScissorIndexedv() {
		return glScissorIndexedv != 0;
	}

	bool isglDepthRangeArrayv() {
		return glDepthRangeArrayv != 0;
	}

	bool isglDepthRangeIndexed() {
		return glDepthRangeIndexed != 0;
	}

	bool isglGetFloati_v() {
		return glGetFloati_v != 0;
	}

	bool isglGetDoublei_v() {
		return glGetDoublei_v != 0;
	}

	bool isglDrawArraysInstancedBaseInstance() {
		return glDrawArraysInstancedBaseInstance != 0;
	}

	bool isglDrawElementsInstancedBaseInstance() {
		return glDrawElementsInstancedBaseInstance != 0;
	}

	bool isglDrawElementsInstancedBaseVertexBaseInstance() {
		return glDrawElementsInstancedBaseVertexBaseInstance != 0;
	}

	bool isglGetInternalformativ() {
		return glGetInternalformativ != 0;
	}

	bool isglGetActiveAtomicCounterBufferiv() {
		return glGetActiveAtomicCounterBufferiv != 0;
	}

	bool isglBindImageTexture() {
		return glBindImageTexture != 0;
	}

	bool isglMemoryBarrier() {
		return glMemoryBarrier != 0;
	}

	bool isglTexStorage1D() {
		return glTexStorage1D != 0;
	}

	bool isglTexStorage2D() {
		return glTexStorage2D != 0;
	}

	bool isglTexStorage3D() {
		return glTexStorage3D != 0;
	}

	bool isglDrawTransformFeedbackInstanced() {
		return glDrawTransformFeedbackInstanced != 0;
	}

	bool isglDrawTransformFeedbackStreamInstanced() {
		return glDrawTransformFeedbackStreamInstanced != 0;
	}

	bool isglClearBufferData() {
		return glClearBufferData != 0;
	}

	bool isglClearBufferSubData() {
		return glClearBufferSubData != 0;
	}

	bool isglDispatchCompute() {
		return glDispatchCompute != 0;
	}

	bool isglDispatchComputeIndirect() {
		return glDispatchComputeIndirect != 0;
	}

	bool isglCopyImageSubData() {
		return glCopyImageSubData != 0;
	}

	bool isglFramebufferParameteri() {
		return glFramebufferParameteri != 0;
	}

	bool isglGetFramebufferParameteriv() {
		return glGetFramebufferParameteriv != 0;
	}

	bool isglGetInternalformati64v() {
		return glGetInternalformati64v != 0;
	}

	bool isglInvalidateTexSubImage() {
		return glInvalidateTexSubImage != 0;
	}

	bool isglInvalidateTexImage() {
		return glInvalidateTexImage != 0;
	}

	bool isglInvalidateBufferSubData() {
		return glInvalidateBufferSubData != 0;
	}

	bool isglInvalidateBufferData() {
		return glInvalidateBufferData != 0;
	}

	bool isglInvalidateFramebuffer() {
		return glInvalidateFramebuffer != 0;
	}

	bool isglInvalidateSubFramebuffer() {
		return glInvalidateSubFramebuffer != 0;
	}

	bool isglMultiDrawArraysIndirect() {
		return glMultiDrawArraysIndirect != 0;
	}

	bool isglMultiDrawElementsIndirect() {
		return glMultiDrawElementsIndirect != 0;
	}

	bool isglGetProgramInterfaceiv() {
		return glGetProgramInterfaceiv != 0;
	}

	bool isglGetProgramResourceIndex() {
		return glGetProgramResourceIndex != 0;
	}

	bool isglGetProgramResourceName() {
		return glGetProgramResourceName != 0;
	}

	bool isglGetProgramResourceiv() {
		return glGetProgramResourceiv != 0;
	}

	bool isglGetProgramResourceLocation() {
		return glGetProgramResourceLocation != 0;
	}

	bool isglGetProgramResourceLocationIndex() {
		return glGetProgramResourceLocationIndex != 0;
	}

	bool isglShaderStorageBlockBinding() {
		return glShaderStorageBlockBinding != 0;
	}

	bool isglTexBufferRange() {
		return glTexBufferRange != 0;
	}

	bool isglTexStorage2DMultisample() {
		return glTexStorage2DMultisample != 0;
	}

	bool isglTexStorage3DMultisample() {
		return glTexStorage3DMultisample != 0;
	}

	bool isglTextureView() {
		return glTextureView != 0;
	}

	bool isglBindVertexBuffer() {
		return glBindVertexBuffer != 0;
	}

	bool isglVertexAttribFormat() {
		return glVertexAttribFormat != 0;
	}

	bool isglVertexAttribIFormat() {
		return glVertexAttribIFormat != 0;
	}

	bool isglVertexAttribLFormat() {
		return glVertexAttribLFormat != 0;
	}

	bool isglVertexAttribBinding() {
		return glVertexAttribBinding != 0;
	}

	bool isglVertexBindingDivisor() {
		return glVertexBindingDivisor != 0;
	}

	bool isglDebugMessageControl() {
		return glDebugMessageControl != 0;
	}

	bool isglDebugMessageInsert() {
		return glDebugMessageInsert != 0;
	}

	bool isglDebugMessageCallback() {
		return glDebugMessageCallback != 0;
	}

	bool isglGetDebugMessageLog() {
		return glGetDebugMessageLog != 0;
	}

	bool isglPushDebugGroup() {
		return glPushDebugGroup != 0;
	}

	bool isglPopDebugGroup() {
		return glPopDebugGroup != 0;
	}

	bool isglObjectLabel() {
		return glObjectLabel != 0;
	}

	bool isglGetObjectLabel() {
		return glGetObjectLabel != 0;
	}

	bool isglObjectPtrLabel() {
		return glObjectPtrLabel != 0;
	}

	bool isglGetObjectPtrLabel() {
		return glGetObjectPtrLabel != 0;
	}

	bool isglBufferStorage() {
		return glBufferStorage != 0;
	}

	bool isglClearTexImage() {
		return glClearTexImage != 0;
	}

	bool isglClearTexSubImage() {
		return glClearTexSubImage != 0;
	}

	bool isglBindBuffersBase() {
		return glBindBuffersBase != 0;
	}

	bool isglBindBuffersRange() {
		return glBindBuffersRange != 0;
	}

	bool isglBindTextures() {
		return glBindTextures != 0;
	}

	bool isglBindSamplers() {
		return glBindSamplers != 0;
	}

	bool isglBindImageTextures() {
		return glBindImageTextures != 0;
	}

	bool isglBindVertexBuffers() {
		return glBindVertexBuffers != 0;
	}

	bool isglClipControl() {
		return glClipControl != 0;
	}

	bool isglCreateTransformFeedbacks() {
		return glCreateTransformFeedbacks != 0;
	}

	bool isglTransformFeedbackBufferBase() {
		return glTransformFeedbackBufferBase != 0;
	}

	bool isglTransformFeedbackBufferRange() {
		return glTransformFeedbackBufferRange != 0;
	}

	bool isglGetTransformFeedbackiv() {
		return glGetTransformFeedbackiv != 0;
	}

	bool isglGetTransformFeedbacki_v() {
		return glGetTransformFeedbacki_v != 0;
	}

	bool isglGetTransformFeedbacki64_v() {
		return glGetTransformFeedbacki64_v != 0;
	}

	bool isglCreateBuffers() {
		return glCreateBuffers != 0;
	}

	bool isglNamedBufferStorage() {
		return glNamedBufferStorage != 0;
	}

	bool isglNamedBufferData() {
		return glNamedBufferData != 0;
	}

	bool isglNamedBufferSubData() {
		return glNamedBufferSubData != 0;
	}

	bool isglCopyNamedBufferSubData() {
		return glCopyNamedBufferSubData != 0;
	}

	bool isglClearNamedBufferData() {
		return glClearNamedBufferData != 0;
	}

	bool isglClearNamedBufferSubData() {
		return glClearNamedBufferSubData != 0;
	}

	bool isglMapNamedBuffer() {
		return glMapNamedBuffer != 0;
	}

	bool isglMapNamedBufferRange() {
		return glMapNamedBufferRange != 0;
	}

	bool isglUnmapNamedBuffer() {
		return glUnmapNamedBuffer != 0;
	}

	bool isglFlushMappedNamedBufferRange() {
		return glFlushMappedNamedBufferRange != 0;
	}

	bool isglGetNamedBufferParameteriv() {
		return glGetNamedBufferParameteriv != 0;
	}

	bool isglGetNamedBufferParameteri64v() {
		return glGetNamedBufferParameteri64v != 0;
	}

	bool isglGetNamedBufferPointerv() {
		return glGetNamedBufferPointerv != 0;
	}

	bool isglGetNamedBufferSubData() {
		return glGetNamedBufferSubData != 0;
	}

	bool isglCreateFramebuffers() {
		return glCreateFramebuffers != 0;
	}

	bool isglNamedFramebufferRenderbuffer() {
		return glNamedFramebufferRenderbuffer != 0;
	}

	bool isglNamedFramebufferParameteri() {
		return glNamedFramebufferParameteri != 0;
	}

	bool isglNamedFramebufferTexture() {
		return glNamedFramebufferTexture != 0;
	}

	bool isglNamedFramebufferTextureLayer() {
		return glNamedFramebufferTextureLayer != 0;
	}

	bool isglNamedFramebufferDrawBuffer() {
		return glNamedFramebufferDrawBuffer != 0;
	}

	bool isglNamedFramebufferDrawBuffers() {
		return glNamedFramebufferDrawBuffers != 0;
	}

	bool isglNamedFramebufferReadBuffer() {
		return glNamedFramebufferReadBuffer != 0;
	}

	bool isglInvalidateNamedFramebufferData() {
		return glInvalidateNamedFramebufferData != 0;
	}

	bool isglInvalidateNamedFramebufferSubData() {
		return glInvalidateNamedFramebufferSubData != 0;
	}

	bool isglClearNamedFramebufferiv() {
		return glClearNamedFramebufferiv != 0;
	}

	bool isglClearNamedFramebufferuiv() {
		return glClearNamedFramebufferuiv != 0;
	}

	bool isglClearNamedFramebufferfv() {
		return glClearNamedFramebufferfv != 0;
	}

	bool isglClearNamedFramebufferfi() {
		return glClearNamedFramebufferfi != 0;
	}

	bool isglBlitNamedFramebuffer() {
		return glBlitNamedFramebuffer != 0;
	}

	bool isglCheckNamedFramebufferStatus() {
		return glCheckNamedFramebufferStatus != 0;
	}

	bool isglGetNamedFramebufferParameteriv() {
		return glGetNamedFramebufferParameteriv != 0;
	}

	bool isglGetNamedFramebufferAttachmentParameteriv() {
		return glGetNamedFramebufferAttachmentParameteriv != 0;
	}

	bool isglCreateRenderbuffers() {
		return glCreateRenderbuffers != 0;
	}

	bool isglNamedRenderbufferStorage() {
		return glNamedRenderbufferStorage != 0;
	}

	bool isglNamedRenderbufferStorageMultisample() {
		return glNamedRenderbufferStorageMultisample != 0;
	}

	bool isglGetNamedRenderbufferParameteriv() {
		return glGetNamedRenderbufferParameteriv != 0;
	}

	bool isglCreateTextures() {
		return glCreateTextures != 0;
	}

	bool isglTextureBuffer() {
		return glTextureBuffer != 0;
	}

	bool isglTextureBufferRange() {
		return glTextureBufferRange != 0;
	}

	bool isglTextureStorage1D() {
		return glTextureStorage1D != 0;
	}

	bool isglTextureStorage2D() {
		return glTextureStorage2D != 0;
	}

	bool isglTextureStorage3D() {
		return glTextureStorage3D != 0;
	}

	bool isglTextureStorage2DMultisample() {
		return glTextureStorage2DMultisample != 0;
	}

	bool isglTextureStorage3DMultisample() {
		return glTextureStorage3DMultisample != 0;
	}

	bool isglTextureSubImage1D() {
		return glTextureSubImage1D != 0;
	}

	bool isglTextureSubImage2D() {
		return glTextureSubImage2D != 0;
	}

	bool isglTextureSubImage3D() {
		return glTextureSubImage3D != 0;
	}

	bool isglCompressedTextureSubImage1D() {
		return glCompressedTextureSubImage1D != 0;
	}

	bool isglCompressedTextureSubImage2D() {
		return glCompressedTextureSubImage2D != 0;
	}

	bool isglCompressedTextureSubImage3D() {
		return glCompressedTextureSubImage3D != 0;
	}

	bool isglCopyTextureSubImage1D() {
		return glCopyTextureSubImage1D != 0;
	}

	bool isglCopyTextureSubImage2D() {
		return glCopyTextureSubImage2D != 0;
	}

	bool isglCopyTextureSubImage3D() {
		return glCopyTextureSubImage3D != 0;
	}

	bool isglTextureParameterf() {
		return glTextureParameterf != 0;
	}

	bool isglTextureParameterfv() {
		return glTextureParameterfv != 0;
	}

	bool isglTextureParameteri() {
		return glTextureParameteri != 0;
	}

	bool isglTextureParameterIiv() {
		return glTextureParameterIiv != 0;
	}

	bool isglTextureParameterIuiv() {
		return glTextureParameterIuiv != 0;
	}

	bool isglTextureParameteriv() {
		return glTextureParameteriv != 0;
	}

	bool isglGenerateTextureMipmap() {
		return glGenerateTextureMipmap != 0;
	}

	bool isglBindTextureUnit() {
		return glBindTextureUnit != 0;
	}

	bool isglGetTextureImage() {
		return glGetTextureImage != 0;
	}

	bool isglGetCompressedTextureImage() {
		return glGetCompressedTextureImage != 0;
	}

	bool isglGetTextureLevelParameterfv() {
		return glGetTextureLevelParameterfv != 0;
	}

	bool isglGetTextureLevelParameteriv() {
		return glGetTextureLevelParameteriv != 0;
	}

	bool isglGetTextureParameterfv() {
		return glGetTextureParameterfv != 0;
	}

	bool isglGetTextureParameterIiv() {
		return glGetTextureParameterIiv != 0;
	}

	bool isglGetTextureParameterIuiv() {
		return glGetTextureParameterIuiv != 0;
	}

	bool isglGetTextureParameteriv() {
		return glGetTextureParameteriv != 0;
	}

	bool isglCreateVertexArrays() {
		return glCreateVertexArrays != 0;
	}

	bool isglDisableVertexArrayAttrib() {
		return glDisableVertexArrayAttrib != 0;
	}

	bool isglEnableVertexArrayAttrib() {
		return glEnableVertexArrayAttrib != 0;
	}

	bool isglVertexArrayElementBuffer() {
		return glVertexArrayElementBuffer != 0;
	}

	bool isglVertexArrayVertexBuffer() {
		return glVertexArrayVertexBuffer != 0;
	}

	bool isglVertexArrayVertexBuffers() {
		return glVertexArrayVertexBuffers != 0;
	}

	bool isglVertexArrayAttribBinding() {
		return glVertexArrayAttribBinding != 0;
	}

	bool isglVertexArrayAttribFormat() {
		return glVertexArrayAttribFormat != 0;
	}

	bool isglVertexArrayAttribIFormat() {
		return glVertexArrayAttribIFormat != 0;
	}

	bool isglVertexArrayAttribLFormat() {
		return glVertexArrayAttribLFormat != 0;
	}

	bool isglVertexArrayBindingDivisor() {
		return glVertexArrayBindingDivisor != 0;
	}

	bool isglGetVertexArrayiv() {
		return glGetVertexArrayiv != 0;
	}

	bool isglGetVertexArrayIndexediv() {
		return glGetVertexArrayIndexediv != 0;
	}

	bool isglGetVertexArrayIndexed64iv() {
		return glGetVertexArrayIndexed64iv != 0;
	}

	bool isglCreateSamplers() {
		return glCreateSamplers != 0;
	}

	bool isglCreateProgramPipelines() {
		return glCreateProgramPipelines != 0;
	}

	bool isglCreateQueries() {
		return glCreateQueries != 0;
	}

	bool isglGetQueryBufferObjecti64v() {
		return glGetQueryBufferObjecti64v != 0;
	}

	bool isglGetQueryBufferObjectiv() {
		return glGetQueryBufferObjectiv != 0;
	}

	bool isglGetQueryBufferObjectui64v() {
		return glGetQueryBufferObjectui64v != 0;
	}

	bool isglGetQueryBufferObjectuiv() {
		return glGetQueryBufferObjectuiv != 0;
	}

	bool isglMemoryBarrierByRegion() {
		return glMemoryBarrierByRegion != 0;
	}

	bool isglGetTextureSubImage() {
		return glGetTextureSubImage != 0;
	}

	bool isglGetCompressedTextureSubImage() {
		return glGetCompressedTextureSubImage != 0;
	}

	bool isglGetGraphicsResetStatus() {
		return glGetGraphicsResetStatus != 0;
	}

	bool isglGetnCompressedTexImage() {
		return glGetnCompressedTexImage != 0;
	}

	bool isglGetnTexImage() {
		return glGetnTexImage != 0;
	}

	bool isglGetnUniformdv() {
		return glGetnUniformdv != 0;
	}

	bool isglGetnUniformfv() {
		return glGetnUniformfv != 0;
	}

	bool isglGetnUniformiv() {
		return glGetnUniformiv != 0;
	}

	bool isglGetnUniformuiv() {
		return glGetnUniformuiv != 0;
	}

	bool isglReadnPixels() {
		return glReadnPixels != 0;
	}

	bool isglTextureBarrier() {
		return glTextureBarrier != 0;
	}


	PROC_glCullFace glCullFace;
	PROC_glFrontFace glFrontFace;
	PROC_glHint glHint;
	PROC_glLineWidth glLineWidth;
	PROC_glPointSize glPointSize;
	PROC_glPolygonMode glPolygonMode;
	PROC_glScissor glScissor;
	PROC_glTexParameterf glTexParameterf;
	PROC_glTexParameterfv glTexParameterfv;
	PROC_glTexParameteri glTexParameteri;
	PROC_glTexParameteriv glTexParameteriv;
	PROC_glTexImage1D glTexImage1D;
	PROC_glTexImage2D glTexImage2D;
	PROC_glDrawBuffer glDrawBuffer;
	PROC_glClear glClear;
	PROC_glClearColor glClearColor;
	PROC_glClearStencil glClearStencil;
	PROC_glClearDepth glClearDepth;
	PROC_glStencilMask glStencilMask;
	PROC_glColorMask glColorMask;
	PROC_glDepthMask glDepthMask;
	PROC_glDisable glDisable;
	PROC_glEnable glEnable;
	PROC_glFinish glFinish;
	PROC_glFlush glFlush;
	PROC_glBlendFunc glBlendFunc;
	PROC_glLogicOp glLogicOp;
	PROC_glStencilFunc glStencilFunc;
	PROC_glStencilOp glStencilOp;
	PROC_glDepthFunc glDepthFunc;
	PROC_glPixelStoref glPixelStoref;
	PROC_glPixelStorei glPixelStorei;
	PROC_glReadBuffer glReadBuffer;
	PROC_glReadPixels glReadPixels;
	PROC_glGetBooleanv glGetBooleanv;
	PROC_glGetDoublev glGetDoublev;
	PROC_glGetError glGetError;
	PROC_glGetFloatv glGetFloatv;
	PROC_glGetIntegerv glGetIntegerv;
	PROC_glGetString glGetString;
	PROC_glGetTexImage glGetTexImage;
	PROC_glGetTexParameterfv glGetTexParameterfv;
	PROC_glGetTexParameteriv glGetTexParameteriv;
	PROC_glGetTexLevelParameterfv glGetTexLevelParameterfv;
	PROC_glGetTexLevelParameteriv glGetTexLevelParameteriv;
	PROC_glIsEnabled glIsEnabled;
	PROC_glDepthRange glDepthRange;
	PROC_glViewport glViewport;
	PROC_glDrawArrays glDrawArrays;
	PROC_glDrawElements glDrawElements;
	PROC_glGetPointerv glGetPointerv;
	PROC_glPolygonOffset glPolygonOffset;
	PROC_glCopyTexImage1D glCopyTexImage1D;
	PROC_glCopyTexImage2D glCopyTexImage2D;
	PROC_glCopyTexSubImage1D glCopyTexSubImage1D;
	PROC_glCopyTexSubImage2D glCopyTexSubImage2D;
	PROC_glTexSubImage1D glTexSubImage1D;
	PROC_glTexSubImage2D glTexSubImage2D;
	PROC_glBindTexture glBindTexture;
	PROC_glDeleteTextures glDeleteTextures;
	PROC_glGenTextures glGenTextures;
	PROC_glIsTexture glIsTexture;
	PROC_glDrawRangeElements glDrawRangeElements;
	PROC_glTexImage3D glTexImage3D;
	PROC_glTexSubImage3D glTexSubImage3D;
	PROC_glCopyTexSubImage3D glCopyTexSubImage3D;
	PROC_glActiveTexture glActiveTexture;
	PROC_glSampleCoverage glSampleCoverage;
	PROC_glCompressedTexImage3D glCompressedTexImage3D;
	PROC_glCompressedTexImage2D glCompressedTexImage2D;
	PROC_glCompressedTexImage1D glCompressedTexImage1D;
	PROC_glCompressedTexSubImage3D glCompressedTexSubImage3D;
	PROC_glCompressedTexSubImage2D glCompressedTexSubImage2D;
	PROC_glCompressedTexSubImage1D glCompressedTexSubImage1D;
	PROC_glGetCompressedTexImage glGetCompressedTexImage;
	PROC_glBlendFuncSeparate glBlendFuncSeparate;
	PROC_glMultiDrawArrays glMultiDrawArrays;
	PROC_glMultiDrawElements glMultiDrawElements;
	PROC_glPointParameterf glPointParameterf;
	PROC_glPointParameterfv glPointParameterfv;
	PROC_glPointParameteri glPointParameteri;
	PROC_glPointParameteriv glPointParameteriv;
	PROC_glBlendColor glBlendColor;
	PROC_glBlendEquation glBlendEquation;
	PROC_glGenQueries glGenQueries;
	PROC_glDeleteQueries glDeleteQueries;
	PROC_glIsQuery glIsQuery;
	PROC_glBeginQuery glBeginQuery;
	PROC_glEndQuery glEndQuery;
	PROC_glGetQueryiv glGetQueryiv;
	PROC_glGetQueryObjectiv glGetQueryObjectiv;
	PROC_glGetQueryObjectuiv glGetQueryObjectuiv;
	PROC_glBindBuffer glBindBuffer;
	PROC_glDeleteBuffers glDeleteBuffers;
	PROC_glGenBuffers glGenBuffers;
	PROC_glIsBuffer glIsBuffer;
	PROC_glBufferData glBufferData;
	PROC_glBufferSubData glBufferSubData;
	PROC_glGetBufferSubData glGetBufferSubData;
	PROC_glMapBuffer glMapBuffer;
	PROC_glUnmapBuffer glUnmapBuffer;
	PROC_glGetBufferParameteriv glGetBufferParameteriv;
	PROC_glGetBufferPointerv glGetBufferPointerv;
	PROC_glBlendEquationSeparate glBlendEquationSeparate;
	PROC_glDrawBuffers glDrawBuffers;
	PROC_glStencilOpSeparate glStencilOpSeparate;
	PROC_glStencilFuncSeparate glStencilFuncSeparate;
	PROC_glStencilMaskSeparate glStencilMaskSeparate;
	PROC_glAttachShader glAttachShader;
	PROC_glBindAttribLocation glBindAttribLocation;
	PROC_glCompileShader glCompileShader;
	PROC_glCreateProgram glCreateProgram;
	PROC_glCreateShader glCreateShader;
	PROC_glDeleteProgram glDeleteProgram;
	PROC_glDeleteShader glDeleteShader;
	PROC_glDetachShader glDetachShader;
	PROC_glDisableVertexAttribArray glDisableVertexAttribArray;
	PROC_glEnableVertexAttribArray glEnableVertexAttribArray;
	PROC_glGetActiveAttrib glGetActiveAttrib;
	PROC_glGetActiveUniform glGetActiveUniform;
	PROC_glGetAttachedShaders glGetAttachedShaders;
	PROC_glGetAttribLocation glGetAttribLocation;
	PROC_glGetProgramiv glGetProgramiv;
	PROC_glGetProgramInfoLog glGetProgramInfoLog;
	PROC_glGetShaderiv glGetShaderiv;
	PROC_glGetShaderInfoLog glGetShaderInfoLog;
	PROC_glGetShaderSource glGetShaderSource;
	PROC_glGetUniformLocation glGetUniformLocation;
	PROC_glGetUniformfv glGetUniformfv;
	PROC_glGetUniformiv glGetUniformiv;
	PROC_glGetVertexAttribdv glGetVertexAttribdv;
	PROC_glGetVertexAttribfv glGetVertexAttribfv;
	PROC_glGetVertexAttribiv glGetVertexAttribiv;
	PROC_glGetVertexAttribPointerv glGetVertexAttribPointerv;
	PROC_glIsProgram glIsProgram;
	PROC_glIsShader glIsShader;
	PROC_glLinkProgram glLinkProgram;
	PROC_glShaderSource glShaderSource;
	PROC_glUseProgram glUseProgram;
	PROC_glUniform1f glUniform1f;
	PROC_glUniform2f glUniform2f;
	PROC_glUniform3f glUniform3f;
	PROC_glUniform4f glUniform4f;
	PROC_glUniform1i glUniform1i;
	PROC_glUniform2i glUniform2i;
	PROC_glUniform3i glUniform3i;
	PROC_glUniform4i glUniform4i;
	PROC_glUniform1fv glUniform1fv;
	PROC_glUniform2fv glUniform2fv;
	PROC_glUniform3fv glUniform3fv;
	PROC_glUniform4fv glUniform4fv;
	PROC_glUniform1iv glUniform1iv;
	PROC_glUniform2iv glUniform2iv;
	PROC_glUniform3iv glUniform3iv;
	PROC_glUniform4iv glUniform4iv;
	PROC_glUniformMatrix2fv glUniformMatrix2fv;
	PROC_glUniformMatrix3fv glUniformMatrix3fv;
	PROC_glUniformMatrix4fv glUniformMatrix4fv;
	PROC_glValidateProgram glValidateProgram;
	PROC_glVertexAttrib1d glVertexAttrib1d;
	PROC_glVertexAttrib1dv glVertexAttrib1dv;
	PROC_glVertexAttrib1f glVertexAttrib1f;
	PROC_glVertexAttrib1fv glVertexAttrib1fv;
	PROC_glVertexAttrib1s glVertexAttrib1s;
	PROC_glVertexAttrib1sv glVertexAttrib1sv;
	PROC_glVertexAttrib2d glVertexAttrib2d;
	PROC_glVertexAttrib2dv glVertexAttrib2dv;
	PROC_glVertexAttrib2f glVertexAttrib2f;
	PROC_glVertexAttrib2fv glVertexAttrib2fv;
	PROC_glVertexAttrib2s glVertexAttrib2s;
	PROC_glVertexAttrib2sv glVertexAttrib2sv;
	PROC_glVertexAttrib3d glVertexAttrib3d;
	PROC_glVertexAttrib3dv glVertexAttrib3dv;
	PROC_glVertexAttrib3f glVertexAttrib3f;
	PROC_glVertexAttrib3fv glVertexAttrib3fv;
	PROC_glVertexAttrib3s glVertexAttrib3s;
	PROC_glVertexAttrib3sv glVertexAttrib3sv;
	PROC_glVertexAttrib4Nbv glVertexAttrib4Nbv;
	PROC_glVertexAttrib4Niv glVertexAttrib4Niv;
	PROC_glVertexAttrib4Nsv glVertexAttrib4Nsv;
	PROC_glVertexAttrib4Nub glVertexAttrib4Nub;
	PROC_glVertexAttrib4Nubv glVertexAttrib4Nubv;
	PROC_glVertexAttrib4Nuiv glVertexAttrib4Nuiv;
	PROC_glVertexAttrib4Nusv glVertexAttrib4Nusv;
	PROC_glVertexAttrib4bv glVertexAttrib4bv;
	PROC_glVertexAttrib4d glVertexAttrib4d;
	PROC_glVertexAttrib4dv glVertexAttrib4dv;
	PROC_glVertexAttrib4f glVertexAttrib4f;
	PROC_glVertexAttrib4fv glVertexAttrib4fv;
	PROC_glVertexAttrib4iv glVertexAttrib4iv;
	PROC_glVertexAttrib4s glVertexAttrib4s;
	PROC_glVertexAttrib4sv glVertexAttrib4sv;
	PROC_glVertexAttrib4ubv glVertexAttrib4ubv;
	PROC_glVertexAttrib4uiv glVertexAttrib4uiv;
	PROC_glVertexAttrib4usv glVertexAttrib4usv;
	PROC_glVertexAttribPointer glVertexAttribPointer;
	PROC_glUniformMatrix2x3fv glUniformMatrix2x3fv;
	PROC_glUniformMatrix3x2fv glUniformMatrix3x2fv;
	PROC_glUniformMatrix2x4fv glUniformMatrix2x4fv;
	PROC_glUniformMatrix4x2fv glUniformMatrix4x2fv;
	PROC_glUniformMatrix3x4fv glUniformMatrix3x4fv;
	PROC_glUniformMatrix4x3fv glUniformMatrix4x3fv;
	PROC_glColorMaski glColorMaski;
	PROC_glGetBooleani_v glGetBooleani_v;
	PROC_glGetIntegeri_v glGetIntegeri_v;
	PROC_glEnablei glEnablei;
	PROC_glDisablei glDisablei;
	PROC_glIsEnabledi glIsEnabledi;
	PROC_glBeginTransformFeedback glBeginTransformFeedback;
	PROC_glEndTransformFeedback glEndTransformFeedback;
	PROC_glBindBufferRange glBindBufferRange;
	PROC_glBindBufferBase glBindBufferBase;
	PROC_glTransformFeedbackVaryings glTransformFeedbackVaryings;
	PROC_glGetTransformFeedbackVarying glGetTransformFeedbackVarying;
	PROC_glClampColor glClampColor;
	PROC_glBeginConditionalRender glBeginConditionalRender;
	PROC_glEndConditionalRender glEndConditionalRender;
	PROC_glVertexAttribIPointer glVertexAttribIPointer;
	PROC_glGetVertexAttribIiv glGetVertexAttribIiv;
	PROC_glGetVertexAttribIuiv glGetVertexAttribIuiv;
	PROC_glVertexAttribI1i glVertexAttribI1i;
	PROC_glVertexAttribI2i glVertexAttribI2i;
	PROC_glVertexAttribI3i glVertexAttribI3i;
	PROC_glVertexAttribI4i glVertexAttribI4i;
	PROC_glVertexAttribI1ui glVertexAttribI1ui;
	PROC_glVertexAttribI2ui glVertexAttribI2ui;
	PROC_glVertexAttribI3ui glVertexAttribI3ui;
	PROC_glVertexAttribI4ui glVertexAttribI4ui;
	PROC_glVertexAttribI1iv glVertexAttribI1iv;
	PROC_glVertexAttribI2iv glVertexAttribI2iv;
	PROC_glVertexAttribI3iv glVertexAttribI3iv;
	PROC_glVertexAttribI4iv glVertexAttribI4iv;
	PROC_glVertexAttribI1uiv glVertexAttribI1uiv;
	PROC_glVertexAttribI2uiv glVertexAttribI2uiv;
	PROC_glVertexAttribI3uiv glVertexAttribI3uiv;
	PROC_glVertexAttribI4uiv glVertexAttribI4uiv;
	PROC_glVertexAttribI4bv glVertexAttribI4bv;
	PROC_glVertexAttribI4sv glVertexAttribI4sv;
	PROC_glVertexAttribI4ubv glVertexAttribI4ubv;
	PROC_glVertexAttribI4usv glVertexAttribI4usv;
	PROC_glGetUniformuiv glGetUniformuiv;
	PROC_glBindFragDataLocation glBindFragDataLocation;
	PROC_glGetFragDataLocation glGetFragDataLocation;
	PROC_glUniform1ui glUniform1ui;
	PROC_glUniform2ui glUniform2ui;
	PROC_glUniform3ui glUniform3ui;
	PROC_glUniform4ui glUniform4ui;
	PROC_glUniform1uiv glUniform1uiv;
	PROC_glUniform2uiv glUniform2uiv;
	PROC_glUniform3uiv glUniform3uiv;
	PROC_glUniform4uiv glUniform4uiv;
	PROC_glTexParameterIiv glTexParameterIiv;
	PROC_glTexParameterIuiv glTexParameterIuiv;
	PROC_glGetTexParameterIiv glGetTexParameterIiv;
	PROC_glGetTexParameterIuiv glGetTexParameterIuiv;
	PROC_glClearBufferiv glClearBufferiv;
	PROC_glClearBufferuiv glClearBufferuiv;
	PROC_glClearBufferfv glClearBufferfv;
	PROC_glClearBufferfi glClearBufferfi;
	PROC_glGetStringi glGetStringi;
	PROC_glIsRenderbuffer glIsRenderbuffer;
	PROC_glBindRenderbuffer glBindRenderbuffer;
	PROC_glDeleteRenderbuffers glDeleteRenderbuffers;
	PROC_glGenRenderbuffers glGenRenderbuffers;
	PROC_glRenderbufferStorage glRenderbufferStorage;
	PROC_glGetRenderbufferParameteriv glGetRenderbufferParameteriv;
	PROC_glIsFramebuffer glIsFramebuffer;
	PROC_glBindFramebuffer glBindFramebuffer;
	PROC_glDeleteFramebuffers glDeleteFramebuffers;
	PROC_glGenFramebuffers glGenFramebuffers;
	PROC_glCheckFramebufferStatus glCheckFramebufferStatus;
	PROC_glFramebufferTexture1D glFramebufferTexture1D;
	PROC_glFramebufferTexture2D glFramebufferTexture2D;
	PROC_glFramebufferTexture3D glFramebufferTexture3D;
	PROC_glFramebufferRenderbuffer glFramebufferRenderbuffer;
	PROC_glGetFramebufferAttachmentParameteriv glGetFramebufferAttachmentParameteriv;
	PROC_glGenerateMipmap glGenerateMipmap;
	PROC_glBlitFramebuffer glBlitFramebuffer;
	PROC_glRenderbufferStorageMultisample glRenderbufferStorageMultisample;
	PROC_glFramebufferTextureLayer glFramebufferTextureLayer;
	PROC_glMapBufferRange glMapBufferRange;
	PROC_glFlushMappedBufferRange glFlushMappedBufferRange;
	PROC_glBindVertexArray glBindVertexArray;
	PROC_glDeleteVertexArrays glDeleteVertexArrays;
	PROC_glGenVertexArrays glGenVertexArrays;
	PROC_glIsVertexArray glIsVertexArray;
	PROC_glDrawArraysInstanced glDrawArraysInstanced;
	PROC_glDrawElementsInstanced glDrawElementsInstanced;
	PROC_glTexBuffer glTexBuffer;
	PROC_glPrimitiveRestartIndex glPrimitiveRestartIndex;
	PROC_glCopyBufferSubData glCopyBufferSubData;
	PROC_glGetUniformIndices glGetUniformIndices;
	PROC_glGetActiveUniformsiv glGetActiveUniformsiv;
	PROC_glGetActiveUniformName glGetActiveUniformName;
	PROC_glGetUniformBlockIndex glGetUniformBlockIndex;
	PROC_glGetActiveUniformBlockiv glGetActiveUniformBlockiv;
	PROC_glGetActiveUniformBlockName glGetActiveUniformBlockName;
	PROC_glUniformBlockBinding glUniformBlockBinding;
	PROC_glDrawElementsBaseVertex glDrawElementsBaseVertex;
	PROC_glDrawRangeElementsBaseVertex glDrawRangeElementsBaseVertex;
	PROC_glDrawElementsInstancedBaseVertex glDrawElementsInstancedBaseVertex;
	PROC_glMultiDrawElementsBaseVertex glMultiDrawElementsBaseVertex;
	PROC_glProvokingVertex glProvokingVertex;
	PROC_glFenceSync glFenceSync;
	PROC_glIsSync glIsSync;
	PROC_glDeleteSync glDeleteSync;
	PROC_glClientWaitSync glClientWaitSync;
	PROC_glWaitSync glWaitSync;
	PROC_glGetInteger64v glGetInteger64v;
	PROC_glGetSynciv glGetSynciv;
	PROC_glGetInteger64i_v glGetInteger64i_v;
	PROC_glGetBufferParameteri64v glGetBufferParameteri64v;
	PROC_glFramebufferTexture glFramebufferTexture;
	PROC_glTexImage2DMultisample glTexImage2DMultisample;
	PROC_glTexImage3DMultisample glTexImage3DMultisample;
	PROC_glGetMultisamplefv glGetMultisamplefv;
	PROC_glSampleMaski glSampleMaski;
	PROC_glBindFragDataLocationIndexed glBindFragDataLocationIndexed;
	PROC_glGetFragDataIndex glGetFragDataIndex;
	PROC_glGenSamplers glGenSamplers;
	PROC_glDeleteSamplers glDeleteSamplers;
	PROC_glIsSampler glIsSampler;
	PROC_glBindSampler glBindSampler;
	PROC_glSamplerParameteri glSamplerParameteri;
	PROC_glSamplerParameteriv glSamplerParameteriv;
	PROC_glSamplerParameterf glSamplerParameterf;
	PROC_glSamplerParameterfv glSamplerParameterfv;
	PROC_glSamplerParameterIiv glSamplerParameterIiv;
	PROC_glSamplerParameterIuiv glSamplerParameterIuiv;
	PROC_glGetSamplerParameteriv glGetSamplerParameteriv;
	PROC_glGetSamplerParameterIiv glGetSamplerParameterIiv;
	PROC_glGetSamplerParameterfv glGetSamplerParameterfv;
	PROC_glGetSamplerParameterIuiv glGetSamplerParameterIuiv;
	PROC_glQueryCounter glQueryCounter;
	PROC_glGetQueryObjecti64v glGetQueryObjecti64v;
	PROC_glGetQueryObjectui64v glGetQueryObjectui64v;
	PROC_glVertexAttribDivisor glVertexAttribDivisor;
	PROC_glVertexAttribP1ui glVertexAttribP1ui;
	PROC_glVertexAttribP1uiv glVertexAttribP1uiv;
	PROC_glVertexAttribP2ui glVertexAttribP2ui;
	PROC_glVertexAttribP2uiv glVertexAttribP2uiv;
	PROC_glVertexAttribP3ui glVertexAttribP3ui;
	PROC_glVertexAttribP3uiv glVertexAttribP3uiv;
	PROC_glVertexAttribP4ui glVertexAttribP4ui;
	PROC_glVertexAttribP4uiv glVertexAttribP4uiv;
	PROC_glMinSampleShading glMinSampleShading;
	PROC_glBlendEquationi glBlendEquationi;
	PROC_glBlendEquationSeparatei glBlendEquationSeparatei;
	PROC_glBlendFunci glBlendFunci;
	PROC_glBlendFuncSeparatei glBlendFuncSeparatei;
	PROC_glDrawArraysIndirect glDrawArraysIndirect;
	PROC_glDrawElementsIndirect glDrawElementsIndirect;
	PROC_glUniform1d glUniform1d;
	PROC_glUniform2d glUniform2d;
	PROC_glUniform3d glUniform3d;
	PROC_glUniform4d glUniform4d;
	PROC_glUniform1dv glUniform1dv;
	PROC_glUniform2dv glUniform2dv;
	PROC_glUniform3dv glUniform3dv;
	PROC_glUniform4dv glUniform4dv;
	PROC_glUniformMatrix2dv glUniformMatrix2dv;
	PROC_glUniformMatrix3dv glUniformMatrix3dv;
	PROC_glUniformMatrix4dv glUniformMatrix4dv;
	PROC_glUniformMatrix2x3dv glUniformMatrix2x3dv;
	PROC_glUniformMatrix2x4dv glUniformMatrix2x4dv;
	PROC_glUniformMatrix3x2dv glUniformMatrix3x2dv;
	PROC_glUniformMatrix3x4dv glUniformMatrix3x4dv;
	PROC_glUniformMatrix4x2dv glUniformMatrix4x2dv;
	PROC_glUniformMatrix4x3dv glUniformMatrix4x3dv;
	PROC_glGetUniformdv glGetUniformdv;
	PROC_glGetSubroutineUniformLocation glGetSubroutineUniformLocation;
	PROC_glGetSubroutineIndex glGetSubroutineIndex;
	PROC_glGetActiveSubroutineUniformiv glGetActiveSubroutineUniformiv;
	PROC_glGetActiveSubroutineUniformName glGetActiveSubroutineUniformName;
	PROC_glGetActiveSubroutineName glGetActiveSubroutineName;
	PROC_glUniformSubroutinesuiv glUniformSubroutinesuiv;
	PROC_glGetUniformSubroutineuiv glGetUniformSubroutineuiv;
	PROC_glGetProgramStageiv glGetProgramStageiv;
	PROC_glPatchParameteri glPatchParameteri;
	PROC_glPatchParameterfv glPatchParameterfv;
	PROC_glBindTransformFeedback glBindTransformFeedback;
	PROC_glDeleteTransformFeedbacks glDeleteTransformFeedbacks;
	PROC_glGenTransformFeedbacks glGenTransformFeedbacks;
	PROC_glIsTransformFeedback glIsTransformFeedback;
	PROC_glPauseTransformFeedback glPauseTransformFeedback;
	PROC_glResumeTransformFeedback glResumeTransformFeedback;
	PROC_glDrawTransformFeedback glDrawTransformFeedback;
	PROC_glDrawTransformFeedbackStream glDrawTransformFeedbackStream;
	PROC_glBeginQueryIndexed glBeginQueryIndexed;
	PROC_glEndQueryIndexed glEndQueryIndexed;
	PROC_glGetQueryIndexediv glGetQueryIndexediv;
	PROC_glReleaseShaderCompiler glReleaseShaderCompiler;
	PROC_glShaderBinary glShaderBinary;
	PROC_glGetShaderPrecisionFormat glGetShaderPrecisionFormat;
	PROC_glDepthRangef glDepthRangef;
	PROC_glClearDepthf glClearDepthf;
	PROC_glGetProgramBinary glGetProgramBinary;
	PROC_glProgramBinary glProgramBinary;
	PROC_glProgramParameteri glProgramParameteri;
	PROC_glUseProgramStages glUseProgramStages;
	PROC_glActiveShaderProgram glActiveShaderProgram;
	PROC_glCreateShaderProgramv glCreateShaderProgramv;
	PROC_glBindProgramPipeline glBindProgramPipeline;
	PROC_glDeleteProgramPipelines glDeleteProgramPipelines;
	PROC_glGenProgramPipelines glGenProgramPipelines;
	PROC_glIsProgramPipeline glIsProgramPipeline;
	PROC_glGetProgramPipelineiv glGetProgramPipelineiv;
	PROC_glProgramUniform1i glProgramUniform1i;
	PROC_glProgramUniform1iv glProgramUniform1iv;
	PROC_glProgramUniform1f glProgramUniform1f;
	PROC_glProgramUniform1fv glProgramUniform1fv;
	PROC_glProgramUniform1d glProgramUniform1d;
	PROC_glProgramUniform1dv glProgramUniform1dv;
	PROC_glProgramUniform1ui glProgramUniform1ui;
	PROC_glProgramUniform1uiv glProgramUniform1uiv;
	PROC_glProgramUniform2i glProgramUniform2i;
	PROC_glProgramUniform2iv glProgramUniform2iv;
	PROC_glProgramUniform2f glProgramUniform2f;
	PROC_glProgramUniform2fv glProgramUniform2fv;
	PROC_glProgramUniform2d glProgramUniform2d;
	PROC_glProgramUniform2dv glProgramUniform2dv;
	PROC_glProgramUniform2ui glProgramUniform2ui;
	PROC_glProgramUniform2uiv glProgramUniform2uiv;
	PROC_glProgramUniform3i glProgramUniform3i;
	PROC_glProgramUniform3iv glProgramUniform3iv;
	PROC_glProgramUniform3f glProgramUniform3f;
	PROC_glProgramUniform3fv glProgramUniform3fv;
	PROC_glProgramUniform3d glProgramUniform3d;
	PROC_glProgramUniform3dv glProgramUniform3dv;
	PROC_glProgramUniform3ui glProgramUniform3ui;
	PROC_glProgramUniform3uiv glProgramUniform3uiv;
	PROC_glProgramUniform4i glProgramUniform4i;
	PROC_glProgramUniform4iv glProgramUniform4iv;
	PROC_glProgramUniform4f glProgramUniform4f;
	PROC_glProgramUniform4fv glProgramUniform4fv;
	PROC_glProgramUniform4d glProgramUniform4d;
	PROC_glProgramUniform4dv glProgramUniform4dv;
	PROC_glProgramUniform4ui glProgramUniform4ui;
	PROC_glProgramUniform4uiv glProgramUniform4uiv;
	PROC_glProgramUniformMatrix2fv glProgramUniformMatrix2fv;
	PROC_glProgramUniformMatrix3fv glProgramUniformMatrix3fv;
	PROC_glProgramUniformMatrix4fv glProgramUniformMatrix4fv;
	PROC_glProgramUniformMatrix2dv glProgramUniformMatrix2dv;
	PROC_glProgramUniformMatrix3dv glProgramUniformMatrix3dv;
	PROC_glProgramUniformMatrix4dv glProgramUniformMatrix4dv;
	PROC_glProgramUniformMatrix2x3fv glProgramUniformMatrix2x3fv;
	PROC_glProgramUniformMatrix3x2fv glProgramUniformMatrix3x2fv;
	PROC_glProgramUniformMatrix2x4fv glProgramUniformMatrix2x4fv;
	PROC_glProgramUniformMatrix4x2fv glProgramUniformMatrix4x2fv;
	PROC_glProgramUniformMatrix3x4fv glProgramUniformMatrix3x4fv;
	PROC_glProgramUniformMatrix4x3fv glProgramUniformMatrix4x3fv;
	PROC_glProgramUniformMatrix2x3dv glProgramUniformMatrix2x3dv;
	PROC_glProgramUniformMatrix3x2dv glProgramUniformMatrix3x2dv;
	PROC_glProgramUniformMatrix2x4dv glProgramUniformMatrix2x4dv;
	PROC_glProgramUniformMatrix4x2dv glProgramUniformMatrix4x2dv;
	PROC_glProgramUniformMatrix3x4dv glProgramUniformMatrix3x4dv;
	PROC_glProgramUniformMatrix4x3dv glProgramUniformMatrix4x3dv;
	PROC_glValidateProgramPipeline glValidateProgramPipeline;
	PROC_glGetProgramPipelineInfoLog glGetProgramPipelineInfoLog;
	PROC_glVertexAttribL1d glVertexAttribL1d;
	PROC_glVertexAttribL2d glVertexAttribL2d;
	PROC_glVertexAttribL3d glVertexAttribL3d;
	PROC_glVertexAttribL4d glVertexAttribL4d;
	PROC_glVertexAttribL1dv glVertexAttribL1dv;
	PROC_glVertexAttribL2dv glVertexAttribL2dv;
	PROC_glVertexAttribL3dv glVertexAttribL3dv;
	PROC_glVertexAttribL4dv glVertexAttribL4dv;
	PROC_glVertexAttribLPointer glVertexAttribLPointer;
	PROC_glGetVertexAttribLdv glGetVertexAttribLdv;
	PROC_glViewportArrayv glViewportArrayv;
	PROC_glViewportIndexedf glViewportIndexedf;
	PROC_glViewportIndexedfv glViewportIndexedfv;
	PROC_glScissorArrayv glScissorArrayv;
	PROC_glScissorIndexed glScissorIndexed;
	PROC_glScissorIndexedv glScissorIndexedv;
	PROC_glDepthRangeArrayv glDepthRangeArrayv;
	PROC_glDepthRangeIndexed glDepthRangeIndexed;
	PROC_glGetFloati_v glGetFloati_v;
	PROC_glGetDoublei_v glGetDoublei_v;
	PROC_glDrawArraysInstancedBaseInstance glDrawArraysInstancedBaseInstance;
	PROC_glDrawElementsInstancedBaseInstance glDrawElementsInstancedBaseInstance;
	PROC_glDrawElementsInstancedBaseVertexBaseInstance glDrawElementsInstancedBaseVertexBaseInstance;
	PROC_glGetInternalformativ glGetInternalformativ;
	PROC_glGetActiveAtomicCounterBufferiv glGetActiveAtomicCounterBufferiv;
	PROC_glBindImageTexture glBindImageTexture;
	PROC_glMemoryBarrier glMemoryBarrier;
	PROC_glTexStorage1D glTexStorage1D;
	PROC_glTexStorage2D glTexStorage2D;
	PROC_glTexStorage3D glTexStorage3D;
	PROC_glDrawTransformFeedbackInstanced glDrawTransformFeedbackInstanced;
	PROC_glDrawTransformFeedbackStreamInstanced glDrawTransformFeedbackStreamInstanced;
	PROC_glClearBufferData glClearBufferData;
	PROC_glClearBufferSubData glClearBufferSubData;
	PROC_glDispatchCompute glDispatchCompute;
	PROC_glDispatchComputeIndirect glDispatchComputeIndirect;
	PROC_glCopyImageSubData glCopyImageSubData;
	PROC_glFramebufferParameteri glFramebufferParameteri;
	PROC_glGetFramebufferParameteriv glGetFramebufferParameteriv;
	PROC_glGetInternalformati64v glGetInternalformati64v;
	PROC_glInvalidateTexSubImage glInvalidateTexSubImage;
	PROC_glInvalidateTexImage glInvalidateTexImage;
	PROC_glInvalidateBufferSubData glInvalidateBufferSubData;
	PROC_glInvalidateBufferData glInvalidateBufferData;
	PROC_glInvalidateFramebuffer glInvalidateFramebuffer;
	PROC_glInvalidateSubFramebuffer glInvalidateSubFramebuffer;
	PROC_glMultiDrawArraysIndirect glMultiDrawArraysIndirect;
	PROC_glMultiDrawElementsIndirect glMultiDrawElementsIndirect;
	PROC_glGetProgramInterfaceiv glGetProgramInterfaceiv;
	PROC_glGetProgramResourceIndex glGetProgramResourceIndex;
	PROC_glGetProgramResourceName glGetProgramResourceName;
	PROC_glGetProgramResourceiv glGetProgramResourceiv;
	PROC_glGetProgramResourceLocation glGetProgramResourceLocation;
	PROC_glGetProgramResourceLocationIndex glGetProgramResourceLocationIndex;
	PROC_glShaderStorageBlockBinding glShaderStorageBlockBinding;
	PROC_glTexBufferRange glTexBufferRange;
	PROC_glTexStorage2DMultisample glTexStorage2DMultisample;
	PROC_glTexStorage3DMultisample glTexStorage3DMultisample;
	PROC_glTextureView glTextureView;
	PROC_glBindVertexBuffer glBindVertexBuffer;
	PROC_glVertexAttribFormat glVertexAttribFormat;
	PROC_glVertexAttribIFormat glVertexAttribIFormat;
	PROC_glVertexAttribLFormat glVertexAttribLFormat;
	PROC_glVertexAttribBinding glVertexAttribBinding;
	PROC_glVertexBindingDivisor glVertexBindingDivisor;
	PROC_glDebugMessageControl glDebugMessageControl;
	PROC_glDebugMessageInsert glDebugMessageInsert;
	PROC_glDebugMessageCallback glDebugMessageCallback;
	PROC_glGetDebugMessageLog glGetDebugMessageLog;
	PROC_glPushDebugGroup glPushDebugGroup;
	PROC_glPopDebugGroup glPopDebugGroup;
	PROC_glObjectLabel glObjectLabel;
	PROC_glGetObjectLabel glGetObjectLabel;
	PROC_glObjectPtrLabel glObjectPtrLabel;
	PROC_glGetObjectPtrLabel glGetObjectPtrLabel;
	PROC_glBufferStorage glBufferStorage;
	PROC_glClearTexImage glClearTexImage;
	PROC_glClearTexSubImage glClearTexSubImage;
	PROC_glBindBuffersBase glBindBuffersBase;
	PROC_glBindBuffersRange glBindBuffersRange;
	PROC_glBindTextures glBindTextures;
	PROC_glBindSamplers glBindSamplers;
	PROC_glBindImageTextures glBindImageTextures;
	PROC_glBindVertexBuffers glBindVertexBuffers;
	PROC_glClipControl glClipControl;
	PROC_glCreateTransformFeedbacks glCreateTransformFeedbacks;
	PROC_glTransformFeedbackBufferBase glTransformFeedbackBufferBase;
	PROC_glTransformFeedbackBufferRange glTransformFeedbackBufferRange;
	PROC_glGetTransformFeedbackiv glGetTransformFeedbackiv;
	PROC_glGetTransformFeedbacki_v glGetTransformFeedbacki_v;
	PROC_glGetTransformFeedbacki64_v glGetTransformFeedbacki64_v;
	PROC_glCreateBuffers glCreateBuffers;
	PROC_glNamedBufferStorage glNamedBufferStorage;
	PROC_glNamedBufferData glNamedBufferData;
	PROC_glNamedBufferSubData glNamedBufferSubData;
	PROC_glCopyNamedBufferSubData glCopyNamedBufferSubData;
	PROC_glClearNamedBufferData glClearNamedBufferData;
	PROC_glClearNamedBufferSubData glClearNamedBufferSubData;
	PROC_glMapNamedBuffer glMapNamedBuffer;
	PROC_glMapNamedBufferRange glMapNamedBufferRange;
	PROC_glUnmapNamedBuffer glUnmapNamedBuffer;
	PROC_glFlushMappedNamedBufferRange glFlushMappedNamedBufferRange;
	PROC_glGetNamedBufferParameteriv glGetNamedBufferParameteriv;
	PROC_glGetNamedBufferParameteri64v glGetNamedBufferParameteri64v;
	PROC_glGetNamedBufferPointerv glGetNamedBufferPointerv;
	PROC_glGetNamedBufferSubData glGetNamedBufferSubData;
	PROC_glCreateFramebuffers glCreateFramebuffers;
	PROC_glNamedFramebufferRenderbuffer glNamedFramebufferRenderbuffer;
	PROC_glNamedFramebufferParameteri glNamedFramebufferParameteri;
	PROC_glNamedFramebufferTexture glNamedFramebufferTexture;
	PROC_glNamedFramebufferTextureLayer glNamedFramebufferTextureLayer;
	PROC_glNamedFramebufferDrawBuffer glNamedFramebufferDrawBuffer;
	PROC_glNamedFramebufferDrawBuffers glNamedFramebufferDrawBuffers;
	PROC_glNamedFramebufferReadBuffer glNamedFramebufferReadBuffer;
	PROC_glInvalidateNamedFramebufferData glInvalidateNamedFramebufferData;
	PROC_glInvalidateNamedFramebufferSubData glInvalidateNamedFramebufferSubData;
	PROC_glClearNamedFramebufferiv glClearNamedFramebufferiv;
	PROC_glClearNamedFramebufferuiv glClearNamedFramebufferuiv;
	PROC_glClearNamedFramebufferfv glClearNamedFramebufferfv;
	PROC_glClearNamedFramebufferfi glClearNamedFramebufferfi;
	PROC_glBlitNamedFramebuffer glBlitNamedFramebuffer;
	PROC_glCheckNamedFramebufferStatus glCheckNamedFramebufferStatus;
	PROC_glGetNamedFramebufferParameteriv glGetNamedFramebufferParameteriv;
	PROC_glGetNamedFramebufferAttachmentParameteriv glGetNamedFramebufferAttachmentParameteriv;
	PROC_glCreateRenderbuffers glCreateRenderbuffers;
	PROC_glNamedRenderbufferStorage glNamedRenderbufferStorage;
	PROC_glNamedRenderbufferStorageMultisample glNamedRenderbufferStorageMultisample;
	PROC_glGetNamedRenderbufferParameteriv glGetNamedRenderbufferParameteriv;
	PROC_glCreateTextures glCreateTextures;
	PROC_glTextureBuffer glTextureBuffer;
	PROC_glTextureBufferRange glTextureBufferRange;
	PROC_glTextureStorage1D glTextureStorage1D;
	PROC_glTextureStorage2D glTextureStorage2D;
	PROC_glTextureStorage3D glTextureStorage3D;
	PROC_glTextureStorage2DMultisample glTextureStorage2DMultisample;
	PROC_glTextureStorage3DMultisample glTextureStorage3DMultisample;
	PROC_glTextureSubImage1D glTextureSubImage1D;
	PROC_glTextureSubImage2D glTextureSubImage2D;
	PROC_glTextureSubImage3D glTextureSubImage3D;
	PROC_glCompressedTextureSubImage1D glCompressedTextureSubImage1D;
	PROC_glCompressedTextureSubImage2D glCompressedTextureSubImage2D;
	PROC_glCompressedTextureSubImage3D glCompressedTextureSubImage3D;
	PROC_glCopyTextureSubImage1D glCopyTextureSubImage1D;
	PROC_glCopyTextureSubImage2D glCopyTextureSubImage2D;
	PROC_glCopyTextureSubImage3D glCopyTextureSubImage3D;
	PROC_glTextureParameterf glTextureParameterf;
	PROC_glTextureParameterfv glTextureParameterfv;
	PROC_glTextureParameteri glTextureParameteri;
	PROC_glTextureParameterIiv glTextureParameterIiv;
	PROC_glTextureParameterIuiv glTextureParameterIuiv;
	PROC_glTextureParameteriv glTextureParameteriv;
	PROC_glGenerateTextureMipmap glGenerateTextureMipmap;
	PROC_glBindTextureUnit glBindTextureUnit;
	PROC_glGetTextureImage glGetTextureImage;
	PROC_glGetCompressedTextureImage glGetCompressedTextureImage;
	PROC_glGetTextureLevelParameterfv glGetTextureLevelParameterfv;
	PROC_glGetTextureLevelParameteriv glGetTextureLevelParameteriv;
	PROC_glGetTextureParameterfv glGetTextureParameterfv;
	PROC_glGetTextureParameterIiv glGetTextureParameterIiv;
	PROC_glGetTextureParameterIuiv glGetTextureParameterIuiv;
	PROC_glGetTextureParameteriv glGetTextureParameteriv;
	PROC_glCreateVertexArrays glCreateVertexArrays;
	PROC_glDisableVertexArrayAttrib glDisableVertexArrayAttrib;
	PROC_glEnableVertexArrayAttrib glEnableVertexArrayAttrib;
	PROC_glVertexArrayElementBuffer glVertexArrayElementBuffer;
	PROC_glVertexArrayVertexBuffer glVertexArrayVertexBuffer;
	PROC_glVertexArrayVertexBuffers glVertexArrayVertexBuffers;
	PROC_glVertexArrayAttribBinding glVertexArrayAttribBinding;
	PROC_glVertexArrayAttribFormat glVertexArrayAttribFormat;
	PROC_glVertexArrayAttribIFormat glVertexArrayAttribIFormat;
	PROC_glVertexArrayAttribLFormat glVertexArrayAttribLFormat;
	PROC_glVertexArrayBindingDivisor glVertexArrayBindingDivisor;
	PROC_glGetVertexArrayiv glGetVertexArrayiv;
	PROC_glGetVertexArrayIndexediv glGetVertexArrayIndexediv;
	PROC_glGetVertexArrayIndexed64iv glGetVertexArrayIndexed64iv;
	PROC_glCreateSamplers glCreateSamplers;
	PROC_glCreateProgramPipelines glCreateProgramPipelines;
	PROC_glCreateQueries glCreateQueries;
	PROC_glGetQueryBufferObjecti64v glGetQueryBufferObjecti64v;
	PROC_glGetQueryBufferObjectiv glGetQueryBufferObjectiv;
	PROC_glGetQueryBufferObjectui64v glGetQueryBufferObjectui64v;
	PROC_glGetQueryBufferObjectuiv glGetQueryBufferObjectuiv;
	PROC_glMemoryBarrierByRegion glMemoryBarrierByRegion;
	PROC_glGetTextureSubImage glGetTextureSubImage;
	PROC_glGetCompressedTextureSubImage glGetCompressedTextureSubImage;
	PROC_glGetGraphicsResetStatus glGetGraphicsResetStatus;
	PROC_glGetnCompressedTexImage glGetnCompressedTexImage;
	PROC_glGetnTexImage glGetnTexImage;
	PROC_glGetnUniformdv glGetnUniformdv;
	PROC_glGetnUniformfv glGetnUniformfv;
	PROC_glGetnUniformiv glGetnUniformiv;
	PROC_glGetnUniformuiv glGetnUniformuiv;
	PROC_glReadnPixels glReadnPixels;
	PROC_glTextureBarrier glTextureBarrier;

}

#if defined(_WIN32) || defined(_WIN64)

#include <Windows.h>

namespace OpenGL {
	HMODULE opengl32;

	typedef const void * (__stdcall * PROC_wglGetProcAddress)(const char *);
	typedef const void * (__stdcall * PROC_wglGetCurrentContext)();

	PROC_wglGetProcAddress wglGetProcAddress;
	PROC_wglGetCurrentContext wglGetCurrentContext;

	const void * GetOpenGLFunction(const char * name) {
		const void * result = (const void *)GetProcAddress(opengl32, name);

		if (!result) {
			result = OpenGL::wglGetProcAddress(name);
		}

		return result;
	}

	bool InitializeOpenGL() {
		opengl32 = LoadLibrary("opengl32.dll");

		if (!opengl32) {
			return false;
		}

		OpenGL::wglGetProcAddress = (PROC_wglGetProcAddress)GetProcAddress(opengl32, "wglGetProcAddress");

		if (!OpenGL::wglGetProcAddress) {
			return false;
		}
		OpenGL::wglGetCurrentContext = (PROC_wglGetCurrentContext)GetProcAddress(opengl32, "wglGetCurrentContext");

		if (!OpenGL::wglGetCurrentContext) {
			return false;
		}

		if (!OpenGL::wglGetCurrentContext()) {
			return false;
		}

		if (!LoadCoreOpenGLFunctions()) {
			return false;
		}

		return true;
	}

}

#else

#include <dlfcn.h>

namespace OpenGL {
	void * libgl;

	typedef const void * (* PROC_glXGetProcAddress)(const char *);
	typedef const void * (* PROC_glXGetCurrentContext)();

	PROC_glXGetProcAddress glXGetProcAddress;
	PROC_glXGetCurrentContext glXGetCurrentContext;

	const void * GetOpenGLFunction(const char * name) {
		const void * result = dlsym(libgl, name);

		if (!result) {
			result = OpenGL::glXGetProcAddress(name);
		}

		return result;
	}

	bool InitializeOpenGL() {
		libgl = dlopen("libGL.so.1", RTLD_LAZY);

		if (!libgl) {
			return false;
		}

		OpenGL::glXGetProcAddress = (PROC_glXGetProcAddress)dlsym(libgl, "glXGetProcAddress");

		if (!OpenGL::glXGetProcAddress) {
			return false;
		}

		OpenGL::glXGetCurrentContext = (PROC_glXGetCurrentContext)dlsym(libgl, "glXGetCurrentContext");

		if (!OpenGL::glXGetCurrentContext) {
			return false;
		}

		if (!OpenGL::glXGetCurrentContext()) {
			return false;
		}

		if (!LoadCoreOpenGLFunctions()) {
			return false;
		}

		return true;
	}
}

#endif
