from meya.util.system import NonZeroExitCode
from meya.util.system import system


async def touch(path):
    touched = True
    try:
        await system("touch", path)
    except NonZeroExitCode:
        touched = False
    return touched
