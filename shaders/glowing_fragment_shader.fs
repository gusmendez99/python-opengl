#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec3 glPosition;
in float glTime;
in vec3 glNormal;

uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{
    float theta = glTime;

    vec3 dir1 = vec3(cos(theta), 0, sin(theta)); 
    vec3 dir2 = vec3(sin(theta), 0, cos(theta));

    float diffuse1 = pow(dot(glNormal, dir1),2.0);
    float diffuse2 = pow(dot(glNormal, dir2),2.0);
    
    vec3 col1 = diffuse1 * vec3(1,0,0);
    vec3 col2 = diffuse2 * vec3(0,0,1);
    gl_FragColor = vec4(col1 + col2, 1.0);
}