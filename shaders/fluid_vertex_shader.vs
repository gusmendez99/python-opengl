#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 theMatrix;
uniform mat4 normalMatrix;
uniform vec3 light;
uniform float clock;

out float intensity;
out vec3 glPosition;
out vec3 glNormal;
out float glTime;

void main()
{
    glTime = clock;
    glNormal = normal;
    glPosition = position;
    intensity = dot(normal, normalize(light));
    gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1.0);
}