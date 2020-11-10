import pygame
import numpy as np
import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vcolor;

uniform mat4 theMatrix;

out vec3 ourcolor;

void main()
{
  gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1.0);
  ourcolor = vcolor;
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

in vec3 ourcolor;

void main()
{
  fragColor = vec4(ourcolor, 1.0f);;
}
"""

shader = compileProgram(
  compileShader(vertex_shader, GL_VERTEX_SHADER),
  compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

vertex_data = np.array([
  -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
  0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
  0.0,  0.5, 0.0, 0.0, 0.0, 1.0
], dtype=np.float32)

# VBO
vertex_buffer_object = glGenBuffers(1)

glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# VAO
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # type
  GL_FALSE, # not normalized array
  6 * 4, # stride
  ctypes.c_void_p(0)
)

# For colors
glVertexAttribPointer(
   1,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
   3,                  # size
   GL_FLOAT,           # type
   GL_FALSE,           # normalized?
   6 * 4,              # stride
   ctypes.c_void_p(3 * 4)  # array buffer offset, reading only rgb values
)
glEnableVertexAttribArray(1)


# Loading models
i = glm.mat4()
def create_matrix(counter):
  translate = glm.translate(i, glm.vec3(0, 0, 0))
  rotate = glm.rotate(i, glm.radians(counter), glm.vec3(0, 1, 0))
  projection = glm.scale(i, glm.vec3(1, 1, 1))

  model = translate * rotate * projection
  view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), 800/600, 0.1,  1000)

  return projection * view * model


glViewport(0, 0, 800, 600)




running = True
counter = 0
while running:

  glClear(GL_COLOR_BUFFER_BIT)
  glClearColor(0.5, 1.0, 0.5, 1.0)
  
  glEnableVertexAttribArray(0)
  glUseProgram(shader)

  theMatrix = create_matrix(counter)

  # sending uniform, this won't be interpolated
  theMatrixLocation = glGetUniformLocation(shader, 'theMatrix')
  glUniformMatrix4fv(
    theMatrixLocation,  # location
    1,                  # count
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )

  # 
  counter += 1
  clock.tick(15)


  glDrawArrays(GL_TRIANGLES, 0, 3) # vertex data array len (row)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False