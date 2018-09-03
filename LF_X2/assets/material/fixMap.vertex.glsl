#ifdef VERTEX_SHADER

#ifdef GL_ES
# ifdef GL_FRAGMENT_PRECISION_HIGH
	precision highp float;
# else
	precision mediump float;
# endif
#endif

uniform mat4 uModelToWorldMatrix;
uniform mat4 uWorldToScreenMatrix;

// =====================================================================================
// Input attributes
// =====================================================================================
attribute vec3 aPosition;
attribute vec2 aUV;

// =====================================================================================
// Output attributes
// =====================================================================================

varying vec4 vUV;

// =====================================================================================
// Vertex shader
// =====================================================================================
void main(void)
{
	vUV.xy = aUV.xy;

	vec4 worldPos = vec4(aPosition, 1.0);
	worldPos = uModelToWorldMatrix * worldPos;

	gl_Position =  uWorldToScreenMatrix * worldPos;
}

#endif // VERTEX_SHADER
