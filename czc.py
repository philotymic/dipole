# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+.
#import ipdb
from cefpython3 import cefpython as cef
import platform
import sys

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
    url = sys.argv[1]
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    browser_settings = {
        #"file_access_from_file_urls_allowed": True,
        #"universal_access_from_file_urls_allowed": True
    }
    cef.Initialize()
    #url = "file:///home/asmirnov/czc/examples/simplest/index.html"
    #url = "file:///home/asmirnov/czc/examples/nestedmodules/index.html"
    browser = cef.CreateBrowserSync(url=url, window_title="Hello World!", settings=browser_settings)
    #ipdb.set_trace()
    cef.MessageLoop()
    cef.Shutdown()
