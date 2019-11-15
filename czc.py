# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.
#import ipdb
from cefpython3 import cefpython as cef
import platform
import sys, os.path

def check_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[hello_world.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

class Backend:
    def __init__(self):
        self.backend_port = None

    def JS_get_backend_port(self, js_value, js_callback):
        print "Backend::JS_get_backend_port: js_value:", js_value
        js_callback.Call(self.backend_port, None)
        
    def run_backend(self, czcapp_top):
        backend_path = os.path.join(czcapp_top, "backend/run-backend.py")
        self.backend_port = 12345

if __name__ == '__main__':
    czcapp_top = sys.argv[1]
    check_versions()

    backend = Backend()
    backend.run_backend(czcapp_top)
    
    
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    browser_settings = {
        #"file_access_from_file_urls_allowed": True,
        #"universal_access_from_file_urls_allowed": True
    }
    cef.Initialize()

    url = "file://" + os.path.join(os.path.expanduser(czcapp_top), "frontend/index.html")
    print "URL:", url
    browser = cef.CreateBrowserSync(url=url, window_title="Hello World!", settings=browser_settings)

    # see also https://github.com/cztomczak/cefpython/blob/master/examples/snippets/javascript_bindings.py
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("getBackendPort", backend.JS_get_backend_port)
    browser.SetJavascriptBindings(bindings)

    #ipdb.set_trace()
    cef.MessageLoop()
    del browser
    cef.Shutdown()
