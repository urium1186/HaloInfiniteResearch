
#define STANDARD

#ifdef PHYSICAL
	#define REFLECTIVITY
	#define CLEARCOAT
	#define TRANSMISSION
#endif

uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;


  struct ScratchSwatch {
      float scratchBrightness;
      vec3 scratchColor;
      float scratchIOR;
      float scratchMetallic;
      float scratchRoughness;
  };

  struct SwatchMaterial {
    vec3 top;
    vec3 mid;
    vec3 bot;
    float tDensity;
    float metalness;
    float roughness;
    float emissiveAmount;
    float emissiveIntensity;
    ScratchSwatch scratch;
    float ior;
  };

  struct Swatch {
    vec3 color;
    vec3 normal;
    float tDensity;
    float metalness;
    float roughness;
  };


uniform sampler2D control0;
uniform sampler2D asg;

uniform float scratchStrength;

uniform bool hasS0;
uniform SwatchMaterial swatch0;
uniform sampler2D s0Mask;

uniform bool hasS1;
uniform SwatchMaterial swatch1;
uniform sampler2D s1Mask;

uniform bool hasS2;
uniform SwatchMaterial swatch2;
uniform sampler2D s2Mask;

uniform bool hasS3;
uniform SwatchMaterial swatch3;
uniform sampler2D s3Mask;

uniform bool hasS4;
uniform SwatchMaterial swatch4;
uniform sampler2D s4Mask;

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


    vec3 applyScratches(vec3 diffuseColor, vec3 scratchColor, float scratchMask) {
        float inverseStrength = abs(scratchStrength - 1.0);
        
        // vec3 outc = scratchMask > inverseStrength ? scratchColor * scratchStrength * scratchMask : diffuseColor;
        vec3 outc = mix(diffuseColor, scratchColor, scratchMask * scratchStrength);
        return outc;
    }

    vec3 applyAo(vec3 outgoingLight, float aoValue) {
        vec3 shadowColor = vec3(0, 0, 0);
        float inverseStrength = abs(aoValue - 1.0);

        return mix(outgoingLight, shadowColor, inverseStrength);
    }

    vec3 applyGrime(vec3 diffuseColor, float grimeval) {
        vec3 grimeColor = vec3(0.2, 0.1, 0.1);
        float inverseStrength = abs(grimeval - 1.0);
        
        return mix(diffuseColor, grimeColor, grimeval);
    }

    vec3 sampleSwatch(vec3 topC, vec3 midC, vec3 botC, sampler2D mask, float tDensity, vec3 scratchColor) {    
        // Todo: Pretty sure that the game is using a shaping function to control the colors. Currently what I have here isn't working well with darker colors like the carbon fiber.
        // will need to revisit and update.
        vec4 maskSample = texture2D(mask, mod(vUv * tDensity, 1.0));

        // 0 - 1... 
        // bot - mid, 0 - 0.5
        // mid - top, 0.5 - 1
        float mid = 0.6;
        float topMidMask = maskSample.r - mid;
        float midBotMask = clamp(maskSample.r, 0.0, mid);

        vec3 outCol = mix(botC, midC, midBotMask);
        outCol = mix(outCol, topC, topMidMask);  

        vec4 asgMask = texture2D(asg, vUv);
        // outCol = applyScratches(outCol, scratchColor, asgMask.g);

        // Grime has its own swatch
        // outCol = applyGrime(outCol, asgMask.b);

        return outCol;
    }

    vec3 sampleMaterialSwatch(SwatchMaterial cSwatch, sampler2D mask) {    
        // Todo: Pretty sure that the game is using a shaping function to control the colors. Currently what I have here isn't working well with darker colors like the carbon fiber.
        // will need to revisit and update.
        vec4 maskSample = texture2D(mask, vUv * cSwatch.tDensity);
    
        // 0 - 1... 
        // bot - mid, 0 - 0.5
        // mid - top, 0.5 - 1
        float mid = 0.6;
        float topMidMask = maskSample.r - mid;
        float midBotMask = clamp(maskSample.r, 0.0, mid);
    
        vec3 outCol = mix(cSwatch.bot, cSwatch.mid, midBotMask);
        outCol = mix(outCol, cSwatch.top, topMidMask);  
        
        vec4 asgMask = texture2D(asg, vUv);
        // outCol = applyScratches(outCol, scratchColor, asgMask.g);
    
        return outCol;
    }


vec3 paintRegionBySwatch(vec4 control0Sample) {
    vec3 outColor = sampleMaterialSwatch(swatch0, s0Mask);
    outColor = mix(outColor, sampleMaterialSwatch(swatch1, s1Mask), control0Sample.r);
    outColor = mix(outColor, sampleMaterialSwatch(swatch2, s2Mask), control0Sample.g);
    outColor = mix(outColor, sampleMaterialSwatch(swatch3, s3Mask), control0Sample.b);

    
    return outColor;
}

float sampleMetallic(vec4 control0Sample) {
    float metalnessFactor = swatch0.metalness;
    
    metalnessFactor = mix(metalnessFactor, swatch1.metalness, control0Sample.r);
    metalnessFactor = mix(metalnessFactor, swatch2.metalness, control0Sample.g);
    metalnessFactor = mix(metalnessFactor, swatch3.metalness, control0Sample.b);
    
    return min(max(metalnessFactor, 0.4), 0.8);
}

float sampleRoughness (vec4 control0Sample) {
    float roughnessFactor = swatch0.roughness;
    // Seems safe to use these without checking if they exist first.
    roughnessFactor = mix(roughnessFactor, swatch1.roughness, control0Sample.r);
    roughnessFactor = mix(roughnessFactor, swatch2.roughness, control0Sample.g);
    roughnessFactor = mix(roughnessFactor, swatch3.roughness, control0Sample.b);
   

    return roughnessFactor * 0.1;
}

ScratchSwatch sampleScratchColor(vec4 sample0) {
    ScratchSwatch outSwatch;

    outSwatch.scratchMetallic = swatch1.scratch.scratchMetallic;
    outSwatch.scratchMetallic = mix(outSwatch.scratchMetallic, swatch1.scratch.scratchMetallic, sample0.r);
    outSwatch.scratchMetallic = mix(outSwatch.scratchMetallic, swatch2.scratch.scratchMetallic, sample0.g);
    outSwatch.scratchMetallic = mix(outSwatch.scratchMetallic, swatch3.scratch.scratchMetallic, sample0.b);
   
    outSwatch.scratchBrightness = swatch1.scratch.scratchBrightness;
    outSwatch.scratchBrightness = mix(outSwatch.scratchBrightness, swatch1.scratch.scratchBrightness, sample0.r);
    outSwatch.scratchBrightness = mix(outSwatch.scratchBrightness, swatch2.scratch.scratchBrightness, sample0.g);
    outSwatch.scratchBrightness = mix(outSwatch.scratchBrightness, swatch3.scratch.scratchBrightness, sample0.b);
   
    outSwatch.scratchColor = swatch1.scratch.scratchColor;
    outSwatch.scratchColor = mix(outSwatch.scratchColor, swatch1.scratch.scratchColor, sample0.r);
    outSwatch.scratchColor = mix(outSwatch.scratchColor, swatch2.scratch.scratchColor, sample0.g);
    outSwatch.scratchColor = mix(outSwatch.scratchColor, swatch3.scratch.scratchColor, sample0.b);
    
    outSwatch.scratchIOR = swatch1.scratch.scratchIOR;
    outSwatch.scratchIOR = mix(outSwatch.scratchIOR, swatch1.scratch.scratchIOR, sample0.r);
    outSwatch.scratchIOR = mix(outSwatch.scratchIOR, swatch2.scratch.scratchIOR, sample0.g);
    outSwatch.scratchIOR = mix(outSwatch.scratchIOR, swatch3.scratch.scratchIOR, sample0.b);
    
    outSwatch.scratchRoughness = swatch1.scratch.scratchIOR;
    outSwatch.scratchRoughness = mix(outSwatch.scratchRoughness, swatch1.scratch.scratchRoughness, sample0.r);
    outSwatch.scratchRoughness = mix(outSwatch.scratchRoughness, swatch2.scratch.scratchRoughness, sample0.g);
    outSwatch.scratchRoughness = mix(outSwatch.scratchRoughness, swatch3.scratch.scratchRoughness, sample0.b);

    return outSwatch;
}

float SampleSwatchEmissive (vec4 sample0) {
    float emissiveValue = swatch0.emissiveIntensity * swatch0.emissiveAmount;

    // Seems safe to use these without checking if they exist first.
    emissiveValue = mix(emissiveValue, swatch1.emissiveIntensity, sample0.r * swatch1.emissiveAmount);
    emissiveValue = mix(emissiveValue, swatch2.emissiveIntensity, sample0.g * swatch2.emissiveAmount);
    emissiveValue = mix(emissiveValue, swatch3.emissiveIntensity, sample0.b * swatch3.emissiveAmount);

    return emissiveValue;
}


// May need handling?
// EXT_color_buffer_float extension not supported.
// LOG  Warning: THREE.WebGLRenderer: EXT_texture_filter_anisotropic extension not supported.
void main() {
	// #include <clipping_planes_fragment>

	vec4 sample0 = texture2D(control0, vUv);
	vec4 asgSample = texture2D(asg, vUv);    

	// Swatch samples
	vec3 color = paintRegionBySwatch(sample0);
	float metalnessFactor = sampleMetallic(sample0);
	float roughnessFactor = sampleRoughness(sample0);


	// Todo: this isn't as "glowy" as I would expect. 
	float emissiveStrength = SampleSwatchEmissive(sample0);
	vec4 emissiveColor = vec4(vec3(1.0) * emissiveStrength, 1.0);

	// Scratches
	ScratchSwatch scratchSample = sampleScratchColor(sample0);
	float scratchScalar = asgSample.g * scratchStrength;
	color = mix(color, scratchSample.scratchColor * scratchSample.scratchBrightness, scratchScalar);
	roughnessFactor = mix(roughnessFactor, scratchSample.scratchRoughness, scratchScalar);
	metalnessFactor = mix(metalnessFactor, scratchSample.scratchMetallic, scratchScalar);

	
	vec4 diffuseColor = vec4(color, 1.0);

	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;

	#ifdef TRANSMISSION
		float totalTransmission = transmission;
	#endif
	
  	#include <logdepthbuf_fragment>
	#include <map_fragment>
	// #include <color_fragment>
	// #include <alphamap_fragment>
	// #include <alphatest_fragment>
	// #include <roughnessmap_fragment>
	// #include <metalnessmap_fragment>

	#include <normal_fragment_begin>
	#include <normal_fragment_maps>

	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	
	// #include <emissivemap_fragment>
	emissiveColor.rgb = emissiveMapTexelToLinear(emissiveColor).rgb;
	totalEmissiveRadiance *= emissiveColor.rgb;
     
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

	gl_FragColor = vec4(outgoingLight, diffuseColor.a);
	
	// Seems to desaturate colors
	#include <tonemapping_fragment>
	#include <encodings_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}
