
#define STANDARD

uniform sampler2D control0;
uniform sampler2D control1;
uniform sampler2D asg;

uniform float scratchStrength;

uniform bool hasS0;
uniform sampler2D s0Mask;
uniform vec3 s0TopC;
uniform vec3 s0MidC;
uniform vec3 s0BotC;
uniform float s0TDensity;
uniform vec3 s0ScratchColor;

uniform bool hasS1;
uniform sampler2D s1Mask;
uniform vec3 s1TopC;
uniform vec3 s1MidC;
uniform vec3 s1BotC;
uniform float s1TDensity;
uniform vec3 s1ScratchColor;

uniform bool hasS2;
uniform sampler2D s2Mask;
uniform vec3 s2TopC;
uniform vec3 s2MidC;
uniform vec3 s2BotC;
uniform float s2TDensity;
uniform vec3 s2ScratchColor;

uniform bool hasS3;
uniform sampler2D s3Mask;
uniform vec3 s3TopC;
uniform vec3 s3MidC;
uniform vec3 s3BotC;
uniform float s3TDensity;
uniform vec3 s3ScratchColor;

uniform bool hasS4;
uniform sampler2D s4Mask;
uniform vec3 s4TopC;
uniform vec3 s4MidC;
uniform vec3 s4BotC;
uniform float s4TDensity;
uniform vec3 s4ScratchColor;

uniform bool hasS5;
uniform sampler2D s5Mask;
uniform vec3 s5TopC;
uniform vec3 s5MidC;
uniform vec3 s5BotC;
uniform float s5TDensity;
uniform vec3 s5ScratchColor;

uniform bool hasS6;
uniform sampler2D s6Mask;
uniform vec3 s6TopC;
uniform vec3 s6MidC;
uniform vec3 s6BotC;
uniform float s6TDensity;
uniform vec3 s6ScratchColor;

uniform bool hasS7;
uniform sampler2D s7Mask;
uniform vec3 s7TopC;
uniform vec3 s7MidC;
uniform vec3 s7BotC;
uniform float s7TDensity;
uniform vec3 s7ScratchColor;

varying vec3 vViewPosition;

#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif

#include <common>
#include <uv_pars_vertex>
#include <uv2_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>

void main() 
{  
    #include <uv_vertex>
	#include <uv2_vertex>
	#include <color_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>

    #ifndef FLAT_SHADED // Normal computed with derivatives when FLAT_SHADED
    	vNormal = normalize( transformedNormal );
        #ifdef USE_TANGENT
            vTangent = normalize( transformedTangent );
            vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
        #endif
    #endif

    #include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>

    vViewPosition = - mvPosition.xyz;

    #include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}

