# load code in a folders
import os
import re
import obj2code

input_folder = 'test3'

def code2json_handle(code):
    height = int(code.split("\n")[1][len("<height> "):])
    # print("height",height)
    cmd_dict = {"<Line>":"l","<Circle>":"c","<Arc>":"a"}
    node_pattern = r"<node(\d+)> \(([^)]+)\)|<node(\d+)>  \(([^)]+)\)"
    nodes = re.findall(node_pattern, code)
    # print("nodes")
    # print(nodes)

    # Convert nodes to JSON format
    dup_dict = {}
    vertices = []
    for node in nodes:
        coords = node[-1]
        x, y = map(float, [x.replace(' ','') for x in coords.split(',')])
        v = {"x": float(x/200), "y": float(y/200)}
        for idx, vv in enumerate(vertices):
            if v == vv:
                dup_dict[len(vertices)] = idx
                break
        vertices.append(v)
    # print("vertices")
    # for idx, v in enumerate(vertices):
    #     print(idx, v)
    #     if idx in dup_dict:
    #         print('dup!',idx,'->',dup_dict[idx])
    

    # Find all face definitions
    face_pattern = r"<face>(.*?)</face>"
    faces = re.findall(face_pattern, code, re.DOTALL)

    # Convert faces to JSON format
    json_faces = []
    for face in faces:
        outer_loops = []
        loop_pattern = r"<loop type=\"outer\">(.*?)</loop>|<loop type=\"outer\" >(.*?)</loop>"
        loops = re.findall(loop_pattern, face, re.DOTALL)
        for loop in loops:
            loop = loop[-1]
            # print("loop")
            # print(loop)
            loop_data = []
            curves = [x.strip() for x in loop.strip().split('\n')]
            # print("curves")
            # print(curves)
            for curve in curves:
                splitted = curve.replace('  ',' ').split(' ')
                # print('splitted')
                # print(splitted)
                cmd, nodes = splitted[0], splitted[1:]
                loop_data.append({"type": cmd_dict[cmd], "params": [int(x[len('<node'):-1]) for x in nodes]})
            outer_loops.append(loop_data)

        inner_loops = []
        loop_pattern = r"<loop type=\"inner\">(.*?)</loop>|<loop type=\"inner\" >(.*?)</loop>"
        loops = re.findall(loop_pattern, face, re.DOTALL)
        for loop in loops:
            loop = loop[-1]
            # print("loop")
            # print(loop)
            loop_data = []
            curves = [x.strip() for x in loop.strip().split('\n')]
            # print("curves")
            # print(curves)
            for curve in curves:
                splitted =  curve.replace('  ',' ').split(' ')
                # print('splitted')
                # print(splitted)
                cmd, nodes = splitted[0], splitted[1:]
                loop_data.append({"type": cmd_dict[cmd], "params": [int(x[len('<node'):-1]) for x in nodes]})
            inner_loops.append(loop_data)
        json_faces.append({"outer": outer_loops, "inner": inner_loops})

    # Construct the final JSON structure
    result = {
        "operation": "NewBodyFeatureOperation",
        "vertices": vertices,
        "faces": json_faces,
        "extrude": {"l": 0.0, "h": float(height/200)},
        "transformations": {
            "origin": {"x": 0.0, "y": 0.0, "z": 0.0},
            "xaxis": {"x": 1, "y": 0, "z": 0},
            "yaxis": {"x": 0, "y": 1, "z": 0},
            "zaxis": {"x": 0, "y": 0, "z": 1}
        }
    }
    return result

# handle issues
# for p in code_paths:
#     print(p)
#     json_data = code2json_handle(obj2code.load_code(p))
#     print(json_data)

# convert code -> obj, handle issues

def convert_code_to_obj(code_path, obj_path):
    print(f'{code_path} -> {obj_path}')
    code_data = obj2code.load_code(code_path)
    json_data = code2json_handle(code_data)
    obj_data = obj2code.json2obj(json_data)
    obj2code.save_obj(obj_data, obj_path)


code_paths = []
for folder in os.listdir(input_folder):
    full_path = os.path.join(input_folder, folder)
    for file in os.listdir(full_path):
        if not file.endswith('.code'):
            continue
        load_path = os.path.join(full_path, file)
        save_path = os.path.join(full_path, file.replace('.code','.obj'))
        convert_code_to_obj(load_path, save_path)







