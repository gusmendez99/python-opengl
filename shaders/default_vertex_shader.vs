#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 theMatrix;
uniform vec3 light;

out float intensity;
out vec2 vertexTexcoords;

void main()
{
    vertexTexcoords = texcoords;
    intensity = dot(normal, normalize(light));
    gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1.0);
}