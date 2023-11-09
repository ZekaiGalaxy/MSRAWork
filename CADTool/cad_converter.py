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
            loop_type = 'outer' if command == 'out' else 'inner'
            current_face[loop_type].append([])
            current_loop = current_face[loop_type][-1]

        elif command in ['c', 'a', 'l']:
            params = list(map(int, tokens[1:]))
            face_part = {"type": command, "params": params}
            current_loop.append(face_part)

        elif command == 'Extrude':
            l, h = map(float, tokens[1:])
            data["extrude"] = {"l": l, "h": h}

        elif command.startswith('T_'):
            # Transformations
            axis = command.split('_')[1]
            if axis == 'origin':
                x, y, z = map(float, tokens[1:])
            else:
                x, y, z = map(float, tokens[1:])
            data["transformations"][axis] = {"x": x, "y": y, "z": z}

    if current_face:
        data["faces"].append(current_face)

    return data

def format_json(data):
    for v in data['vertices']:
        v['x'] = float(round(200 * v['x']) / 200)
        v['y'] = float(round(200 * v['y']) / 200)

    l,h = data['extrude']['l'], data['extrude']['h']
    data['extrude']['l'] = 0.0
    data['extrude']['h'] = float(min(200,round((h - l)*200))/200)

    data['transformations']['origin'] = {"x": 0.0, "y": 0.0, "z": 0.0}

    data['transformations']['xaxis'] = {"x": 1, "y": 0, "z": 0}
    data['transformations']['yaxis'] = {"x": 0, "y": 1, "z": 0}
    data['transformations']['zaxis'] = {"x": 0, "y": 0, "z": 1}
    return data

def json2code(data):
    codes = ["# height", f"<height> {min(200,round(200*data['extrude']['h']))}", "", "# define nodes"]

    v_idx = 0
    for v in data['vertices']:
        # codes.append(f"<node{v_idx}> "+"{"+f"x:{int(200*v['x'])},y:{int(200*v['y'])}"+"}")
        codes.append(f"<node{v_idx}> ({round(200*v['x'])},{round(200*v['y'])})")
        v_idx += 1
    codes.extend(["","# draw face"])

    def get_curve(curve):
        cmds = {"l":"<Line>","c":"<Circle>","a":"<Arc>"}
        curve_str = cmds[curve['type']]
        for node_idx in curve['params']:
            curve_str+= f" <node{node_idx}>"
        return curve_str

    for face_data in data['faces']:
        codes.append("<face>")
        for loop in face_data['outer']:
            codes.append(" "*4+'<loop type="outer">')
            for curve in loop:
                curve_str = get_curve(curve)
                codes.append(" "*8+curve_str)
            codes.append(" "*4+'</loop>')

        for loop in face_data['inner']:
            codes.append(" "*4+'<loop type="inner">')
            for curve in loop:
                curve_str = get_curve(curve)
                codes.append(" "*8+curve_str)
            codes.append(" "*4+'</loop>')
        codes.append("</face>")
    return "\n".join(codes)

def code2json(code):
    height = int(code.split("\n")[1][len("<height> "):])
    cmd_dict = {"<Line>":"l","<Circle>":"c","<Arc>":"a"}
    node_pattern = r"<node(\d+)> \(([^)]+)\)"
    nodes = re.findall(node_pattern, code)

    # Convert nodes to JSON format
    vertices = []
    for _, coords in nodes:
        x, y = map(float, coords.split(','))
        vertices.append({"x": float(x/200), "y": float(y/200)})

    # Find all face definitions
    face_pattern = r"<face>(.*?)</face>"
    faces = re.findall(face_pattern, code, re.DOTALL)

    # Convert faces to JSON format
    json_faces = []
    for face in faces:
        outer_loops = []
        loop_pattern = r"<loop type=\"outer\">(.*?)</loop>"
        loops = re.findall(loop_pattern, face, re.DOTALL)
        for loop in loops:
            loop_data = []
            curves = loop.strip().split('\n')
            for curve in curves:
                splitted = curve.strip().split(' ')
                cmd, nodes = splitted[0], splitted[1:]
                loop_data.append({"type": cmd_dict[cmd], "params": [int(x[len('<node'):-1]) for x in nodes]})
            outer_loops.append(loop_data)

        inner_loops = []
        loop_pattern = r"<loop type=\"inner\">(.*?)</loop>"
        loops = re.findall(loop_pattern, face, re.DOTALL)
        for loop in loops:
            loop_data = []
            curves = loop.strip().split('\n')
            for curve in curves:
                splitted = curve.strip().split(' ')
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

def json2obj(data):
    obj_str = "# WaveFront *.obj file\n"
    obj_str += "# ExtrudeOperation: {}\n\n".format(data["operation"])

    for vertex in data["vertices"]:
        obj_str += "v {} {}\n".format(vertex["x"], vertex["y"])

    for face in data["faces"]:
        obj_str += '\nface'
        for loop in face["outer"]:
            obj_str += '\nout\n'
            for cmd in loop:
                obj_str += "{} {}\n".format(cmd["type"], ' '.join(map(str, cmd["params"])))

        for loop in face["inner"]:
            obj_str += '\nin\n'
            for cmd in loop:
                obj_str += "{} {}\n".format(cmd["type"], ' '.join(map(str, cmd["params"])))

    obj_str += "\n\nExtrude {} {} \n".format(data["extrude"]["l"], data["extrude"]["h"])
    obj_str += "T_origin {} {} {}\n".format(data["transformations"]["origin"]["x"], data["transformations"]["origin"]["y"], data["transformations"]["origin"]["z"])
    obj_str += "T_xaxis {} {} {}\n".format(data["transformations"]["xaxis"]["x"], data["transformations"]["xaxis"]["y"], data["transformations"]["xaxis"]["z"])
    obj_str += "T_yaxis {} {} {}\n".format(data["transformations"]["yaxis"]["x"], data["transformations"]["yaxis"]["y"], data["transformations"]["yaxis"]["z"])
    obj_str += "T_zaxis {} {} {}".format(data["transformations"]["zaxis"]["x"], data["transformations"]["zaxis"]["y"], data["transformations"]["zaxis"]["z"])

    return obj_str

def obj2code(obj_data):
    json_data = obj2json(obj_data)
    formatted_json_data = format_json(json_data)
    code_data = json2code(formatted_json_data)
    return code_data

def code2obj(code_data):
    json_data = code2json(code_data)
    obj_data = json2obj(json_data)
    return obj_data

def debug(obj_path):
    obj_data = load_obj(obj_path)
    cad_utils.checkp('OBJ data',obj_data)
    json_data = obj2json(obj_data)
    cad_utils.checkp('JSON data',json_data)
    formatted_json_data = format_json(json_data)
    cad_utils.checkp('Formatted JSON data',formatted_json_data)
    code_data = json2code(formatted_json_data)
    cad_utils.checkp('CODE data',code_data)
    json_data_ = code2json(code_data)
    cad_utils.checkp('RECOVER JSON data',json_data_)
    assert json_data_ == formatted_json_data

def obj2code_with_path(obj_path, code_path):
    obj_data = cad_utils.load_text(obj_path)
    code_data = obj2code(obj_data)
    cad_utils.save_text(code_data, code_path)

def code2obj_with_path(code_path, obj_path):
    code_data = cad_utils.load_text(code_path)
    obj_data = code2obj(code_data)
    cad_utils.save_text(obj_data, obj_path)