import sys
import traceback

def usage():
    print('Usage: cell [module.function] [args]')
    raise QuietFailureException()


class QuietFailureException(Exception):
    pass

aliases = {
}

def parseModuleName(args):
    try:
        entryPoint = args.pop(0)
        entryPoint = aliases.get(entryPoint, entryPoint)
        splitName = entryPoint.rsplit('.', 1)
        module = splitName[0]
        entryName = splitName[1]
        return module, entryName
    except:
        usage()

def loadModule(moduleName):
    try:
        __import__(moduleName)
        return sys.modules[moduleName]
    except Exception as e:
        print(traceback.format_exc())
        raise QuietFailureException()

def launch(args):
    moduleName, entryName = parseModuleName(args)
    executeModuleMethod(moduleName, entryName, args)

def executeModuleMethod(moduleName, entryName, args):
    module = loadModule(moduleName)
    try:
        res = getattr(module, entryName)(*args)
        if res:
            print(res)
    except QuietFailureException:
        raise
    except Exception as e:
        print('Exception when executing `{}` from `{}`:'.format(entryName, moduleName))
        lines = traceback.format_exc().split('\n')
        print('\n'.join(lines[0:1] + lines[3:]))

def main():
    if '' in sys.path:  sys.path.remove('') # remove cwd from PYTHONPATH
    try:
        launch(sys.argv[1:])
    except QuietFailureException:
        sys.exit(1)
