# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.
#import ipdb
from cefpython3 import cefpython as cef
import platform
import sys, os.path
import tempfile, uuid
import subprocess, shlex, threading

class Backend:
    def __init__(self, dplapp_top, dipole_top):
        self.dplapp_top = dplapp_top
        self.dipole_top = dipole_top
        self.backend_port = None
        self.xfn = None # TemporaryFile object, used to return port number assigned by backend
        self.browser = None

    def JS_get_argv(self, js_value, js_callback):
        print "Backend::JS_get_argv"
        js_callback.Call(sys.argv, None)
        
    def JS_get_backend_port(self, js_value, js_callback):
        print "Backend::JS_get_backend_port: js_value:", js_value
        print "found port:", self.backend_port
        js_callback.Call(self.backend_port, None)

    def run_backend(self):
        self.xfn = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        backend_path = os.path.join(self.dplapp_top, "backend/run-backend.py")
        python_path = sys.executable
        cmd = "{python_path} {backend_path} {xfn}".format(python_path = python_path, backend_path = backend_path, xfn = self.xfn)
        pp = subprocess.Popen(shlex.split(cmd),
                              env = {'topdir': self.dplapp_top,
                                     'dipole_topdir': self.dipole_top})
        print "backend process pid:", pp.pid
        
        os.mkfifo(self.xfn)
        with open(self.xfn) as xfn_fifo:
            print "xfn fifo opened, waiting for backend to respond with port"
            self.backend_port = int(xfn_fifo.read())
            print "dipole runner backend port:", self.backend_port
        os.unlink(self.xfn)
        
        self.t1 = threading.Thread(target = self.backend_thread)
        self.t1.daemon = True
        self.t1.start()
        
    def backend_thread(self):
        self.browser.CloseBrowser()
        
        sys.exit(0)
        
def check_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[hello_world.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

if __name__ == '__main__':
    dipole_top = os.path.abspath(os.path.dirname(sys.argv[0]))
    dplapp_top = sys.argv[1]
    check_versions()

    backend = Backend(dplapp_top, dipole_top)
    backend.run_backend()    
    
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    browser_settings = {
        #"file_access_from_file_urls_allowed": True,
        #"universal_access_from_file_urls_allowed": True
    }
    cef.Initialize()

    url = "file://" + os.path.join(os.path.abspath(os.path.expanduser(dplapp_top)), "frontend/index.html")
    print "URL:", url
    browser = cef.CreateBrowserSync(url=url, window_title="Hello World!", settings=browser_settings)
    backend.browser = browser

    # see also https://github.com/cztomczak/cefpython/blob/master/examples/snippets/javascript_bindings.py
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("dpl_getArgv", backend.JS_get_argv)
    bindings.SetFunction("dpl_getBackendPort", backend.JS_get_backend_port)
    browser.SetJavascriptBindings(bindings)

    #ipdb.set_trace()
    cef.MessageLoop()
    del browser
    cef.Shutdown()
