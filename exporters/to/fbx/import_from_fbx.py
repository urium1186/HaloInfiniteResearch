import os
import sys

import fbx
from fbx import FbxStatus, FbxLayerElement, FbxDeformer, FbxSkin, FbxCluster

from configs.config import Config


class FbxModelImporter:
    def __init__(self,p_filepath=''):
        self.filepath = p_filepath
        if self.filepath == '':
            self.filepath = Config.ROOT_DIR + "\\exporters\\ref\\lef_glove_ref.fbx"
        self.manager = fbx.FbxManager.Create()
        if not self.manager:
            sys.exit(0)
        self.ios = fbx.FbxIOSettings.Create(self.manager, fbx.IOSROOT)
        self.scene = fbx.FbxScene.Create(self.manager, '')
        self.importer = None

    def importModel(self):
        self.importer = fbx.FbxImporter.Create(self.manager, '')
        # pFilename = 'H:\RE_OtherGames\HI\models\eskHI.FBX'
        pFilename = self.filepath
        if not os.path.isfile(pFilename):
            return
        lImportStatus = self.importer.Initialize(pFilename, -1,
                                                 self.manager.GetIOSettings())
        sdkVersion = self.manager.GetFileFormatVersion()
        lSDKMajor = sdkVersion[0]
        lSDKMinor = sdkVersion[1]
        lSDKRevision = sdkVersion[2]
        fileVer = self.importer.GetFileVersion()
        lFileMajor = fileVer[0]
        lFileMinor = fileVer[1]
        lFileRevision = fileVer[2]
        print('Init Fbx****************')
        print(fileVer)
        if not lImportStatus:  # Problem with the file to be imported

            error = self.importer.GetStatus().GetErrorString()
            print("Call to FbxImporter::Initialize() failed.")
            print("Error returned: %s", error.Buffer())
            if self.importer.GetStatus().GetCode() == FbxStatus.eInvalidFileVersion:
                print("FBX version number for this FBX SDK is %d.%d.%d")
                print("FBX version number for file %s is %d.%d.%d")

            return False
        print(f"FBX version number for this FBX SDK is {lSDKMajor}.{lSDKMinor}.{lSDKRevision}")

        if self.importer.IsFBX():
            print(f"FBX version number for file {pFilename} is {lFileMajor}.{lFileMinor}.{lFileRevision}")

            print("Animation Stack Information")
            lAnimStackCount = self.importer.GetAnimStackCount()
            print(f"    Number of animation stacks: {lAnimStackCount}")
            print(f"    Active animation stack: \"{self.importer.GetActiveAnimStackName()}\"")

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
        lStatus = self.importer.Import(self.scene)
        print(f"Status {lStatus}")
        print(self.scene)

    def getMesh(self) -> []:
        geo_count = self.scene.GetGeometryCount()
        mesh_array = []
        for i in range(geo_count):
            mesh = self.scene.GetGeometry(i)
            mesh_array.append(mesh)
        return mesh_array

    def displayControlsPoints(self, pMesh):
        lVertexCount = lControlPointsCount = pMesh.GetControlPointsCount()
        lControlPoints = pMesh.GetControlPoints()
        print("    Control Points")
        lSkinCount = pMesh.GetDeformerCount(FbxDeformer.eSkin)

        for lSkinIndex in range(lSkinCount):
            lSkinDeformer:FbxSkin = pMesh.GetDeformer(lSkinIndex, FbxDeformer.eSkin)
            lClusterCount = lSkinDeformer.GetClusterCount()
            for lClusterIndex in range(lClusterCount):
                lCluster: FbxCluster = lSkinDeformer.GetCluster(lClusterIndex)
                link = lCluster.GetLink()
                link_name = str(link.GetName())
                if link_name.__contains__(':'):
                    link_name = link_name.split(':')[-1]
                print(link_name)
                if not link:
                    continue
                lVertexIndexCount = lCluster.GetControlPointIndicesCount()
                for k in range(lVertexIndexCount):
                    lIndex = lCluster.GetControlPointIndices()[k];
                    # Sometimes, the mesh can have less points than at the time of the skinning
                    # because a smooth operator was active when skinning but has been deactivated during export.
                    if (lIndex >= lVertexCount):
                        continue;
                    lWeight = lCluster.GetControlPointWeights()[k];
                    debug = True


        for i in range(lControlPointsCount):
            print("        Control Point ", i)
            print("            Coordinates: ", lControlPoints[i])
            for j in  range(pMesh.GetElementNormalCount()):
                leNormals = pMesh.GetElementNormal( j)
                if leNormals.GetMappingMode() == FbxLayerElement.eByControlPoint:
                    if leNormals.GetReferenceMode() == FbxLayerElement.eDirect: # FbxGeometryElement
                        print(leNormals.GetDirectArray().GetAt(i))








