import ipdb
import sys, os, glob
import ast

class ClassDef:
    def __init__(self, class_name):
        self.class_name = class_name
        self.methods = []

class ClassMethodDef:
    def __init__(self, class_def, method_name, method_node):
        self.class_def = class_def
        self.method_name = method_name
        self.method_args = []
        self.pass_calling_context = False
        if len(method_node.decorator_list) > 0:
            decorator = method_node.decorator_list[0].id
            if decorator == 'pass_calling_context':
                self.pass_calling_context = True

def generate_js_serverbase(class_def, out_fd):
    print("export class", class_def.class_name, "{", file = out_fd)
    print(" __call_method(method, args) {", file = out_fd)
    lbrace = "{"; rbrace = "}"
    for method in class_def.methods:
        m_code = f"""
        if (method == '{method.method_name}') {lbrace}
          return this.{method.method_name}(...args);
        {rbrace}
        """
        print(m_code, file = out_fd)

    print("""
    throw new Error("unknown method " + method);
    """, file = out_fd)

    print(" }", file = out_fd)       

    for method in class_def.methods:
        method_args = list(filter(lambda x: x != 'self', method.method_args))
        if method.pass_calling_context:
            method_args.append("ctx")
        print(f'{method.method_name}({",".join(method_args)}) {lbrace} throw new Error("not implemented"); {rbrace}', file = out_fd)

    print("};", file = out_fd)
                
def generate_js_proxy(class_def, out_fd):
    prx_class_name = class_def.class_name + "Prx"

    print("export class", prx_class_name, "{", file = out_fd)
    print("""
    constructor(ws_handler, remote_obj_id) {
      this.ws_handler = ws_handler;
      this.remote_obj_id = remote_obj_id;
    }
    """, file = out_fd)
    for method in class_def.methods:
        method_args_l = filter(lambda x: x != 'self', method.method_args)
        print("        ", file = out_fd)
        print(method.method_name, "(", ",".join(method_args_l), ") {", file = out_fd)
        method_args_l = [arg for arg in method.method_args if arg != 'self']
        print("""
        let call_req = {'obj_id': this.remote_obj_id,
                        'call_method': '%s',
                        'pass_calling_context': %s,
                        'args': JSON.stringify([%s])};
        return this.ws_handler.object_client.do_remote_call(call_req).then((ret) => {return ret});
        }
        """ % (method.method_name, "true" if method.pass_calling_context else "false", ",".join(method_args_l)), file = out_fd)

    print("};", file = out_fd)

def generate_js_file(class_defs, out_fn):
    print("out file:", out_fn)
    out_fd = open(out_fn, "w")
    for class_def in class_defs:
        generate_js_serverbase(class_def, out_fd)
        generate_js_proxy(class_def, out_fd)
    out_fd.close()

def generate_py_serverbase(class_def, out_fd):
    print("class %s:" % class_def.class_name, file = out_fd)
    for method in class_def.methods:
        method_args = list(method.method_args)
        if method.pass_calling_context:
            method_args.append("ctx")
        print("\tdef %s(%s): raise Exception('not implemented')" % (method.method_name, ",".join(method_args)), file = out_fd)

def generate_py_proxy(class_def, out_fd):
    print("class %sPrx:" % class_def.class_name, file = out_fd)
    ctor = \
"""\tdef __init__(self, ws_handler, remote_obj_id):
\t\tself.ws_handler = ws_handler
\t\tself.remote_obj_id = remote_obj_id
"""
    print(ctor, file = out_fd)
    for method in class_def.methods:
        args_l = [x for x in filter(lambda x: x != 'self', method.method_args)]
        args_l_w_self = ['self'] + args_l
        lbrace = "{"; rbrace = "}"
        method_code = f"""
\tasync def {method.method_name}({",".join(args_l_w_self)}):
\t\tcall_req = {lbrace}
\t\t\t'obj_id': self.remote_obj_id,
\t\t\t'call_method': '{method.method_name}',
\t\t\t'pass_calling_context': {method.pass_calling_context},
\t\t\t'args': json.dumps([{",".join(args_l)}])
\t\t\t{rbrace}
\t\tprint("{class_def.class_name}Prx::{method.method_name}:", call_req)
\t\tcall_ret = await self.ws_handler.object_client.do_remote_call(call_req)
\t\treturn call_ret
"""
        print(method_code, file = out_fd)
        
def generate_py_file(class_defs, out_fn):
    print("out file:", out_fn)
    out_fd = open(out_fn, "w")
    print("import json", file = out_fd)
    print("", file = out_fd)
    
    for class_def in class_defs:
        generate_py_serverbase(class_def, out_fd)
        generate_py_proxy(class_def, out_fd)
    out_fd.close()
            
def parse_pyidl_class(ast_node):
    print("class:", ast_node.name)
    class_def = ClassDef(ast_node.name)
    
    for node in ast_node.body:
        if isinstance(node, ast.FunctionDef):
            print("function:", node.name)
            #ipdb.set_trace()
            class_method = ClassMethodDef(ast_node.name, node.name, node)
            for arg_node in node.args.args:
                #ipdb.set_trace()
                print("arg:", arg_node.arg)
                class_method.method_args.append(arg_node.arg)
            class_def.methods.append(class_method)

    return class_def

def parse_file(pyidl_fn):
    source_code = "\n".join(open(pyidl_fn).readlines())
    class_defs = []
    #print source_code[:100]
    pt = ast.parse(source_code)
    #print(ast.dump(pt))
    #return None

    for node in ast.walk(pt):
        print(node, type(node))
        #ipdb.set_trace()
        if isinstance(node, ast.ClassDef):
            print("pyidl class:", node)
            class_def = parse_pyidl_class(node)
            class_defs.append(class_def)

    print("walk is done")
    return class_defs
    
if __name__ == "__main__":
    pyidl_dir = sys.argv[1]
    out_dir = sys.argv[2]
    out_lang = sys.argv[3]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    for pyidl_fn in glob.glob(os.path.join(pyidl_dir, "*.pyidl")):
        out_fn_b = os.path.join(out_dir, os.path.basename(pyidl_fn).split(".")[0])
        print("parse", pyidl_fn)
        class_defs = parse_file(pyidl_fn)
        if out_lang == "js":
            generate_js_file(class_defs, out_fn_b + ".js")
        elif out_lang == "py":
            generate_py_file(class_defs, out_fn_b + ".py")
        
    
