import fbx
import sys
import os

import json
import pythreejs as ptj

from fbx import FbxStatus

from materials_utils import *

import mapBones

import utils
import jsonref


class Model:
    def __init__(self, p_export_skl = True, p_skl_filepath = ''):
        self.export_skl = p_export_skl
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
        self.nodes = []

        if self.export_skl:
            from_fbx = False
            if not from_fbx:
                self.bones = self.fillBonesFromSkeletalInfo(False)
                self.scene.GetRootNode().AddChild(self.bones[0])
            else:
                self.importSkl()
                self.fillBones()
                self.bones = self.nodes


        print("Fin init**********")
        return

    def importSkl(self):
        self.importer = fbx.FbxImporter.Create(self.manager, '');
        #pFilename = 'H:\RE_OtherGames\HI\models\eskHI.FBX'
        pFilename = self.skl_filepath
        if not os.path.isfile(pFilename):
            return
        lImportStatus = self.importer.Initialize(pFilename, -1,
                                                 self.manager.GetIOSettings());
        sdkVersion = self.manager.GetFileFormatVersion()
        lSDKMajor = sdkVersion[0]
        lSDKMinor = sdkVersion[1]
        lSDKRevision = sdkVersion[2]
        fileVer = self.importer.GetFileVersion();
        lFileMajor = fileVer[0]
        lFileMinor = fileVer[1]
        lFileRevision = fileVer[2]
        print('Init Fbx****************')
        print(fileVer)
        if not lImportStatus:  # Problem with the file to be imported

            error = self.importer.GetStatus().GetErrorString();
            print("Call to FbxImporter::Initialize() failed.");
            print("Error returned: %s", error.Buffer());
            if self.importer.GetStatus().GetCode() == FbxStatus.eInvalidFileVersion:
                print("FBX version number for this FBX SDK is %d.%d.%d");
                print("FBX version number for file %s is %d.%d.%d");

            return False;
        print(f"FBX version number for this FBX SDK is {lSDKMajor}.{lSDKMinor}.{lSDKRevision}")

        if self.importer.IsFBX():
            print(f"FBX version number for file {pFilename} is {lFileMajor}.{lFileMinor}.{lFileRevision}");

            print("Animation Stack Information");
            lAnimStackCount = self.importer.GetAnimStackCount();
            print(f"    Number of animation stacks: {lAnimStackCount}");
            print(f"    Active animation stack: \"{self.importer.GetActiveAnimStackName()}\"");

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

        print(self.scene)
        lStatus = self.importer.Import(self.scene);
        print(f"Status {lStatus}")
        print(self.scene)

    def fillBones(self, bone = None):
        if bone is None:
            self.getNodes(self.scene.GetRootNode())
        else:
            self.getNodes(bone)

    def getBonePath(self, root, path:str):
        root_path = root['parent']['$ref']
        clean = path.replace(root_path,'',1)
        childss = clean.split('["children"]')
        childsss = childss[2:]
        if len(childsss) == 0:
            return root

        children = root['children']
        ch_n = {}
        for ch in childsss:
            k = int(ch.replace('[','').replace(']',''))
            ch_n = children[k]
            children = ch_n['children']

        return  ch_n

    def fillBonesFromSkeletalInfo(self, nomerate_bones = True):
        tempBones = []
        f = open('H:\GameDev\games-tool\  _!ExtraerModelsHalo\HaloInfinite\HaloInfiniteModelExtractor-main\skeletonInfoG.json')
        # f = open('data.json')

        # returns JSON object as
        # a dictionary
        data = json.load(f)
        skelInfoList = data['skeletons']
        for i in range(len(skelInfoList)):
            skelInfo = skelInfoList[i]
            index_bone = ''
            if nomerate_bones:
                index_bone = str(i) + '_'
            nodeatt = fbx.FbxSkeleton.Create(self.scene, index_bone + skelInfo['name'])
            nodeatt.SetSkeletonType(fbx.FbxSkeleton.eLimbNode)

            fbxnode = fbx.FbxNode.Create(self.scene, index_bone + skelInfo['name'])
            fbxnode.SetNodeAttribute(nodeatt)
            pos = [skelInfo['pos'][0], skelInfo['pos'][1], skelInfo['pos'][2]]
            temp0 = []
            if i == 0:
                temp0 = self.scaleVector(pos[0], pos[1], pos[2], rot=0)
            else:
                temp0 = self.scaleVector(pos[0], pos[1], pos[2], rot=0)
            fbxnode.LclTranslation.Set(fbx.FbxDouble3(temp0[0],temp0[1],temp0[2]))

            rot = [skelInfo['rot'][0], skelInfo['rot'][1], skelInfo['rot'][1]]

            fq = fbx.FbxQuaternion(skelInfo['rotq'][0],skelInfo['rotq'][1],skelInfo['rotq'][2],skelInfo['rotq'][3])

            fa = fbx.FbxAMatrix()
            fa.SetQ(fq)

            fe = fbx.FbxVector4(fa.GetR());
            if i ==0:
                fbxnode.LclRotation.Set(fbx.FbxDouble3(fe[0], -90, -90))
            else:
                fbxnode.LclRotation.Set(fbx.FbxDouble3(fe[0], fe[1], fe[2]))

            scl = [skelInfo['scl'][0], skelInfo['scl'][1], skelInfo['scl'][1]]
            fbxnode.LclScaling.Set(fbx.FbxDouble3(scl[0], scl[2], scl[1]))
            tempBones.append(fbxnode)
            if (skelInfo['parent'] != -1):
                tempBones[skelInfo['parent']].AddChild(fbxnode)
        # Iterating through the json
        # list

        # Closing file
        f.close()
        return tempBones

    def fillBonesFromSkinMesh(self, p_json):
        root_bone = p_json['children'][0]

        root_path = root_bone['parent']['$ref']
        skel = p_json['skeleton']
        skl_bones: [] = skel['bones']
        array = []
        tempBones = []
        for i, bone_ref in enumerate(skl_bones):
            bone_info_path = bone_ref['$ref']

            bone_info = self.getBonePath(root_bone,bone_info_path)
            bone_info['up'] = [v for k, v in bone_info['up'].items()]
            bone_info['position'] = [v for k, v in bone_info['position'].items()]
            bone_info['quaternion'] = [v for k, v in bone_info['quaternion'].items()]
            bone_info['rotation'] = [v for k, v in bone_info['rotation'].items()]
            bone_info['scale'] = [v for k, v in bone_info['scale'].items()]
            bone_info['matrix'] = bone_info['matrix']['elements']
            bone_info['matrixWorld'] = bone_info['matrixWorld']['elements']
            loader = json.loads(json.dumps(bone_info))
            bl = ptj.Bone(**loader)
            v = ptj.Vector3()
            #v.setFromMatrixPosition(bl.matrix)
            #ptj.Vector3.setFromMatrixPosition(bl.matrix)
            print(bl.name)
            #boneTj= loader.load(bone_info)
            nodeatt = fbx.FbxSkeleton.Create(self.scene, bone_info['name'])
            nodeatt.SetSkeletonType(fbx.FbxSkeleton.eLimbNode)

            fbxnode = fbx.FbxNode.Create(self.scene, bone_info['name'])
            fbxnode.SetNodeAttribute(nodeatt)
            pos = [0.0, 0.0, 0.0]
            #pos = [bone_info['position']['x'], bone_info['position']['y'], bone_info['position']['z']]
            pos = bl.position
            fbxnode.LclTranslation.Set(fbx.FbxDouble3(pos[0],pos[1],pos[2]))
            rot = [0.0, 0.0, 0.0]
            #rot = [bone_info['rotation']['_x'], bone_info['rotation']['_y'], bone_info['rotation']['_z']]
            rot = bl.rotation
            fbxnode.LclRotation.Set(fbx.FbxDouble3(rot[0],rot[2],-rot[1]))
            #fbxnode.LclScaling.Set(fbx.FbxDouble3(bone_info['scale']['x'], bone_info['scale']['y'], bone_info['scale']['z']))
            transform: fbx.FbxMatrix = fbxnode.EvaluateGlobalTransform()

            lT = fbx.FbxVector4(pos[0],pos[1],pos[2])
            lT = fbx.FbxVector4(0.0, 0.0, 0.0)
            lR = fbx.FbxVector4(0,0,0)
            lS = fbx.FbxVector4(1.0, 1.0, 1.0)

            lTransformMatrix = fbx.FbxMatrix()
            lTransformMatrix.SetTRS(lT, lR, lS)
            t = lTransformMatrix.MultNormalize(fbx.FbxVector4(pos[0],pos[1],pos[2]))
            fbxnode.LclTranslation.Set(fbx.FbxDouble3(t[0],t[1],t[2]))

            c1 = []
            c2 = []
            c3 = []
            c4 = []
            """"
            lTransformMatrix = fbx.FbxMatrix()
            useGlobal = True
            if useGlobal:
                for p in range(4):
                    c1.append(bone_info['matrixWorld'][p])
                    c2.append(bone_info['matrixWorld'][p+4])
                    c3.append(bone_info['matrixWorld'][p+8])
                    c4.append(bone_info['matrixWorld'][p+12])
            else:
                for p in range(4):
                    c1.append(bone_info['matrix'][p])
                    c2.append(bone_info['matrix'][p+4])
                    c3.append(bone_info['matrix'][p+8])
                    c4.append(bone_info['matrix'][p+12])

            #c1 = bone_info['matrixWorld']['elements'][0:4]
            #c2 = bone_info['matrixWorld']['elements'][4:8]
            #c3 = bone_info['matrixWorld']['elements'][8:12]
            #c4 = bone_info['matrixWorld']['elements'][11:16]

            lTransformMatrix.SetRow(0 , fbx.FbxVector4(c1[0],c1[1],c1[2],c1[3]))
            lTransformMatrix.SetRow(1 , fbx.FbxVector4(c2[0],c2[1],c2[2],c2[3]))
            lTransformMatrix.SetRow(2 , fbx.FbxVector4(c3[0],c3[1],c3[2],c3[3]))
            lTransformMatrix.SetRow(3 , fbx.FbxVector4(c4[0],c4[1],c4[2],c4[3]))
            tv= fbx.FbxVector4(0,0,0,0)
            tq= fbx.FbxQuaternion(0,0,0,1)
            tr= fbx.FbxVector4(0,0,0,0)
            ts= fbx.FbxVector4(0,0,0,0)
            lTransformMatrix.GetElements(tv,tq,tr,ts)
            a = tv[0]
            fbxnode.LclTranslation.Set(fbx.FbxDouble3(tv[0], tv[1], tv[2]))
            fbxnode.LclRotation.Set(fbx.FbxDouble3(tr[0], tr[1], tr[2]))
            fbxnode.LclScaling.Set(fbx.FbxDouble3(ts[0], ts[1], ts[2]))
            rot = [0.0, 0.0, 0.0]
            """
            # rot = [bone_info['rotation']['_x'], bone_info['rotation']['_z'], bone_info['rotation']['_y']]
            #fbxnode.LclRotation.Set(fbx.FbxDouble3(tr[0], tr[1], tr[2]))
            #fbxnode.SetTransformLinkMatrix(transform)
            #self.bones.append(fbxnode)
            boneNode = None
            #asd = fbx.FbxNode()
            tempBones.append(self.bones[0])
            for iBone in self.bones:
                if iBone.GetName() == bl.name.replace('skel:',''):
                    tempBones.append(iBone)
                    self.bones.remove(iBone)
                else:
                    a = 1

            index = -1
            for p, parent in enumerate(skl_bones):
                if (bone_info['parent']['$ref'] == parent['$ref']):
                    index = p
                    break
            #self.scene.GetRootNode().AddChild(fbxnode)
            continue
            if (index == -1) and i == 0:
                self.scene.GetRootNode().AddChild(fbxnode)
            else:
                self.bones[index].AddChild(fbxnode)
        print(tempBones)
        for o in self.bones:
            print(f"Missing Bone {o.GetName()}")
        self.bones = tempBones

    def getNodes(self, node):
        self.nodes.append(node)

        # print(f" {node.GetSrcObjectCount()} of source objects with which this object connects" )
        # print(f"\"{node.GetName()}\",")
        for i in range(node.GetChildCount()):
            # print(node.GetChild(i).GetNodeAttribute().GetAttributeType() ) # eSkeleton = 3
            # print(node.GetChild(i).GetNodeAttribute().GetNodeCount() ) # eSkeleton = 3
            self.getNodes(node.GetChild(i))

    def myCreateACubeTutorial(self, submesh=None, direc="", b_unreal=False):
        print(f"myAdd a Cube")

        print(f"fin myAdd a Cube")

    def add(self, submesh, direc="", b_unreal=False):
        submesh.name = submesh.name + '_' +str(self.count)
        self.count = self.count +1
        node, mesh = self.create_mesh(submesh)

        if not mesh.GetLayer(0):
            mesh.CreateLayer()
        if submesh.vert_uv1:
            mesh.CreateLayer()
        layer = mesh.GetLayer(0)

        # if submesh.material:
        #    if submesh.diffuse:
        if len(submesh.parts) > 0:
            for part in submesh.parts:
                nameMaterial = part.mat_string.split('/')[-1]
                self.apply_diffuse(nameMaterial, f'{direc}/textures/{nameMaterial}.dds', node, part.mat_string)
                node.SetShadingMode(fbx.FbxNode.eTextureShading)
        else:
            print(f"No tiene materiales {submesh}")

        if submesh.vert_uv0 or submesh.vert_uv1:
            if submesh.vert_uv0:
                self.create_uv(mesh, submesh, layer, "uv0")
            if submesh.vert_uv1:
                self.create_uv(mesh, submesh, mesh.GetLayer(1), "uv1")
        if submesh.vert_norm:
            self.add_norm(mesh, submesh, layer)
        # if submesh.vert_col:
        #     self.add_vert_colours(mesh, submesh, layer)

        if submesh.weight_pairs:
            self.add_weights(mesh, submesh, "")

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

    def scaleVector(self,x,y,z,scl=254.0,rot = 90):
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

    def create_mesh(self, submesh):
        mesh = fbx.FbxMesh.Create(self.scene, submesh.name)

        lT = fbx.FbxVector4(0.0, 0.0, 0.0)
        lR = fbx.FbxVector4(0.0, 90.0, 0.0)
        #lR = fbx.FbxVector4(-90.0, 180.0, 0.0)
        #lR = fbx.FbxVector4(0.0, 0.0, 0.0)
        lS = fbx.FbxVector4(254.0, 254.0, 254.0)
        #lS = fbx.FbxVector4(25.4, 25.4, 25.4)
        #lS = fbx.FbxVector4(1.0, 1.0, 1.0)

        lTransformMatrix = fbx.FbxMatrix()
        lTransformMatrix.SetTRS(lT, lR, lS)

        if not mesh.GetLayer(0):
            mesh.CreateLayer()

        layer = mesh.GetLayer(0)

        lMaterialLayer = fbx.FbxLayerElementMaterial.Create(mesh, "Material Layers")
        lMaterialLayer.SetMappingMode(fbx.FbxLayerElement.eByPolygon)
        lMaterialLayer.SetReferenceMode(fbx.FbxLayerElement.eIndexToDirect)
        layer.SetMaterials(lMaterialLayer)

        controlpoints = [self.scaleVector(-x[0], x[2], x[1]) for x in submesh.vert_pos]
        for i, p in enumerate(controlpoints):
            mesh.SetControlPointAt(p, i)

        for index, face in enumerate(submesh.faces):
            mesh.BeginPolygon(utils.getFaceMaterialIndex(index, submesh))
            mesh.AddPolygon(face[0])
            mesh.AddPolygon(face[1])
            mesh.AddPolygon(face[2])
            mesh.EndPolygon()
        node = fbx.FbxNode.Create(self.scene, submesh.name)

        # if self.converter.ComputePolygonSmoothingFromEdgeSmoothing(mesh):
        #    print("Converter grpou")
        node.SetNodeAttribute(mesh)
        # node.LclRotation.Set(fbx.FbxDouble3(0, 90, 0))
        return node, mesh

    def add_norm(self, mesh, submesh, layer):
        # Dunno where to put this, norm quat -> norm vec conversion
        # return
        normElement = fbx.FbxLayerElementNormal.Create(mesh, 'norm')
        normElement.SetMappingMode(fbx.FbxLayerElement.eByControlPoint)
        normElement.SetReferenceMode(fbx.FbxLayerElement.eDirect)
        for i, vec in enumerate(submesh.vert_norm):
            normElement.GetDirectArray().Add(fbx.FbxVector4(-vec[0], vec[2], vec[1],vec[3]))
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

    def add_temp_bones(self):
        for i in range(120):
            nodeatt = fbx.FbxSkeleton.Create(self.scene, str(i))
            nodeatt.SetSkeletonType(fbx.FbxSkeleton.eLimbNode)
            fbxnode = fbx.FbxNode.Create(self.scene, str(i))
            fbxnode.SetNodeAttribute(nodeatt)
            # fbxnode.LclRotation.Set(fbx.FbxDouble3(-90, 0, 180))
            self.bones.append(fbxnode)
            self.scene.GetRootNode().AddChild(fbxnode)

    def getBoneIndexByNamePart(self, namePart = ''):
        start = namePart.find('parts_')
        end = namePart.find('_model') + 6
        t_name_part = namePart[ start: end]
        if t_name_part == '':
            #print(f"error {namePart}")
            return 1
        bone_name = utils.parst_bones_rel[t_name_part][0]
        bone_name = bone_name.split(':')[-1]
        for i, bone in enumerate(self.bones):
            t_name = bone.GetName()
            if t_name.find(bone_name) >-1:
                return i
        return -1

    def add_weights(self, mesh, submesh, name):
        if not self.export_skl:
            return
        if len(self.bones) == 0:
            self.add_temp_bones()
        skin = fbx.FbxSkin.Create(self.scene, name)
        bone_cluster = []
        for bone in self.bones:
            def_cluster = fbx.FbxCluster.Create(self.scene, 'BoneWeightCluster')
            def_cluster.SetLink(bone)
            def_cluster.SetLinkMode(fbx.FbxCluster.eNormalize)
            bone_cluster.append(def_cluster)

            transform = bone.EvaluateGlobalTransform()
            def_cluster.SetTransformLinkMatrix(transform)

        for i, w in enumerate(submesh.weight_pairs):
            indices = w[0]
            weights = w[1]
            for j in range(len(indices)):
                if len(bone_cluster) < indices[j]:
                    print(
                        f'Bone index longer than bone clusters, could not add weights ({indices[j]} > {len(bone_cluster)})')
                    return
                try:
                    bone_index = indices[j]
                    index = self.getBoneIndexByNamePart(submesh.name)
                    index = -1#self.getBoneIndexByNamePart(submesh.name)
                    if index > -1:
                        bone_index = index
                    #if utils.sklMap.keys().__contains__(indices[j]):
                    #    bone_index = utils.sklMap[indices[j]]
                    bone_cluster[bone_index].AddControlPointIndex(i, weights[j])
                    continue
                    if not self.myMapBones.mapBones[indices[j]] == "replace":
                        indx = self.myMapBones.bonesNames.index(self.myMapBones.mapBones[indices[j]])
                        bone_cluster[indx].AddControlPointIndex(i, weights[j])
                except IndexError:
                    pass

        for c in bone_cluster:
            skin.AddCluster(c)

        mesh.AddDeformer(skin)