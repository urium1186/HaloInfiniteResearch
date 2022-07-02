import json
import fbx
import js2py
# Opening JSON file
import pyfbxMod
import utilsWeb

global data

#js2py.translate_file('utils.js', 'utilsWeb.py')

#f = open('meshGroup.json')
f = open('olympusJsonBody.json')
#f = open('data.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list

# Closing file
f.close()

"""
webUtils = js2py.require('utils.js')
"""




#a = utilsWeb.
#f1 = js2py.eval_js("function $(name) {return name.length}")
#print( f1("Hello world"))


class Mesh:
    def __init__(self):
        self.vert_pos = []
        self.vert_uv0 = []
        self.vert_uv1 = []
        self.vert_norm = []
        self.vert_tangent = []
        self.faces = []
        self.name = ""
        self.weight_indices = []
        self.weights = []
        self.weight_pairs = []
        self.parts = []


atributesMap = {
'vert_pos':'position',
'vert_uv0':'uv',
'vert_uv1':'uv2',
'vert_norm':'normal',
'weight_indices':'skinIndex',
'weights':'skinWeight',
}

"""
['nUVLayers', 'index', 'position', 'skinWeight', 'skinIndex', 'uvs', 'faceNormals', 'vertexNormals', 'faceColor', 'vertexColor', 'materialIndices']
"""

global meshJson

meshJson = {
    'mesh' : None
}

def searchMeshIn(childrens):
    meshFound = []
    for item in childrens:
        if item['type'] == "Group":
            for m in searchMeshIn(item['children']):
                meshFound.append(m)
        else:
            if item['type'] == "SkinnedMesh":
                meshFound.append(create_mesh_form_geometry(item['geometry']['attributes']))
                if meshJson['mesh'] == None:
                    meshJson['mesh'] =  item
    return meshFound

def create_mesh_form_geometry(geometry):
    mesh = Mesh()
    for x in atributesMap.keys():
        if  not geometry.keys().__contains__(atributesMap[x]):
            continue
        tempA = []
        mesh.__setattr__(x, [])
        count = geometry[atributesMap[x]]['count']
        itemSize = geometry[atributesMap[x]]['itemSize']
        values = [z for z in geometry[atributesMap[x]]['array'].values()]
        for j in range(0, count * itemSize, itemSize):
            tempA.append([x for x in values[j:j + itemSize]])
        mesh.__setattr__(x, tempA)
    mesh.name = 'temp'
    for k in range(0, len(mesh.vert_pos), 3):
        mesh.faces.append([k, k + 1, k + 2])
    if (len(mesh.weight_indices) == len(mesh.weights)):
        mesh.weight_pairs = []
        for w in range(len(mesh.weight_indices)):
            mesh.weight_pairs.append([mesh.weight_indices[w],mesh.weights[w]])
    return mesh

def searchMeshInWebJson():
    meshFound = []
    for x in data['parts'].keys():
        if data['parts'][x].keys().__contains__('model'):
            model = utilsWeb.PyJsHoisted_a_(data['parts'][x]['model'])
            model = model.own['object']
            model = model['value']

            print(model.own.keys())
            mesh = Mesh()
            mesh.name = x

            mesh.vert_pos = []


            for k in range(int(len(model["position"])/3)):
                mesh.vert_pos.append([model['position'][k].value,model['position'][k+1].value,model['position'][k+2].value])
            """
            #mesh.vert_uv0 = model['uvs'][0]
            #mesh.vert_uv1 = model['uvs'][1]
            """
            mesh.weight_indices = []
            mesh.weights = []
            """"
            for i in range(len(mesh.vert_pos)):
                if len(mesh.weight_indices) == 1:
                    mesh.weight_indices.append([model['skinIndices'][0]])
                    mesh.weights.append([model['skinWeights'][0]])
                else:
                    mesh.weight_indices.append(model['skinIndices'][i:i+2])
                    mesh.weights.append(model['skinWeights'][i:i+2])
            """

            mesh.weight_pairs = []
            for w in range(len(mesh.weight_indices)):
                mesh.weight_pairs.append([mesh.weight_indices[w], mesh.weights[w]])

            for k in range(0, len(mesh.vert_pos), 3):
                mesh.faces.append([k, k + 1, k + 2])

            meshFound.append(mesh)

        elif data.parts[x].keys().__contains__('models'):
            wer = 2
        else:
            debug = True

    return meshFound

meshes = searchMeshInWebJson()


model = pyfbxMod.Model()
#model.fillBonesFromSkinMesh(meshJson['mesh'])
for m in meshes:
    model.add(m)
item_name = data['name']
save_path = f"H:/RE_OtherGames/HI/models/{item_name}.fbx"
model.export(save_path)
print(f"Saved model to {save_path}")