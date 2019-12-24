#!/usr/bin/python -B
#
import os, sys

def install_cmds(top):
    cmds = []
    cmds.append("cd {top}/frontend && npm install".format(top = top))
    return cmds

def build_cmds(top):
    dd = {}
    dd["top"] = top
    dd["dipole_jsgen"] = "python {dipole_dir}/src/dipole-jsgen.py".format(dipole_dir = ".")
    dd["rollup"] = "./node_modules/rollup/dist/bin/rollup"    

    cmds = []
    cmds.append("{dipole_jsgen} {top}/frontend/gen-js {top}/backend".format(**dd))
    cmds.append("cd {top}/frontend && {rollup} -c".format(**dd))
    return cmds

def clean_cmds(top):
    cmds = []
    cmds.append("rm -f *~ {top}/frontend/package-lock.json".format(top = top))
    cmds.append("rm -rf {top}/frontend/node_modules".format(top = top))
    cmds.append("rm -rf {top}/frontend/public".format(top = top))
    cmds.append("rm -rf {top}/frontend/gen-js".format(top = top))
    return cmds

if __name__ == "__main__":
    action = sys.argv[1]
    top = sys.argv[2]

    if action == "install":
        cmds = install_cmds(top)
    elif action == "clean":
        cmds = clean_cmds(top)
    elif action == "build":
        cmds = build_cmds(top)
    else:
        raise Exception("unknown action %s" % action)

    for cmd in cmds:
        print "CMD:", cmd
        e_code = os.system(cmd)
        if e_code != 0:
            print "command failed"
            break
    
