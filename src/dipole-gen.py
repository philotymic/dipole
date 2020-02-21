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
            dcr = method_node.decorator_list[0].id
            if dcr == 'pass_calling_context':
                self.pass_calling_context = True

def generate_js_file(class_defs, out_fn):
    print("out file:", out_fn)
    out_fd = open(out_fn, "w")
    for class_def in class_defs:
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
            method_args_l = ["'%s': %s" % (arg, arg) for arg in method.method_args if arg != 'self']
            print("""
            let call_req = {'obj_id': this.remote_obj_id,
	                    'call_method': '%s',
                            'pass_calling_context': %s,
		            'args': JSON.stringify({%s})};
	    return this.ws_handler.object_client.do_remote_call(call_req).then((ret) => {return ret});
            }
            """ % (method.method_name, "true" if method.pass_calling_context else "false", ",".join(method_args_l)), file = out_fd)
            
        print("};", file = out_fd)

    out_fd.close()

def generate_py_file(class_defs, out_fn):
    print("out file:", out_fn)
    out_fd = open(out_fn, "w")
    for class_def in class_defs:
        print("class %s:" % class_def.class_name, file = out_fd)
        for method in class_def.methods:
            method_args = method.method_args
            if method.pass_calling_context:
                method_args.append("ctx")
            print("\tdef %s(%s): raise Exception('not implemented')" % (method.method_name, ",".join(method_args)), file = out_fd)
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
        
    
