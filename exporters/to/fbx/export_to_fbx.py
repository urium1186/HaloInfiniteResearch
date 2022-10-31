import math

import fbx
import sys

import numpy
from fbx import FbxDeformer, FbxSkin, FbxCluster, FbxAMatrix

from commons.common_utils import inSphere
from commons.logs import Log
from exporters.domain.domain_types import *
from configs.config import Config
from exporters.to.fbx.import_from_fbx import FbxModelImporter
from materials_utils import *

import mapBones

import utils


class FbxModel:
    def __init__(self, p_export_skl=True, p_skl_filepath='', p_skl_data=None):
        self.export_colours = False
        self.export_skl = False # p_export_skl
        self.export_normals = False
        self.export_tangent = False
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
        Log.Print("Fin init**********")
        return

    def fillBonesFromSkeletalInfo(self, data=None, numerate_bones=True):
        tempBones = []
        if data is None:
            f = open(
                'H:\GameDev\games-tool\  _!ExtraerModelsHalo\HaloInfinite\HaloInfiniteModelExtractor-main\skeletonInfoG.json')
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
            if True:
                index_bone = f'{i}.joint_skel:'
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
            node, mesh = self.create_mesh(lod, submesh)

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

            if len(lod.weight_indices) > 0 or submesh.rigid_node_index != -1:
                self.add_weights(mesh, lod, submesh)

            # b_unreal = False
            # if not b_unreal and not submesh.weight_pairs:
            # node.LclRotation.Set(fbx.FbxDouble3(0, 90, 0))
            #self.compareToDataInFbx(lod)
            self.scene.GetRootNode().AddChild(node)

    def export(self, save_path=None, ascii_format=False):
        """Export the scene to an fbx file."""
        temp_dir  = '/'.join(save_path.split('/')[:-1])
        Log.Print("Directory "+temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
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
        try:
            self.exporter.Initialize(save_path, b_ascii, self.manager.GetIOSettings())
            self.exporter.Export(self.scene)
            self.exporter.Destroy()
        except Exception as e:
            Log.Print(f"Error in export_to_fbx.py: {e}")

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

    def create_mesh(self, lod_n: ObjLOD, subMesh: ObjMesh):

        index_buffer_type = subMesh.index_buffer_type
        mesh = fbx.FbxMesh.Create(self.scene, lod_n.name)
        lTransformMatrix = fbx.FbxMatrix()
        if subMesh.attachment_info is not None:
            if len(self.bones) == 0:
                self.add_bones()
            debug = True
            vScl = self.scaleVector(subMesh.attachment_info.translation['x'], subMesh.attachment_info.translation['y'], subMesh.attachment_info.translation['z'], rot=0)
            lT = fbx.FbxVector4(vScl)
            # lR = fbx.FbxVector4(0.0, 90.0, 0.0)
            # lR = fbx.FbxVector4(-90.0, 180.0, 0.0)
            lR = fbx.FbxVector4(subMesh.attachment_info.rotation['x'], subMesh.attachment_info.rotation['y'], subMesh.attachment_info.rotation['z'])
            # lS = fbx.FbxVector4(254.0, 254.0, 254.0)
            # lS = fbx.FbxVector4(25.4, 25.4, 25.4)
            lS = fbx.FbxVector4(subMesh.attachment_info.scale, subMesh.attachment_info.scale, subMesh.attachment_info.scale)

            lTransformMatrix.SetTRS(lT, lR, lS)
        else:
            lT = fbx.FbxVector4(0.0, 0.0, 0.0)
            # lR = fbx.FbxVector4(0.0, 90.0, 0.0)
            # lR = fbx.FbxVector4(-90.0, 180.0, 0.0)
            lR = fbx.FbxVector4(0.0, 0.0, 0.0)
            # lS = fbx.FbxVector4(254.0, 254.0, 254.0)
            # lS = fbx.FbxVector4(25.4, 25.4, 25.4)
            lS = fbx.FbxVector4(1.0, 1.0, 1.0)


            lTransformMatrix.SetTRS(lT, lR, lS)

        if not mesh.GetLayer(0):
            mesh.CreateLayer()

        layer = mesh.GetLayer(0)

        lMaterialLayer = fbx.FbxLayerElementMaterial.Create(mesh, "Material Layers")
        lMaterialLayer.SetMappingMode(fbx.FbxLayerElement.eByPolygon)
        lMaterialLayer.SetReferenceMode(fbx.FbxLayerElement.eIndexToDirect)
        layer.SetMaterials(lMaterialLayer)
        temp = lod_n.vertex_buffer_indices
        vert_pos = temp['Position'][0]
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
        # lod_group_attr = fbx.FbxLODGroup.Create(self.scene, "LODGroup1")
        #
        # lod_group_attr.WorldSpace.Set(False)
        # lod_group_attr.MinMaxDistance.Set(False)
        # lod_group_attr.MinDistance.Set(0.0)
        # lod_group_attr.MaxDistance.Set(0.0)
        # lod_group_attr.
        # lod_group_attr.
        node.SetNodeAttribute(mesh)
        if subMesh.attachment_info is not None:
            bone_cluster = self.getFbxCluster(subMesh.attachment_info.node_index)

            lMatrix = fbx.FbxAMatrix()


            lMatrix = bone_cluster.GetTransformLinkMatrix(lMatrix)
            lMatrix1 = fbx.FbxMatrix(lMatrix)
            tras = fbx.FbxVector4()
            rota = fbx.FbxQuaternion()
            pShearing = fbx.FbxVector4()
            pScaling = fbx.FbxVector4()
            pSign = 0.0

            moved = lMatrix1 * lTransformMatrix
            moved.GetElements(tras, rota, pShearing, pScaling)
            #print("        Transform Translation: ", moved.GetT())
            print("        Transform Translation: ",tras)
            #print("        Transform Rotation: ", moved.GetR())
            print("        Transform Rotation: ", rota)
            #print("        Transform Scaling: ", moved.GetS())
            print("        Transform Scaling: ", pScaling)
            """"""
            node.LclTranslation.Set(fbx.FbxDouble3(tras[0], tras[1], tras[2]))
            #node.LclRotation.Set(fbx.FbxDouble3(lMatrix.GetR()[0], lMatrix.GetR()[1], lMatrix.GetR()[2]))
            #node.LclScaling.Set(fbx.FbxDouble3(lMatrix.GetS()[0], lMatrix.GetS()[1], lMatrix.GetS()[2]))
        # node.SetNodeAttribute(lod_group_attr)
        # node.LclRotation.Set(fbx.FbxDouble3(0, 90, 0))
        return node, mesh

    def add_tangent(self, mesh, submesh, layer):
        if not self.export_tangent:
            return
        tangentElement = fbx.FbxLayerElementTangent.Create(mesh, 'tangent')
        tangentElement.SetMappingMode(fbx.FbxLayerElement.eByControlPoint)
        tangentElement.SetReferenceMode(fbx.FbxLayerElement.eDirect)
        for i, vec in enumerate(submesh.vert_tangent):
            tangentElement.GetDirectArray().Add(fbx.FbxVector4(-vec[0], vec[2], vec[1], vec[3]))
        layer.SetNormals(tangentElement)

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
        bone_index = bone_index
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
            def_cluster.SetLinkMode(fbx.FbxCluster.eNormalize)

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
                assert len(submesh.dual_quat_weight) == 0, 'Si es linear no deberia tener DQ'
            elif obj_mesh.vert_type == VertType.dq_skinned:
                if len(submesh.weights) == len(submesh.dual_quat_weight):
                    skin.SetSkinningType(fbx.FbxSkin.eBlend)
                elif len(submesh.weights) == 0:
                    skin.SetSkinningType(fbx.FbxSkin.eDualQuaternion)
                    assert False, 'Debug si es posible q sea solo dual_Q'
                else:
                    assert len(submesh.dual_quat_weight) != 0, 'Deberia tener pesos en dual_Q'
            else:
                raise NotImplementedError('Tipo de vertice no implementado')

            """"""
            submesh.generateWeightPairs()
            for i, w in enumerate(submesh.weight_pairs):
                indices = w[0]
                weights = w[1]
                if obj_mesh.vert_type == VertType.skinned:
                    skin.AddControlPointIndex(i, 0)
                else:
                   # assert submesh.dual_quat_weight[i][4] <= 1, 'quat pesso siempre menor q 1 float'
                    assert submesh.dual_quat_weight[i] <= 1, 'quat pesso siempre menor q 1 float'
                    skin.AddControlPointIndex(i, submesh.dual_quat_weight[i])

                ctrl_ponit = mesh.GetControlPoints()[i]
                check_w = []
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
                        bone_cluster = self.getFbxCluster(bone_index)
                        """
                        lMatrix = fbx.FbxAMatrix()
                        
                        lMatrix = bone_cluster.GetTransformMatrix(lMatrix)
                        print("        Transform Translation: ", lMatrix.GetT())
                        print("        Transform Rotation: ", lMatrix.GetR())
                        print("        Transform Scaling: ", lMatrix.GetS())

                        lMatrix = bone_cluster.GetTransformLinkMatrix(lMatrix)
                        
                        print("        Transform Link Translation: ", lMatrix.GetT())
                        print("        Transform Link Rotation: ", lMatrix.GetR())
                        print("        Transform Link Scaling: ", lMatrix.GetS())
                        
                        lMatrix = bone_cluster.GetTransformLinkMatrix(lMatrix)
                        bone_transl = lMatrix.GetT()
                        a = numpy.array((ctrl_ponit[0], ctrl_ponit[1], ctrl_ponit[2]))
                        b = numpy.array((bone_transl[0], bone_transl[1], bone_transl[2]))
                        dist = numpy.linalg.norm(a - b)
                        check_w.append((bone_index, weights[j], dist))
                        """
                        bone_cluster.AddControlPointIndex(i, weights[j])
                    except IndexError:
                        pass
                if False and len(check_w) > 1:
                    sorted_by_dist = sorted(check_w, key=lambda tup: tup[2])
                    sorted_by_W = sorted(check_w, key=lambda tup: tup[1])
                    sorted_by_W_rev = sorted(check_w, key=lambda tup: tup[1], reverse=True)
                    temp_l = sorted_by_dist[-1][2] - sorted_by_dist[0][2]
                    if temp_l != 0:
                        for pos_w in enumerate(sorted_by_dist, start=1):
                            temp_l
                    if sorted_by_dist != sorted_by_W_rev:
                        debug = True
                        # for v in check_w:
                        #     print(f'w {v[1]} dist {v[2]}')

        for c_k in self.bones_index_used:
            skin.AddCluster(self.bones_index_used[c_k])

        mesh.AddDeformer(skin)

    def _getMeshData(self, mesh):
        lVertexCount = lControlPointsCount = mesh.GetControlPointsCount()
        lControlPoints = mesh.GetControlPoints()
        map_ref_vertex_key_pos = {}

        for i in range(lControlPointsCount):
            print("        Control Point ", i)
            print("            Coordinates: ", lControlPoints[i])
            coordenate = f"{lControlPoints[i][0]}_{lControlPoints[i][1]}_{lControlPoints[i][2]}"  # _{lControlPoints_iu[i][3]}
            if map_ref_vertex_key_pos.keys().__contains__(coordenate):
                map_ref_vertex_key_pos[coordenate].append(i)
            else:
                map_ref_vertex_key_pos[coordenate] = [i]

        dict_skin_w_info = {}

        lSkinCount = mesh.GetDeformerCount(FbxDeformer.eSkin)
        bones_name_pos = {}
        lSkinDeformer: FbxSkin = None
        for lSkinIndex in range(lSkinCount):
            lSkinDeformer = mesh.GetDeformer(lSkinIndex, FbxDeformer.eSkin)
            lClusterCount = lSkinDeformer.GetClusterCount()
            for lClusterIndex in range(lClusterCount):
                lCluster: FbxCluster = lSkinDeformer.GetCluster(lClusterIndex)
                link = lCluster.GetLink()
                link_name = str(link.GetName())
                if link_name.__contains__(':'):
                    link_name = link_name.split(':')[-1]

                lMatrix = fbx.FbxAMatrix()
                lMatrix = lCluster.GetTransformLinkMatrix(lMatrix)
                bone_transl = lMatrix.GetT()
                bones_name_pos[link_name] = (lMatrix.GetT(), lMatrix.GetR(), lMatrix.GetS())
                print(f'{link_name}_{(bone_transl[0], bone_transl[1], bone_transl[2])}')

                lVertexIndexCount = lCluster.GetControlPointIndicesCount()
                for k in range(lVertexIndexCount):
                    lIndex = lCluster.GetControlPointIndices()[k]
                    # Sometimes, the mesh can have less points than at the time of the skinning
                    # because a smooth operator was active when skinning but has been deactivated during export.
                    if (lIndex >= lVertexCount):
                        continue
                    lWeight = lCluster.GetControlPointWeights()[k]
                    debug = True
                    if dict_skin_w_info.keys().__contains__(lIndex):
                        dict_skin_w_info[lIndex][link_name] = lWeight
                    else:
                        dict_skin_w_info[lIndex] = {link_name: lWeight}

        return map_ref_vertex_key_pos, lControlPoints, dict_skin_w_info, bones_name_pos, lSkinDeformer

    def compareToDataInFbx(self, lod: ObjLOD):
        importer_model = FbxModelImporter(Config.ROOT_DIR + "\\exporters\\ref\\lef_glove_ref.fbx")
        importer_model.importModel()
        mesh_ref = importer_model.getMesh()[0]
        mesh_ref_data = self._getMeshData(mesh_ref)
        # importer_model_iu = FbxModelImporter(Config.MODEL_EXPORT_PATH + "\\exporters\\ref\\lef_shoulder_iu.fbx")
        # importer_model_iu.importModel()
        # mesh_iu = importer_model_iu.getMesh()[0]
        # mesh_iu_data = self._getMeshData(mesh_iu)

        geo_count = self.scene.GetGeometryCount()
        mesh_array = []
        for i in range(geo_count):
            mesh = self.scene.GetGeometry(i)
            mesh_array.append(mesh)
        mesh_in_use = mesh_array[0]
        mesh_in_use_data = self._getMeshData(mesh_in_use)

        map_ref_vertex_key_pos = mesh_ref_data[0]
        map_ref_vertex_key_pos_iu = mesh_in_use_data[0]

        lControlPoints = mesh_ref_data[1]
        lControlPoints_iu = mesh_in_use_data[1]

        dict_skin_w_info = mesh_ref_data[2]
        dict_skin_w_info_iu = mesh_in_use_data[2]

        bones_name_pos = mesh_ref_data[3]
        bones_name_pos_iu = mesh_in_use_data[3]

        count = 0
        # 248
        vert_pos_pair = {}
        w_maps = {}
        for key in map_ref_vertex_key_pos.keys():
            if not map_ref_vertex_key_pos_iu.__contains__(key):
                for key_iu in map_ref_vertex_key_pos_iu.keys():
                    ref = [lControlPoints[map_ref_vertex_key_pos[key][0]][0],
                           lControlPoints[map_ref_vertex_key_pos[key][0]][1],
                           lControlPoints[map_ref_vertex_key_pos[key][0]][2]]
                    ref_iu = [lControlPoints_iu[map_ref_vertex_key_pos_iu[key_iu][0]][0],
                              lControlPoints_iu[map_ref_vertex_key_pos_iu[key_iu][0]][1],
                              lControlPoints_iu[map_ref_vertex_key_pos_iu[key_iu][0]][2]]
                    if inSphere(ref, ref_iu, 0.2):
                        count += 1
                        if vert_pos_pair.keys().__contains__(key):
                            debug = True
                            if vert_pos_pair.values().__contains__(key_iu):
                                debug = True
                        else:
                            if list(vert_pos_pair.values()).__contains__(key_iu):
                                debug = True
                            vert_pos_pair[key] = key_iu

                        break

                debug = True
            else:
                count += 1

        contar_casos = {'caso len 1':0, 'caso len 2 inv':0, 'caso len 2 same':0, 'others': 0}
        for key in vert_pos_pair.keys():
            bone_name_list = []
            bone_w_map = dict_skin_w_info[map_ref_vertex_key_pos[key][0]]
            v_i = map_ref_vertex_key_pos_iu[vert_pos_pair[key]][0]

            wi_list = lod.weight_indices[v_i]
            b_weights = lod.weights[v_i]
            wi_w={}
            for i in map_ref_vertex_key_pos_iu[vert_pos_pair[key]]:
                for b_name in bone_w_map:
                    bone_index = self.getBoneIndexByName(lod, b_name)
                    bone_cluster = self.getFbxCluster(bone_index)
                    bone_cluster.AddControlPointIndex(i, bone_w_map[b_name])

            for i, wi in enumerate(wi_list):
                bone_info_name = lod.mesh_container.bones_data['skeletons'][wi]['name']
                bone_name_list.append(bone_info_name)
                if wi_w.__contains__(bone_info_name):
                    debug = True
                ws = b_weights[4+i]
                wi_w[bone_info_name] = ws
                if w_maps.keys().__contains__(ws):
                    w_maps[ws] += 1
                else:
                    w_maps[ws] = 1

            contained = True
            for b_n in bone_w_map.keys():
                if not bone_name_list.__contains__(b_n):
                    contained = False
                    break

            if len(bone_w_map.keys()) == len(wi_w.keys()) and len(wi_w.keys())!=1:
                l1 = list(bone_w_map.keys())
                l2 = list(wi_w.keys())
                if l1[0] == l2[0] and l1[1] == l2[1]:
                    razon1 = bone_w_map[l1[0]]/bone_w_map[l1[1]]
                    razon2 = wi_w[l2[0]]/wi_w[l2[1]]
                    debug = True
                    contar_casos['caso len 2 same']+=1
                elif l1[0] == l2[1] and l1[1] == l2[0]:
                    contar_casos['caso len 2 inv'] += 1
                else:
                    contar_casos['others'] += 1
            else:
                contar_casos['caso len 1'] += 1

            if contained:
                debug = True

        for c_k in self.bones_index_used:
            mesh_in_use_data[4].AddCluster(self.bones_index_used[c_k])
            debug = True
        print('Fin compa')

    def getBoneIndexByName(self, lod: ObjLOD, name):
        for i, bone in enumerate(lod.mesh_container.bones_data['skeletons']):
            if bone['name'] == name:
                return i


