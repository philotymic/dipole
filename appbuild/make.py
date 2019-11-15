#!/usr/bin/python -B
#
import os, sys
from topdir import topdir

def install_cmds(top):
    cmds = []
    cmds.append("cd {top}/frontend && npm install".format(top = top))
    cmds.append("cd {top}/frontend && mkdir src/gen-js".format(top = top))
    return cmds

def build_cmds(top):
    cmds = []
    cmds.append("cat {top}/backend/backend.ice > {top}/frontend/src/gen-js/all-mods.ice".format(top=top))
    cmds.append("(cd {top}/frontend && ./node_modules/slice2js/build/Release/slice2js --output-dir src/gen-js -I./node_modules/slice2js/ice/slice src/gen-js/all-mods.ice)".format(top=top))
    cmds.append("(cd {top}/frontend && ./node_modules/rollup/dist/bin/rollup -c)".format(top=top))
    return cmds

def clean_cmds(top):
    cmds = []
    cmds.append("rm -f {top}/frontend/package-lock.json".format(top = top))
    cmds.append("rm -rf {top}/frontend/node_modules".format(top = top))
    cmds.append("rm -rf {top}/frontend/public".format(top = top))
    cmds.append("rm -rf {top}/frontend/src/gen-js".format(top = top))
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
        print cmd
        os.system(cmd)
    
