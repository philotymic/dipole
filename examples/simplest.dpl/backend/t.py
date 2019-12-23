import ipdb
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

def generate_js_file():
    for js_class in js_classes:
        print "class", js_class.class_name + "Prx", "{"
        print """
        constructor(communicator, remote_obj_id) {
          this.communicator = communicator;
          this.remote_obj_id = remote_obj_id;
        }
        """
        for js_method in js_class.methods:
            method_args_l = filter(lambda x: x != 'self', js_method.method_args)
            print "        ",
            print js_method.method_name, "(", ",".join(method_args_l), ") {"
            method_args_l = ["'%s': %s" % (arg, arg) for arg in js_method.method_args if arg != 'self']
            print """
            let args = {'obj_id': this.remote_obj_id,
	                'call_method': '%s',
		        'args': {%s}};
	    return this.communicator.do_call(args);
            }
            """ % (js_method.method_name, ",".join(method_args_l))
            
        print "};"
        print "export default", js_class.class_name + "Prx;"
        

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
    source_code = "\n".join(open("./run-backend.py").readlines())
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
                if decorator.value.id in ["dipole","myws"] and decorator.attr == "exportclass":
                    found_dipole_export_class = True
                    break;

            if found_dipole_export_class:
                print "dipole.exportclass:", node
                handle_dipole_export_class(node)

    print "walk is done"
    print js_classes
    generate_js_file()
