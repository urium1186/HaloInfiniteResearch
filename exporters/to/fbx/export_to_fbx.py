import math

import fbx
import sys

from exporters.domain.domain_types import *
from configs.config import Config
from materials_utils import *

import mapBones

import utils


class FbxModel:
    def __init__(self, p_export_skl=True, p_skl_filepath='', p_skl_data=None):
        self.export_colours = False
        self.export_skl = p_export_skl
        self.export_normals = False
        self.skl_data = p_skl_data
        self.skl_filepath = p_skl_filepath
        self.manager = fbx.FbxManager.Create()
        self.count = 0
        if not self.manager:
            sys.exit(0)
        self.myMapBones = mapBones.MapBones()
        self.ios = fbx.FbxIOSettings.Create(self.manager, fbx.IOSROOT)
        self.exporter = fbx.FbxExporter.Create(self.manager, '')
        self.scene = fbx.FbxScene.Create(self.manager, '')
        self.converter = fbx.FbxGeometryConverter(self.manager)

        self.face_counter = 0
        self.bones = []
        self.bones_index_used = {}
        self.nodes = []
        print("Fin init**********")
        return

    def fillBonesFromSkeletalInfo(self, data=None, numerate_bones=True):
        tempBones = []
        if data is None:
            f = open('H:\GameDev\games-tool\  _!ExtraerModelsHalo\HaloInfinite\HaloInfiniteModelExtractor-main\skeletonInfoG.json')
            data = json.load(f)
            # Closing file
            f.close()

        # f = open('data.json')

        # returns JSON object as
        # a dictionary

        skelInfoList = data['skeletons']
        for i in range(len(skelInfoList)):
            skelInfo = skelInfoList[i]
            index_bone = ''
            if numerate_bones:
                index_bone = str(i) + '_'
            nodeatt = fbx.FbxSkeleton.Create(self.scene, index_bone + skelInfo['name'])
            nodeatt.SetSkeletonType(fbx.FbxSkeleton.eLimbNode)

            fbxnode = fbx.FbxNode.Create(self.scene, index_bone + skelInfo['name'])
            fbxnode.SetNodeAttribute(nodeatt)
            pos = [skelInfo['pos'][0], skelInfo['pos'][1], skelInfo['pos'][2]]
            temp0 = self.scaleVector(pos[0], pos[1], pos[2], rot=0)
            fbxnode.LclTranslation.Set(fbx.FbxDouble3(temp0[0], temp0[1], temp0[2]))

            fq = fbx.FbxQuaternion(skelInfo['rotq'][0], skelInfo['rotq'][1], skelInfo['rotq'][2], skelInfo['rotq'][3])

            fa = fbx.FbxAMatrix()
            fa.SetQ(fq)

            fe = fbx.FbxVector4(fa.GetR());

            if i == 0:
                fbxnode.LclRotation.Set(fbx.FbxDouble3(fe[0], -90, -90))
            else:
                fbxnode.LclRotation.Set(fbx.FbxDouble3(fe[0], fe[1], fe[2]))

            scl = [skelInfo['scl'][0], skelInfo['scl'][1], skelInfo['scl'][1]]
            fbxnode.LclScaling.Set(fbx.FbxDouble3(scl[0], scl[2], scl[1]))
            tempBones.append(fbxnode)
            if (skelInfo['parent'] != -1):
                tempBones[skelInfo['parent']].AddChild(fbxnode)

        return tempBones

    def add(self, submesh: ObjMesh, direc="", b_unreal=False):
        for lod_i, lod in enumerate(submesh.LOD_render_data):
            lod.name = submesh.name + f"_lod_{lod_i}"
            self.count = self.count + 1
            node, mesh = self.create_mesh(lod, submesh.index_buffer_type)

            if not mesh.GetLayer(0):
                mesh.CreateLayer()
            if lod.vert_uv1:
                mesh.CreateLayer()
            layer = mesh.GetLayer(0)

            # if submesh.material:
            #    if submesh.diffuse:
            if len(lod.parts) > 0:
                for part in lod.parts:
                    nameMaterial = part.mat_string.split('/')[-1]
                    if direc == "":
                        direc = Config.EXPORTED_TEXTURE_PATH + part.mat_string + '{pc}.bitmap.tga'
                    self.apply_diffuse(nameMaterial, direc, node, part.mat_string)
                    node.SetShadingMode(fbx.FbxNode.eTextureShading)
            else:
                print(f"No tiene materiales {lod}")

            if lod.vert_uv0 or lod.vert_uv1:
                if lod.vert_uv0:
                    self.create_uv(mesh, lod, layer, "uv0")
                if lod.vert_uv1:
                    self.create_uv(mesh, lod, mesh.GetLayer(1), "uv1")
            if lod.vert_norm:
                self.add_norm(mesh, lod, layer)
            # if submesh.vert_col:
            #     self.add_vert_colours(mesh, submesh, layer)

            if len(lod.weight_indices)>0 or submesh.rigid_node_index !=-1:
                self.add_weights(mesh, lod, submesh)

            # b_unreal = False
            # if not b_unreal and not submesh.weight_pairs:
            # node.LclRotation.Set(fbx.FbxDouble3(0, 90, 0))

            self.scene.GetRootNode().AddChild(node)

    def export(self, save_path=None, ascii_format=False):
        """Export the scene to an fbx file."""

        os.makedirs('/'.join(save_path.split('/')[:-1]), exist_ok=True)
        if not self.manager.GetIOSettings():
            self.ios = fbx.FbxIOSettings.Create(self.manager, fbx.IOSROOT)
            self.manager.SetIOSettings(self.ios)

        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_MATERIAL, True)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_TEXTURE, True)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_EMBEDDED, False)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_SHAPE, True)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GOBO, False)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_ANIMATION, True)
        self.manager.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GLOBAL_SETTINGS, True)
        if ascii_format:
            b_ascii = 1
        else:
            b_ascii = -1
        self.exporter.Initialize(save_path, b_ascii, self.manager.GetIOSettings())
        self.exporter.Export(self.scene)
        self.exporter.Destroy()

    def scaleVector(self, x, y, z, scl=254.0, rot=90):
        lT = fbx.FbxVector4(0.0, 0.0, 0.0)
        lR = fbx.FbxVector4(0.0, rot, 0.0)
        # lR = fbx.FbxVector4(-90.0, 180.0, 0.0)
        # lR = fbx.FbxVector4(0.0, 0.0, 0.0)
        lS = fbx.FbxVector4(scl, scl, scl)
        # lS = fbx.FbxVector4(25.4, 25.4, 25.4)
        # lS = fbx.FbxVector4(1.0, 1.0, 1.0)

        lTransformMatrix = fbx.FbxMatrix()
        lTransformMatrix.SetTRS(lT, lR, lS)
        return lTransformMatrix.MultNormalize(fbx.FbxVector4(x, y, z))

    def create_mesh(self, lod_n: ObjLOD, index_buffer_type = IndexBufferType.triangle_list):
        mesh = fbx.FbxMesh.Create(self.scene, lod_n.name)


        lT = fbx.FbxVector4(0.0, 0.0, 0.0)
        # lR = fbx.FbxVector4(0.0, 90.0, 0.0)
        # lR = fbx.FbxVector4(-90.0, 180.0, 0.0)
        lR = fbx.FbxVector4(0.0, 0.0, 0.0)
        # lS = fbx.FbxVector4(254.0, 254.0, 254.0)
        # lS = fbx.FbxVector4(25.4, 25.4, 25.4)
        lS = fbx.FbxVector4(1.0, 1.0, 1.0)

        lTransformMatrix = fbx.FbxMatrix()
        lTransformMatrix.SetTRS(lT, lR, lS)

        if not mesh.GetLayer(0):
            mesh.CreateLayer()

        layer = mesh.GetLayer(0)

        lMaterialLayer = fbx.FbxLayerElementMaterial.Create(mesh, "Material Layers")
        lMaterialLayer.SetMappingMode(fbx.FbxLayerElement.eByPolygon)
        lMaterialLayer.SetReferenceMode(fbx.FbxLayerElement.eIndexToDirect)
        layer.SetMaterials(lMaterialLayer)
        temp = lod_n.vertex_buffer_indices
        vert_pos = temp['position'][0]
        controlpoints = [self.scaleVector(-x[0], x[2], x[1]) for x in vert_pos]
        for i, p in enumerate(controlpoints):
            mesh.SetControlPointAt(p, i)

        faces = lod_n.generateFaceIndex(index_buffer_type)

        for index, face in enumerate(faces):
            mesh.BeginPolygon(lod_n.getFaceMaterialIndex(index))
            mesh.AddPolygon(face[0])
            mesh.AddPolygon(face[1])
            mesh.AddPolygon(face[2])
            mesh.EndPolygon()
        node = fbx.FbxNode.Create(self.scene, lod_n.name)

        # if self.converter.ComputePolygonSmoothingFromEdgeSmoothing(mesh):
        #    print("Converter grpou")
        #lod_group_attr = fbx.FbxLODGroup.Create(self.scene, "LODGroup1")
        #
        # lod_group_attr.WorldSpace.Set(False)
        # lod_group_attr.MinMaxDistance.Set(False)
        # lod_group_attr.MinDistance.Set(0.0)
        # lod_group_attr.MaxDistance.Set(0.0)
        # lod_group_attr.
        # lod_group_attr.
        node.SetNodeAttribute(mesh)
        #node.SetNodeAttribute(lod_group_attr)
        # node.LclRotation.Set(fbx.FbxDouble3(0, 90, 0))
        return node, mesh


    def add_norm(self, mesh, submesh, layer):
        # Dunno where to put this, norm quat -> norm vec conversion
        # return
        if not self.export_normals:
            return 
        normElement = fbx.FbxLayerElementNormal.Create(mesh, 'norm')
        normElement.SetMappingMode(fbx.FbxLayerElement.eByControlPoint)
        normElement.SetReferenceMode(fbx.FbxLayerElement.eDirect)
        for i, vec in enumerate(submesh.vert_norm):
            normElement.GetDirectArray().Add(fbx.FbxVector4(-vec[0], vec[2], vec[1], vec[3]))
        layer.SetNormals(normElement)

    def create_uv(self, mesh, submesh, layer, uv_name):
        uvDiffuseLayerElement = fbx.FbxLayerElementUV.Create(mesh, f'{uv_name} {submesh.name}')
        uvDiffuseLayerElement.SetMappingMode(fbx.FbxLayerElement.eByControlPoint)
        uvDiffuseLayerElement.SetReferenceMode(fbx.FbxLayerElement.eDirect)
        if uv_name == "uv0":
            for i, p in enumerate(submesh.vert_uv0):
                uvDiffuseLayerElement.GetDirectArray().Add(fbx.FbxVector2(p[0], p[1]))
        elif uv_name == "uv1":
            for i, p in enumerate(submesh.vert_uv1):
                uvDiffuseLayerElement.GetDirectArray().Add(fbx.FbxVector2(p[0], p[1]))
        layer.SetUVs(uvDiffuseLayerElement, fbx.FbxLayerElement.eTextureDiffuse)

    def add_vert_colours(self, mesh, submesh, layer):
        if not self.export_colours:
            return 
        vertColourElement = fbx.FbxLayerElementVertexColor.Create(mesh, f'colour')
        vertColourElement.SetMappingMode(fbx.FbxLayerElement.eByControlPoint)
        vertColourElement.SetReferenceMode(fbx.FbxLayerElement.eDirect)
        for i, p in enumerate(submesh.vertex_colour):
            vertColourElement.GetDirectArray().Add(fbx.FbxColor(p[0], p[1], p[2], p[3]))
        layer.SetVertexColors(vertColourElement)

    def apply_diffuse(self, tex_name, tex_path, node, mat_path=""):
        """Bad function that shouldn't be used as shaders should be, but meh"""
        lMaterialName = utils.normalize_material_name(tex_name)
        lMaterial = fbx.FbxSurfacePhong.Create(self.scene, lMaterialName)
        lMaterial.DiffuseFactor.Set(1)
        lMaterial.ShadingModel.Set('Phong')
        node.AddMaterial(lMaterial)

        load_material(mat_path)

        gTexture = fbx.FbxFileTexture.Create(self.scene, f'Diffuse Texture {tex_name}')
        lTexPath = tex_path
        gTexture.SetFileName(lTexPath)
        gTexture.SetRelativeFileName(lTexPath)
        gTexture.SetTextureUse(fbx.FbxFileTexture.eStandard)
        gTexture.SetMappingType(fbx.FbxFileTexture.eUV)
        gTexture.SetMaterialUse(fbx.FbxFileTexture.eModelMaterial)
        gTexture.SetSwapUV(False)
        gTexture.SetTranslation(0.0, 0.0)
        gTexture.SetScale(1.0, 1.0)
        gTexture.SetRotation(0.0, 0.0)

        if lMaterial:
            lMaterial.Diffuse.ConnectSrcObject(gTexture)
        else:
            raise RuntimeError('Material broken somewhere')

    def add_bones(self):
        self.bones = self.fillBonesFromSkeletalInfo(self.skl_data, False)
        self.scene.GetRootNode().AddChild(self.bones[0])

    def getFbxCluster(self, bone_index):
        if self.bones_index_used.keys().__contains__(bone_index):
            return self.bones_index_used[bone_index]
        else:
            bone = self.bones[bone_index]
            def_cluster = fbx.FbxCluster.Create(self.scene, 'BoneWeightCluster')
            def_cluster.SetLink(bone)
            """
            eNormalize 	
            In mode eNormalize, the sum of the weights assigned to a control point is normalized to 1.0.
    
            Setting the associate model in this mode is not relevant. The influence of the link is a function of the displacement of the link node relative to the node containing the control points.
    
            Search for all occurrences
            eAdditive 	
            In mode eAdditive, the sum of the weights assigned to a control point is kept as is.
    
            It is the only mode where setting the associate model is relevant. The influence of the link is a function of the displacement of the link node relative to the node containing the control points or, if set, the associate model. The weight gives the proportional displacement of a control point. For example, if the weight of a link over a control point is set to 2.0, a displacement of the link node of 1 unit in the X direction relative to the node containing the control points or, if set, the associate model, triggers a displacement of the control point of 2 units in the same direction.
    
            Search for all occurrences
            eTotalOne 	
            Mode eTotalOne is identical to mode eNormalize except that the sum of the weights assigned to a control point is not normalized and must equal 1.0.
    
            Search for all occurrences
            """
            def_cluster.SetLinkMode(fbx.FbxCluster.eTotalOne)

            transform = bone.EvaluateGlobalTransform()
            def_cluster.SetTransformLinkMatrix(transform)
            self.bones_index_used[bone_index] = def_cluster
            return self.bones_index_used[bone_index]

    def add_weights(self, mesh, submesh: ObjLOD, obj_mesh: ObjMesh):
        if not self.export_skl:
            return
        if len(self.bones) == 0:
            self.add_bones()
        skin = fbx.FbxSkin.Create(self.scene, '')
        self.bones_index_used.clear()
        if obj_mesh.rigid_node_index != -1 and obj_mesh.vert_type == VertType.rigid:
            skin.SetSkinningType(fbx.FbxSkin.eRigid)
            bone_index = obj_mesh.rigid_node_index
            if len(self.bones) < bone_index:
                print(
                    f'Bone index longer than bone clusters, could not add weights ({bone_index} > {len(self.bones)})')
                return
            for v_i in range(submesh.vert_count):
                self.getFbxCluster(bone_index).AddControlPointIndex(v_i, 1)
        elif obj_mesh.rigid_node_index == -1 and obj_mesh.vert_type == VertType.rigid_boned:
            skin.SetSkinningType(fbx.FbxSkin.eRigid)
            for v_i, v_b_i in enumerate(submesh.weight_indices):
                bone_index = v_b_i[0]

                if len(self.bones) < bone_index:
                    print(
                        f'Bone index longer than bone clusters, could not add weights ({bone_index} > {len(self.bones)})')
                    return
                self.getFbxCluster(bone_index).AddControlPointIndex(v_i, 1)
        else:
            skin.SetSkinningType(fbx.FbxSkin.eLinear)

            if obj_mesh.vert_type == VertType.skinned:
                skin.SetSkinningType(fbx.FbxSkin.eLinear)
            elif obj_mesh.vert_type == VertType.dq_skinned:
                debug = 1
                #skin.SetSkinningType(fbx.FbxSkin.eDualQuaternion)
            """"""
            submesh.generateWeightPairs()
            for i, w in enumerate(submesh.weight_pairs):
                indices = w[0]
                weights = w[1]
                skin.AddControlPointIndex(i, 1)
                for j in range(len(indices)):
                    if len(self.bones) < indices[j]:
                        print(
                            f'Bone index longer than bone clusters, could not add weights ({indices[j]} > {len(self.bones)})')
                        return
                    try:
                        bone_index = indices[j]
                        index = -1
                        if index > -1:
                            bone_index = index
                        if math.isnan(weights[j]):
                            debug = -1
                        self.getFbxCluster(bone_index).AddControlPointIndex(i, weights[j])
                    except IndexError:
                        pass

        for c_k in self.bones_index_used:
            skin.AddCluster(self.bones_index_used[c_k])

        mesh.AddDeformer(skin)
