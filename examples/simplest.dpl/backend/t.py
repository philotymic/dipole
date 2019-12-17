import ipdb
import ast

def handle_dipole_export_class(ast_node):
    print "class:", ast_node.name
    for node in ast_node.body:
        if isinstance(node, ast.FunctionDef):
            print "function:", node.name
            for arg_node in node.args.args:
                print "arg:", arg_node.id

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
                if decorator.value.id == "dipole" and decorator.attr == "exportclass":
                    found_dipole_export_class = True
                    break;

            if found_dipole_export_class:
                print "dipole.exportclass:", node
                handle_dipole_export_class(node)

    
