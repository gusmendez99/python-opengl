import pygame
import numpy
import glm
import pyassimp

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from shader_loader import compile_shader

# For model viewer
CAMERA_VELOCITY = 0.5
MAX_ZOOM = 10
MIN_ZOOM = 2

running = True
exec_time = 0
position_x = 0
position_y = 1.8
position_z = 5
rotation_x = 0


pygame.init()
pygame.display.set_caption("Iron Man - Model Viewer")
screen = pygame.display.set_mode(
    (800, 600), pygame.OPENGL | pygame.OPENGLBLIT | pygame.DOUBLEBUF
)
clock = pygame.time.Clock()

# Load model
scene = pyassimp.load("./models/ironman.obj")
# Load texture
texture_surface = pygame.image.load("./models/ironman.tga")
texture_data = pygame.image.tostring(texture_surface, "RGB", 1)

width = texture_surface.get_width()
height = texture_surface.get_height()

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexImage2D(
    GL_TEXTURE_2D,
    0,  # Level details
    GL_RGB,
    width,
    height,
    0,  # border always zero
    GL_RGB,
    GL_UNSIGNED_BYTE,
    texture_data,
)

glGenerateMipmap(GL_TEXTURE_2D)
glViewport(0, 0, 800, 600)
glEnable(GL_DEPTH_TEST)

# compiles shader
shader = compile_shader(
    "shaders/smoke_vertex_shader.vs", "shaders/smoke_fragment_shader.fs"
)


def glize(node):
    # render
    for mesh in node.meshes:
        vertex_data = numpy.hstack(
            [
                numpy.array(mesh.vertices, dtype=numpy.float32),
                numpy.array(mesh.normals, dtype=numpy.float32),
                numpy.array(mesh.texturecoords[0], dtype=numpy.float32),
            ]
        )

        # print(mesh.materialindex)

        index_data = numpy.hstack(numpy.array(mesh.faces, dtype=numpy.int32),)

        vertex_buffer_object = glGenVertexArrays(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        element_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW
        )

        glUniform3f(glGetUniformLocation(shader, "light"), -2, 10, 5)

        glUniform4f(glGetUniformLocation(shader, "diffuse"), 5, 5, 5, 1)

        glUniform4f(glGetUniformLocation(shader, "ambient"), 0.2, 0.2, 0.2, 1)

        glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

    for child in node.children:
        glize(child)


i = glm.mat4()


def createTheMatrix(x, y, z, rotation_x):
    translate = glm.translate(i, glm.vec3(0, 0, 0))
    rotate_x = glm.rotate(i, glm.radians(rotation_x), glm.vec3(0, 1, 0))
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate_x * scale
    view = glm.lookAt(glm.vec3(x, y, z), glm.vec3(0, 1.8, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45), 800 / 600, 0.1, 1000)
    world = projection * view * model 

    return model, world


while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 1.0, 0.5, 1.0)
    # Background

    glUseProgram(shader)
    modelMatrix, worldMatrix = createTheMatrix(position_x, position_y, position_z, rotation_x)
    theMatrixLocation = glGetUniformLocation(shader, "theMatrix")
    glUniformMatrix4fv(
        theMatrixLocation, 1, GL_FALSE, glm.value_ptr(worldMatrix)  # location  # count
    )

    normalMatrixLocation = glGetUniformLocation(shader, "normalMatrix")
    glUniformMatrix4fv(
        normalMatrixLocation,
        1,
        GL_FALSE,
        glm.value_ptr(glm.transpose(glm.inverse(modelMatrix))),  # location  # count
    )

    exec_time += 0.05
    glUniform1f(glGetUniformLocation(shader, "clock"), exec_time)

    glize(scene.rootnode)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print("keydown")
            if event.key == pygame.K_q:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            if event.key == pygame.K_e:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            if event.key == pygame.K_a:
                position_x -= CAMERA_VELOCITY
            if event.key == pygame.K_d:
                position_x += CAMERA_VELOCITY
            if event.key == pygame.K_w:
                position_y += CAMERA_VELOCITY
            if event.key == pygame.K_s:
                position_y -= CAMERA_VELOCITY
            if event.key == pygame.K_DOWN:
                offset_z = position_z + CAMERA_VELOCITY
                if offset_z > MIN_ZOOM and offset_z < MAX_ZOOM:
                    position_z += CAMERA_VELOCITY
            if event.key == pygame.K_UP:
                offset_z = position_z - CAMERA_VELOCITY
                if offset_z > MIN_ZOOM and offset_z < MAX_ZOOM:
                    position_z -= CAMERA_VELOCITY

    rotation_x = pygame.mouse.get_pos()[0]
    rotation_x -= 400
    rotation_x = (rotation_x / 800) * 360

    clock.tick(0)
