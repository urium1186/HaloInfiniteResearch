
#define STANDARD

#ifdef PHYSICAL
	#define REFLECTIVITY
	#define CLEARCOAT
	#define TRANSMISSION
	#define IOR
    #define SPECULAR
#endif

uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;

uniform sampler2D gradientMask;
uniform vec3 topC;
uniform vec3 midC;
uniform vec3 botC;
uniform float tDensity;
uniform vec3 scratchColor;
uniform vec3 scratchStrength;

#ifdef TRANSMISSION
	uniform float transmission;
#endif

#ifdef REFLECTIVITY
	uniform float reflectivity;
#endif

#ifdef CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif

#ifdef USE_SHEEN
	uniform vec3 sheen;
#endif
varying vec3 vViewPosition;

#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif

#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <uv2_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>

#ifdef USE_TRANSMISSIONMAP

	uniform sampler2D transmissionMap;

#endif

#include <bsdfs>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <lights_physical_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>


#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>

vec3 sampleSwatch(vec3 topC, vec3 midC, vec3 botC, sampler2D mask, float tDensity, vec3 scratchColor) {    
    // will need to revisit and update.
    vec4 maskSample = texture2D(mask, mod(vUv * tDensity, 1.0));

    // Todo: Pretty sure that the game is using a more complex shaping function to control the colors. Currently what I have here isn't working well with darker colors like the carbon fiber.
    // 0 - 1... 
    // bot - mid, 0 - 0.5
    // mid - top, 0.5 - 1
    float mid = 0.6;
    float topMidMask = maskSample.r - mid;
    float midBotMask = clamp(maskSample.r, 0.0, mid);

    vec3 outCol = mix(botC, midC, midBotMask);
    outCol = mix(outCol, topC, topMidMask);  

    return outCol;
   }

// May need handling?
// EXT_color_buffer_float extension not supported.
// LOG  Warning: THREE.WebGLRenderer: EXT_texture_filter_anisotropic extension not supported.
void main() {
	#include <clipping_planes_fragment>

    vec3 col = sampleSwatch(topC, midC, botC, gradientMask, tDensity, scratchColor);
    vec4 diffuseColor = vec4(col, 1.0);

    ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
    vec3 totalEmissiveRadiance = emissive;

	#ifdef TRANSMISSION
		float totalTransmission = transmission;
	#endif
	
  	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>

	#include <normal_fragment_begin>
	#include <normal_fragment_maps>

  #include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	
    #include <emissivemap_fragment>
     
    #ifdef USE_TRANSMISSIONMAP
    	totalTransmission *= texture2D( transmissionMap, vUv ).r;
    #endif
	
    // accumulation
	#include <lights_physical_fragment>
	
	material.specularRoughness = 0.5 * (1.0 - roughnessFactor);

	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	
    // modulation
	#include <aomap_fragment>
	
    vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
  

    // // this is a stub for the transmission model
	#ifdef TRANSMISSION
		diffuseColor.a *= mix( saturate( 1. - totalTransmission + linearToRelativeLuminance( reflectedLight.directSpecular + reflectedLight.indirectSpecular ) ), 1.0, metalness );
	#endif

	gl_FragColor = vec4(outgoingLight, 1.0);
	
    // Seems to desaturate colors
    // #include <tonemapping_fragment>
	#include <encodings_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}
