#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec3 glPosition;
in float glTime;
in vec3 glNormal;
in vec2 vertexTexcoords;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

const int   complexity      = 20;    // More points of color.
const float mouse_factor    = 25.0;  // Makes it more/less jumpy.
const float mouse_offset    = 5.0;   // Drives complexity in the amount of curls/cuves.  Zero is a single whirlpool.
const float fluid_speed     = 45.0;  // Drives speed, higher number will make it slower.
const float color_intensity = 0.7;

const float Pi = 3.14159;

float sinApprox(float x) {
    x = Pi + (2.0 * Pi) * floor(x / (2.0 * Pi)) - x;
    return (4.0 / Pi) * x - (4.0 / Pi / Pi) * x * abs(x);
}

float cosApprox(float x) {
    return sinApprox(x + 0.5 * Pi);
}

void main()
{
    float theta = glTime;
    vec2 p=vec2(glPosition.x, glPosition.y);
    for(int i=1;i<complexity;i++)
    {
        vec2 newp=p;
        newp.x += 0.6/float(i)*sin(float(i)*p.y + glTime/fluid_speed+0.3*float(i));
        newp.y += 0.6/float(i)*sin(float(i)*p.x + glTime/fluid_speed+0.3*float(i+10));
        p=newp;
    }
    vec3 col=vec3(color_intensity*sin(3.0*p.x)+color_intensity,color_intensity*sin(3.0*p.y+glTime*0.75)+color_intensity,sin(p.x+p.y));
    vec4 finalColor=vec4(col, 1.0);
    gl_FragColor = ambient + diffuse * texture(tex, vertexTexcoords) * finalColor;

}