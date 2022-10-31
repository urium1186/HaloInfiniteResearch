# Author: Kaan Eraslan

import numpy as np
import os
import sys
import ctypes

from PySide6.QtGui import QOpenGLContext
from PySide6.QtGui import QVector4D
from PySide6.QtOpenGL import QOpenGLVertexArrayObject, QOpenGLBuffer, QOpenGLShaderProgram, QOpenGLShader
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox


from PySide6.QtCore import QCoreApplication
from shiboken6 import VoidPtr

try:
    from OpenGL import GL as pygl
except ImportError:
    app = QApplication(sys.argv)
    messageBox = QMessageBox(QMessageBox.Critical, "OpenGL hellogl",
                             "PyOpenGL must be installed to run this example.",
                             QMessageBox.Close)
    messageBox.setDetailedText(
        "Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)


class TriangleGL(QOpenGLWidget):
    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)

        # shaders etc
        triangleTutoDir = os.path.dirname(__file__)
        trianglePardir = os.path.join(triangleTutoDir, os.pardir)
        trianglePardir = os.path.realpath(trianglePardir)
        mediaDir = os.path.join(trianglePardir, "media")
        shaderDir = os.path.join(mediaDir, "shaders")
        print(shaderDir)
        availableShaders = ["triangle"]
        self.shaders = {
            name: {
                "fragment": os.path.join(shaderDir, name + ".frag"),
                "vertex": os.path.join(shaderDir, name + ".vert")
            } for name in availableShaders
        }
        self.core = "--coreprofile" in QCoreApplication.arguments()

        # opengl data related
        self.context = QOpenGLContext()
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.program = QOpenGLShaderProgram()

        # some vertex data for corners of triangle
        self.vertexData = np.array(
            [-0.5, -0.5, 0.0,  # x, y, z
             0.5, -0.5, 0.0,  # x, y, z
             0.0, 0.5, 0.0],  # x, y, z
            dtype=ctypes.c_float
        )
        # triangle color
        self.triangleColor = QVector4D(0.5, 0.5, 0.0, 0.0)  # yellow triangle
        # notice the correspondance the vec4 of fragment shader
        # and our choice here

    def loadShader(self,
                   shaderName: str,
                   shaderType: str):
        "Load shader"
        shader = self.shaders[shaderName]
        shaderSourcePath = shader[shaderType]
        if shaderType == "vertex":
            shader = QOpenGLShader(QOpenGLShader.Vertex)
        else:
            shader = QOpenGLShader(QOpenGLShader.Fragment)
        #
        isCompiled = shader.compileSourceFile(shaderSourcePath)

        if isCompiled is False:
            print(shader.log())
            raise ValueError(
                "{0} shader {2} known as {1} is not compiled".format(
                    shaderType, shaderName, shaderSourcePath
                )
            )
        return shader

    def loadVertexShader(self, shaderName: str):
        "load vertex shader"
        return self.loadShader(shaderName, "vertex")

    def loadFragmentShader(self, shaderName: str):
        "load fragment shader"
        return self.loadShader(shaderName, "fragment")

    def getGlInfo(self):
        "Get opengl info"
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
            """.format(
            pygl.glGetString(pygl.GL_VENDOR),
            pygl.glGetString(pygl.GL_RENDERER),
            pygl.glGetString(pygl.GL_VERSION),
            pygl.glGetString(pygl.GL_SHADING_LANGUAGE_VERSION)
        )
        return info

    def initializeGL(self):
        print('gl initial')
        print(self.getGlInfo())
        # create context and make it current
        self.context.create()
        self.context.aboutToBeDestroyed.connect(self.cleanUpGl)

        # initialize functions
        funcs = self.context.functions()
        funcs.initializeOpenGLFunctions()
        funcs.glClearColor(1, 1, 1, 1)

        # deal with shaders
        shaderName = "triangle"
        vshader = self.loadVertexShader(shaderName)
        fshader = self.loadFragmentShader(shaderName)

        # creating shader program
        self.program = QOpenGLShaderProgram(self.context)
        self.program.addShader(vshader)  # adding vertex shader
        self.program.addShader(fshader)  # adding fragment shader

        # bind attribute to a location
        self.program.bindAttributeLocation("aPos", 0)

        # link shader program
        isLinked = self.program.link()
        print("shader program is linked: ", isLinked)

        # bind the program
        self.program.bind()

        # specify uniform value
        colorLoc = self.program.uniformLocation("color")
        self.program.setUniformValue(colorLoc,
                                     self.triangleColor)

        # self.useShader("triangle")

        # deal with vao and vbo

        # create vao and vbo

        # vao
        isVao = self.vao.create()
        vaoBinder = QOpenGLVertexArrayObject.Binder(self.vao)

        # vbo
        isVbo = self.vbo.create()
        isBound = self.vbo.bind()

        # check if vao and vbo are created
        print('vao created: ', isVao)
        print('vbo created: ', isVbo)

        floatSize = ctypes.sizeof(ctypes.c_float)

        # allocate space on buffer
        self.vbo.allocate(self.vertexData.tobytes(),
                          floatSize * self.vertexData.size)
        funcs.glEnableVertexAttribArray(0)
        nullptr = VoidPtr(0)
        funcs.glVertexAttribPointer(0,
                                    3,
                                    int(pygl.GL_FLOAT),
                                    int(pygl.GL_FALSE),
                                    3 * floatSize,
                                    nullptr)
        self.vbo.release()
        self.program.release()
        vaoBinder = None

    def cleanUpGl(self):
        "Clean up everything"
        self.context.makeCurrent()
        self.vbo.destroy()
        del self.program
        self.program = None
        self.doneCurrent()

    def resizeGL(self, width: int, height: int):
        "Resize the viewport"
        funcs = self.context.functions()
        funcs.glViewport(0, 0, width, height)

    def paintGL(self):
        "drawing loop"
        funcs = self.context.functions()

        # clean up what was drawn
        funcs.glClear(pygl.GL_COLOR_BUFFER_BIT)

        # actual drawing
        vaoBinder = QOpenGLVertexArrayObject.Binder(self.vao)
        self.program.bind()
        funcs.glDrawArrays(pygl.GL_TRIANGLES,  # mode
                           0,  # first
                           3)  # count
        self.program.release()
        vaoBinder = None
