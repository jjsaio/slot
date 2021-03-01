
import datetime
import json
import os
import random
import re
import shutil
import string
import sys
import subprocess
import time
from fnmatch import fnmatch


def flatten(listOfLists):
    return [item for sublist in listOfLists for item in sublist]

def stamp(dayOnly = True, seconds = False):
    return datetime.datetime.now().strftime('%Y%m%d' if dayOnly else '%Y%m%d_%H%M%S' if seconds else '%Y%m%d_%H%M')

def normalizePath(path):
    return os.path.realpath(os.path.expanduser(path))

def ensureFolderExists(inPath, wipe = False):
    path = os.path.expanduser(inPath)
    exists = os.path.exists(path)
    if wipe and exists:
        shutil.rmtree(path)
        exists = False
    if not exists:
        os.makedirs(path)
    return path

def findInPath(pathPattern, path):
    result = []
    for root, dirs, files in os.walk(normalizePath(path)):
        for name in files:
            fpath = os.path.join(root, name)
            if fnmatch(fpath, pathPattern):
                result.append(fpath)
    return result

def dataWithFileAtPath(path):
    with open(path, 'rb') as f:
        return f.read()

def strWithFileAtPath(path):
    with open(path, 'r') as f:
        return f.read()

def fileSize(path, noRaiseOnError = False):
    try:
        return os.stat(path).st_size
    except:
        if noRaiseOnError:
            return -1
        raise

def fileModificationTime(path, noRaiseOnError = False):
    try:
        return os.stat(path).st_mtime
    except:
        if noRaiseOnError:
            return 0
        raise

def collapseuser(path):
    ''' Convert a path from "/User/steve/some/path" to "~/some/path". '''
    return path.replace(os.path.expanduser('~'), '~', 1)

def generateIdentifier(len=6, charRange='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    return ''.join(random.choice(charRange) for i in range(int(len)))

# usage: `jjsa.util.moduleFile(__file__, 'foo.json')` will return
# foo.json in the same folder as the file of the caller
def moduleFile(script_file, *filenameParts):
    return os.path.join(os.path.dirname(os.path.realpath(script_file)), *filenameParts)

def writeDataToFileAtPath(inData, path, skipIfNoDiff = False, overwriteReadonly = False):
    if isinstance(inData, str):
        data = inData.encode()
    else:
        data = inData
    if os.path.exists(path):
        if skipIfNoDiff:
            try:
                existing = dataWithFileAtPath(path)
                if existing == data:
                    return
            except:
                pass
        if overwriteReadonly:
            os.remove(path)
    with open(path, 'wb') as f:
        f.write(data)

def appendDataToFileAtPath(inData, path, createIfMissing = False):
    if not os.path.exists(path):
        if not createIfMissing:
            raise Exception("Missing file: {}".format(path))
        writeDataToFileAtPath(inData, path)
    else:
        if isinstance(inData, str):
            data = inData.encode()
        else:
            data = inData
        with open(path, 'ab') as f:
            f.write(data)

def makeBytes(obj):
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, str):
        return obj.encode()
    else:
        raise Exception('Unexpected type for makeString: {}'.format(obj))

def makeString(obj):
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, bytes):
        return obj.decode()
    else:
        raise Exception('Unexpected type for makeString: {}'.format(obj))

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s

def naturalSortKey(text):
    return [ tryint(c) for c in re.split('([0-9]+)', text) ]

def naturalSort(listOfStrings):
    return listOfStrings.sort(key=naturalSortKey)

def jsonAtPath(path, emptyIfMissing = False):
    if emptyIfMissing  and  not os.path.exists(path):
        return {}
    return json.loads(strWithFileAtPath(path))

def writeJsonToPath(dictionary, path, pretty = False, skipIfNoDiff = False, overwriteReadonly = False):
    return writeDataToFileAtPath(json.dumps(dictionary, sort_keys = pretty, indent = 4 if pretty else None, separators = (',', ': ') if pretty else None),
                                 path,
                                 skipIfNoDiff = skipIfNoDiff,
                                 overwriteReadonly = overwriteReadonly)

def prettyJsonPath(path):
    path = os.path.expanduser(path)
    writeJsonToPath(jsonAtPath(path), path, pretty = True)

def prettyJson(dict):
    return json.dumps(dict, sort_keys = True, indent = 4, separators = (',', ': '))

def sanitise(string, replace_char = '_', skinny = False):
    res = ''.join(ch if ch.isalnum() else replace_char for ch in string)
    if skinny:
        res = '_'.join([x for x in res.split('_') if x])
    return res
sanitised = sanitise

def timeDurationString(stamp):
    if stamp < 1:
        return "{:.2f}ms".format(1000*stamp)
    if stamp < 60:
        return "{}s".format(int(stamp))
    if stamp < 3600:
        return "{}m".format(int(stamp/60))
    if stamp < 48*3600:
        return "{}h".format(int(stamp/3600))
    else:
        return "{}d".format(int(stamp/(3600 * 24)))

def agoStringWithLongAgoFormat(stamp, timeFormat = None, longAgoFormat = None):
    now = time.time()
    if stamp > now - 120:
        return "Just now"
    if stamp > now - 3600:
        return "{}m ago".format(int((now - stamp)/60))
    if stamp > now - 6*3600:
        return "{}h ago".format(int((now - stamp)/3600))
    dt = datetime.datetime.fromtimestamp(stamp)
    if datetime.date.today() == datetime.date.fromtimestamp(stamp):
        return "Today {}".format(dt.strftime(timeFormat or "%H:%M"))
    if datetime.date.today() == datetime.date.fromtimestamp(stamp - 3600 * 24):
        return "Yesterday {}".format(dt.strftime(timeFormat or "%H:%M"))
    return dt.strftime(longAgoFormat or "%m/%d {}".format(dt.strftime(timeFormat or "%H:%M")))
agoString = agoStringWithLongAgoFormat

def shellOpen(path, cwd = None, args = None):
    if sys.platform == 'darwin':
        openTool = 'open'
    elif sys.platform == 'linux':
        openTool = 'xdg-open'
    else:
        raise("Unknown platform type for shellOpen: {}".format(sys.platform))
    cmd = [ openTool ]
    if args:
        cmd += args
    cmd.append(path)
    subprocess.check_call(cmd, cwd=cwd)

def shellReveal(path, cwd = None):
    if sys.platform == 'darwin':
        shellOpen(path, cwd = cwd, args = [ '-R' ])
    elif sys.platform == 'linux':
        # TODO: this doesn't really do the same thing, but not sure if reveal is supported on ubuntu...
        shellOpen(os.path.dirname(path), cwd = cwd)
    else:
        raise("Unknown platform type for shellOpen: {}".format(sys.platform))

def confirm(promptText, default = False, useHelper = True, abortOnNo = False):
    if useHelper:
        prompt = "{} ({}/{}) ".format(promptText, "Y" if default else "y", "n" if default else "N")
    else:
        prompt = promptText
    resp = input(prompt)
    if not resp:
        if abortOnNo and (not default):
            print("Abort.")
            os._exit(-1)
        return default
    if resp.lower() in [ "y", "yes", "1", "t", "true" ]:
        return True
    elif resp.lower() in [ "n", "no", "0", "f", "false" ]:
        if abortOnNo:
            print("Abort.")
            os._exit(-1)
        return False
    else:
        return confirm(promptText, default, useHelper)

def displayTime(interval_input, useDays = True):
    interval = float(interval_input)
    if interval < 0.001:
        return '{:.2f}us'.format(interval / 0.000001)
    elif interval < 1:
        return '{:.2f}ms'.format(interval / 0.001)
    elif interval < 60:
        return '{:.2f}s'.format(interval)
    elif interval < 3600:
        mins = int(interval / 60.0)
        return '{}m{}s'.format(mins, int(interval - 60 * mins))
    elif not useDays or interval < 24 * 3600:
        hours = int(interval / 3600.0)
        return '{}h{}m'.format(hours, int(interval / 60.0 - 60 * hours))
    else:
        days = int(interval / (24.0 * 3600.0))
        hours = int(interval / 3600.0 - days * 24)
        mins = int(interval / 60.0 - days * 24 * 60 - hours * 60)
        return '{}d{}h{}m'.format(days, hours, mins)
display_time = displayTime

def hexlify(data):
    return data.hex() if data else None

def unhexlify(string):
    return bytes.fromhex(string) if string else None

def waitForCondition(condLambda, timeout = 5.0, pollInterval = 0.1, raiseOnTimeout = True):
    start = time.time()
    while not condLambda():
        if timeout and (time.time() - start > timeout):
            if raiseOnTimeout:
                raise Exception("wait timeout")
            else:
                return
        time.sleep(pollInterval)

_g_registered = { }
# call this at the global scope to enable the ability to use, e.g.
#  `kill -14 <PID>`
# this will dump all stack traces to sys.stderr
# 14 = SIGALRM, probably a safe one that isn't otherwise used?
def registerFaultHandler(signum = 14):
    if _g_registered:
        return
    import faulthandler
    faulthandler.register(signum)
    _g_registered[1] = 1
    print("[INFO] faulthandler registered for SIG={}, use `kill -{} {}` to view all stack traces".format(signum, signum, os.getpid()))
