import json
import pickle

def load_obj(path):
    with open(path, 'r') as f:
        return f.read()

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_code(path):
    with open(path, 'r') as f:
        return f.read()

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def save_obj(data, path):
    with open(path, 'w') as f:
        f.write(data)

def save_code(data, path):
    with open(path, 'w') as f:
        f.write(data)
    
def checkp(name, data):
    print('='*20+' '+name+' '+'='*20)
    print(data)
    print('')

def obj2json(obj_data):
    lines = obj_data.split('\n')[2:]
    lines = [x.strip() for x in lines if x!="\n"]

    data = {
        "operation": "NewBodyFeatureOperation",
        "vertices": [],
        "faces": [],
        "extrude": {},
        "transformations": {}
    }

    current_face = None

    for line in lines:
        tokens = line.split()
        if not tokens:
            continue

        command = tokens[0]

        if command == 'v':
            x, y = map(float, tokens[1:])
            data["vertices"].append({"x": x, "y": y})

        elif command == 'face':
            if current_face:
                data["faces"].append(current_face)
            current_face = {"outer": [], "inner": []}

        elif command in ['out', 'in']:
            current_face_part = 'outer' if command == 'out' else 'inner'

        elif command in ['c', 'a', 'l']:
            params = list(map(int, tokens[1:]))
            face_part = {"type": command, "params": params}
            current_face[current_face_part].append(face_part)

        elif command == 'Extrude':
            l, h = map(float, tokens[1:])
            data["extrude"] = {"l": l, "h": h}

        elif command.startswith('T_'):
            # Transformations
            axis = command.split('_')[1]
            if axis == 'origin':
                x, y, z = map(float, tokens[1:])
            else:
                x, y, z = map(int, tokens[1:])
            data["transformations"][axis] = {"x": x, "y": y, "z": z}

    if current_face:
        data["faces"].append(current_face)

    return data

def json2code(data):
    pass

def code2json(data):
    pass

def json2obj(data):
    obj_str = "# WaveFront *.obj file\n"
    obj_str += "# ExtrudeOperation: {}\n\n".format(data["operation"])

    for vertex in data["vertices"]:
        obj_str += "v {} {}\n".format(vertex["x"], vertex["y"])

    obj_str += "\nface\nout\n"
    for face in data["faces"]:
        for outer in face["outer"]:
            obj_str += "{} {}\n".format(outer["type"], ' '.join(map(str, outer["params"])))

    obj_str += "\n\nExtrude {} {} \n".format(data["extrude"]["l"], data["extrude"]["h"])
    obj_str += "T_origin {} {} {}\n".format(data["transformations"]["origin"]["x"], data["transformations"]["origin"]["y"], data["transformations"]["origin"]["z"])
    obj_str += "T_xaxis {} {} {}\n".format(data["transformations"]["xaxis"]["x"], data["transformations"]["xaxis"]["y"], data["transformations"]["xaxis"]["z"])
    obj_str += "T_yaxis {} {} {}\n".format(data["transformations"]["yaxis"]["x"], data["transformations"]["yaxis"]["y"], data["transformations"]["yaxis"]["z"])
    obj_str += "T_zaxis {} {} {}".format(data["transformations"]["zaxis"]["x"], data["transformations"]["zaxis"]["y"], data["transformations"]["zaxis"]["z"])

    return obj_str

def format_json(data):
    for v in data['vertices']:
        v['x'] = float(int(200 * v['x']) / 200)
        v['y'] = float(int(200 * v['y']) / 200)

    l,h = data['extrude']['l'], data['extrude']['h']
    data['extrude']['l'] = 0.0
    data['extrude']['h'] = h - l

    data['transformations']['origin'] = {"x": 0.0, "y": 0.0, "z": 0.0}

    data['transformations']['xaxis'] = {"x": 1, "y": 0, "z": 0}
    data['transformations']['yaxis'] = {"x": 0, "y": 1, "z": 0}
    data['transformations']['zaxis'] = {"x": 0, "y": 0, "z": 1}
    return data

# Use the function to parse the CAD file
if __name__ == '__main__':
    path = 'example_obj/00000/00000_000_param.obj'
    obj_data = load_obj(path)
    checkp('OBJ data',obj_data)
    json_data = obj2json(obj_data)
    checkp('JSON data',json_data)
    # obj_data_ = json2obj(json_data)
    # checkp('RECOVER OBJ data',obj_data_)
    # save_obj(obj_data_,'example_obj/00000/recover.obj')
    # assert obj_data == obj_data_
    formatted_json_data = format_json(json_data)
    checkp('Formatted JSON data',formatted_json_data)

