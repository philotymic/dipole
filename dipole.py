# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.
import ipdb
from cefpython3 import cefpython as cef
import platform
import sys, os.path
import tempfile
import subprocess, shlex, threading

class Backend:
    def __init__(self, dplapp_top):
        self.dplapp_top = dplapp_top
        self.backend_port = None
        self.xfn = None # TemporaryFile object, used to return port number assigned by backend
        self.browser = None

    def JS_get_backend_port(self, js_value, js_callback):
        print "Backend::JS_get_backend_port: js_value:", js_value
        print "found port:", self.backend_port
        js_callback.Call(self.backend_port, None)

    def run_backend(self):
        self.xfn = tempfile.mkstemp()
        backend_path = os.path.join(self.dplapp_top, "backend/run-backend.py")
        python_path = sys.executable
        cmd = "{python_path} {backend_path} {xfn}".format(python_path = python_path, backend_path = backend_path, xfn = self.xfn[1])
        def setpgidfn():
            os.setpgid(0, 0)
        pp = subprocess.Popen(shlex.split(cmd), env = {'topdir': self.dplapp_top}, stdout = subprocess.PIPE) # , preexec_fn = setpgidfn)
        pgid = os.getpgid(os.getpid())
        print "pgid, pid", pgid, os.getpid()
        print "be pgid, pid", os.getpgid(pp.pid), pp.pid
        os.setpgid(0, 0) # session id -- http://www.informit.com/articles/article.aspx?p=397655&seqNum=6
        #pp.stdout.read()

        #ipdb.set_trace()
        lines = pp.stdout.readline()
        print lines

        while self.backend_port is None:
            self.backend_port = int(open(self.xfn[1]).read())
            print "dipole runner backend port:", self.backend_port
        os.unlink(self.xfn[1])            
        
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
    dplapp_top = sys.argv[1]
    check_versions()

    backend = Backend(dplapp_top)
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
    bindings.SetFunction("dpl_getBackendPort", backend.JS_get_backend_port)
    browser.SetJavascriptBindings(bindings)

    #ipdb.set_trace()
    cef.MessageLoop()
    del browser
    cef.Shutdown()
