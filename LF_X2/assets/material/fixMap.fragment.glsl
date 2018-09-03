#ifdef FRAGMENT_SHADER

#ifdef GL_ES
    #ifdef GL_FRAGMENT_PRECISION_HIGH
        precision highp float;
    #else
        precision mediump float;
    #endif
#endif

// =====================================================================================
// Uniforms
// =====================================================================================

#ifdef HAS_BASE_MAP
uniform sampler2D uBaseMap;
#endif


#ifdef HAS_MARK_MAP
uniform sampler2D uMarkMap;
#endif

uniform float uFix;
// =====================================================================================
// Attributes
// =====================================================================================
varying vec4 vUV;

// =====================================================================================
// Fragment shader
// =====================================================================================
void main(void)
{
	vec4 color = vec4(1.0, 1.0, 1.0, 1.0);

#ifdef HAS_BASE_MAP
	color = texture2D(uBaseMap, vUV.xy);
#endif
	
	color *= (1.0 - uFix);
#ifdef HAS_MARK_MAP
	vec4 mark = texture2D(uMarkMap, vUV.xy);
	mark *= uFix;
	color = mark + color;
#endif
	
    gl_FragColor = color;
}

#endif // FRAGMENT_SHADER
