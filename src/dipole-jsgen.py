import sys, os
import ast

class JSClassDef:
    def __init__(self, class_name):
        self.class_name = class_name
        self.methods = []

class JSClassMethodDef:
    def __init__(self, js_class, method_name):
        self.js_class = js_class
        self.method_name = method_name
        self.method_args = []

js_classes = []

def generate_js_file(out_dir):
    for js_class in js_classes:
        prx_class_name = js_class.class_name + "Prx"
        out_fd = open(os.path.join(out_dir, prx_class_name + ".js"), "w")

        print >>out_fd, "class", prx_class_name, "{"
        print >>out_fd, """
        constructor(communicator, remote_obj_id) {
          this.communicator = communicator;
          this.remote_obj_id = remote_obj_id;
        }
        """
        for js_method in filter(lambda x: x.method_name != "__init__", js_class.methods):
            method_args_l = filter(lambda x: x != 'self', js_method.method_args)
            print >>out_fd, "        ",
            print >>out_fd, js_method.method_name, "(", ",".join(method_args_l), ") {"
            method_args_l = ["'%s': %s" % (arg, arg) for arg in js_method.method_args if arg != 'self']
            print >>out_fd, """
            let args = {'obj_id': this.remote_obj_id,
	                'call_method': '%s',
		        'args': {%s}};
	    return this.communicator.do_call(args);
            }
            """ % (js_method.method_name, ",".join(method_args_l))
            
        print >>out_fd, "};"
        print >>out_fd, "export default", prx_class_name, ";"
        out_fd.close()

def handle_dipole_export_class(ast_node):
    print "class:", ast_node.name
    js_class = JSClassDef(ast_node.name)
    
    for node in ast_node.body:
        if isinstance(node, ast.FunctionDef):
            print "function:", node.name
            js_method = JSClassMethodDef(ast_node.name, node.name)
            for arg_node in node.args.args:
                print "arg:", arg_node.id
                js_method.method_args.append(arg_node.id)
            js_class.methods.append(js_method)

    js_classes.append(js_class)

if __name__ == "__main__":
    out_dir = sys.argv[1]
    py_fn = sys.argv[2]

    source_code = "\n".join(open(py_fn).readlines())
    #print source_code[:100]
    pt = ast.parse(source_code)
    #print ast.dump(pt)
    for node in ast.walk(pt):
        #print node, type(node)
        if isinstance(node, ast.ClassDef):
            decorators = node.decorator_list
            if len(decorators) == 0:
                continue
            found_dipole_export_class = False
            for decorator in decorators:
                if decorator.value.id == "libdipole" and decorator.attr == "exportclass":
                    found_dipole_export_class = True
                    break;

            if found_dipole_export_class:
                print "dipole.exportclass:", node
                handle_dipole_export_class(node)

    print "walk is done"
    print js_classes
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    generate_js_file(out_dir)
