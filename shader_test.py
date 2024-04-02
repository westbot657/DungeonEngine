# pylint: disable=[W,R,C,no-member, import-error]
import sys
from array import array

import pygame
import moderngl
import random

pygame.init()

screen = pygame.display.set_mode((1080, 720), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
display = pygame.Surface((1080, 720))
ctx = moderngl.create_context()

clock = pygame.time.Clock()

img = pygame.image.load('./ui_resources/attribute_panels_concept.png')

quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''
frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    // vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 10 + time * 0.01) * 0.1, uvs.y);
    f_color = vec4(texture(tex, uvs).rg, texture(tex, uvs).b * ((sin(time/5)/2)+1), 1.0);
}
'''
# 0, 120, 212 : 0, .470<g<.473, .830<b<.834

glow_shader = '''
#version 330 core

uniform sampler2D tex;
uniform vec2 mouse;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void distence(in vec2 pos1, in vec2 pos2, out float ds) {
    ds = clamp(2-(sqrt(pow(pos2.x-pos1.x, 2) + pow(pos2.y-pos1.y, 2))*4), 0.8313, 2.);
}

void main( void ) {
    vec2 uv = uvs;
    // Zooms out by a factor of 2.0
    uv *= 2.0;
    // Shifts every axis by -1.0
    uv -= 1.0;
    
    float d = 0;
    distence(mouse, uvs.xy, d);
    // d = clamp(d, 0., 1.);

    // Base color for the effect
    vec3 color = vec3 ( 0, 0.470588, 0.8313725 );
    
    if (texture(tex, uvs).g > 0.470 && texture(tex, uvs).g < 0.473 && texture(tex, uvs).b > 0.830 && texture(tex, uvs).b < 0.834 && texture(tex, uvs).r == 0) {
        // specify size of border. 0.0 - no border, 1.0 - border occupies the entire space
        vec2 borderSize = vec2(0.3); 

        // size of rectangle in terms of uv
        vec2 rectangleSize = vec2(1.0) - borderSize; 

        // distance field, 0.0 - point is inside rectangle, 1.0 point is on the far edge of the border.
        float distanceField = length(max(abs(uv)-rectangleSize,0.0) / borderSize);

        // calculate alpha accordingly to the value of the distance field
        float alpha = 1.0 - distanceField;

        f_color = vec4(color * d * (((sin((time+uvs.x)/50)/2)+3)/3), alpha);
        
    } else {
        f_color = texture(tex, uvs);
    }

}

'''

glow2_v_shader = '''
#version 330 core

in vec2 a_position;
in vec2 a_tex_coord;
in vec4 a_colour;

uniform mat4 matrix;

out vec4 v_colour;
out vec2 tex_coord;

void main() {
   v_colour = a_colour;
   tex_coord = a_tex_coord;
   gl_Position = matrix * vec4(a_position, 0, 1);
}
'''

glow2_shader = '''
#version 330 core

in vec4 v_colour;
in vec2 tex_coord;
out vec4 pixel;

uniform sampler2D t0;
uniform float glow_size = .5;
uniform vec3 glow_colour = vec3(0, 0, 0);
uniform float glow_intensity = 1;
uniform float glow_threshold = .5;

void main() {
    pixel = texture(t0, tex_coord);
    if (pixel.a <= glow_threshold) {
        ivec2 size = textureSize(t0, 0);
	
        float uv_x = tex_coord.x * size.x;
        float uv_y = tex_coord.y * size.y;

        float sum = 0.0;
        for (int n = 0; n < 9; ++n) {
            uv_y = (tex_coord.y * size.y) + (glow_size * float(n - 4.5));
            float h_sum = 0.0;
            h_sum += texelFetch(t0, ivec2(uv_x - (4.0 * glow_size), uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x - (3.0 * glow_size), uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x - (2.0 * glow_size), uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x - glow_size, uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x, uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x + glow_size, uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x + (2.0 * glow_size), uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x + (3.0 * glow_size), uv_y), 0).a;
            h_sum += texelFetch(t0, ivec2(uv_x + (4.0 * glow_size), uv_y), 0).a;
            sum += h_sum / 9.0;
        }

        pixel = vec4(glow_colour, (sum / 9.0) * glow_intensity);
    }
}

'''

split_shader = '''
#version 330 core

in vec2 uvs;

uniform sampler2D tex;


layout (location = 0) out vec4 FragColor;
layout (location = 1) out vec4 BrightColor;

void main() {
    
    FragColor = texture(tex, uvs);
    // check whether fragment output is higher than threshold, if so output as brightness color
    
    if (FragColor.g > 0.470 && FragColor.g < 0.473 && FragColor.b > 0.830 && FragColor.b < 0.834 && FragColor.r == 0) {
        BrightColor = vec4(FragColor.rgb, 1.0);
    }
    else {
        BrightColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
'''

gaussian_blur_shader = '''
#version 330 core
out vec4 FragColor;
in vec2 uvs;

uniform sampler2D tex;

uniform bool horizontal;
uniform float weight[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main() {
    vec2 tex_offset = 1.0 / textureSize(tex, 0); // gets size of single texel
    vec3 result = texture(tex, uvs).rgb * weight[0]; // current fragment's contribution
    if(horizontal) {
        for(int i = 1; i < 5; ++i) {
            result += texture(tex, uvs + vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
            result += texture(tex, uvs - vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
        }
    }
    else {
        for(int i = 1; i < 5; ++i) {
            result += texture(tex, uvs + vec2(0.0, tex_offset.y * i)).rgb * weight[i];
            result += texture(tex, uvs - vec2(0.0, tex_offset.y * i)).rgb * weight[i];
        }
    }
    FragColor = vec4(result, 1.0);
}
'''

blend_shader = '''
#version 330 core
out vec4 FragColor;
  
in vec2 uvs;

uniform sampler2D scene;
uniform sampler2D bloomBlur;
uniform float exposure;

void main()
{             
    const float gamma = 2.2;
    vec3 hdrColor = texture(scene, uvs).rgb;      
    vec3 bloomColor = texture(bloomBlur, uvs).rgb;
    hdrColor += bloomColor; // additive blending
    // tone mapping
    vec3 result = vec3(1.0) - exp(-hdrColor * exposure);
    // also gamma correct while we're at it       
    result = pow(result, vec3(1.0 / gamma));
    FragColor = vec4(result, 1.0);
}
'''

glow_shader_p1 = '''
#version 330 core


'''

glow_shader_p2 = '''
#version 330 core


'''

program = ctx.program(vertex_shader=vert_shader, fragment_shader=glow_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])
# program2 = ctx.program(vertex_shader=vert_shader, fragment_shader=glow_shader_p2)
# render_object2 = ctx.vertex_array(program2, [(quad_buffer2, '2f 2f', 'vert', 'texcoord')])


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

t = 0

while True:
    display.fill((0, 0, 0))
    display.blit(img, (50, 10))
    
    t += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    frame_tex = surf_to_texture(display)
    # frame_tex2 = surf_to_texture(display)
    frame_tex.use(0)
    # frame_tex.use(1)
    # program0['tex'] = 0
    program['tex'] = 0
    # program2['tex'] = 0
    pos = pygame.mouse.get_pos()
    program['mouse'] = array('f', (pos[0]/1080, pos[1]/720))
    program['time'] = t
    # program["rand"] = random.random()
    
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    
    pygame.display.flip()
    
    frame_tex.release()
    
    clock.tick(60)
    