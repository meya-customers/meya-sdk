import asyncio
import subprocess
import sys

from asyncio import Future
from asyncio.subprocess import DEVNULL
from typing import Optional
from typing import Tuple
from typing import Union


class NonZeroExitCode(Exception):
    def __init__(self, program, args, exit_code, stdout, stderr):
        super().__init__(f"{program} {args} exited with {exit_code}")
        self.program = program
        self.program_args = args
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


async def system(
    program,
    *args,
    stdin=None,
    stdout_raw=False,
    stdout_text=False,
    stdout_stripped=False,
    stderr=True,
    stderr_text=False,
    stdout_future=False,
    **kwargs,
) -> Union[None, str, bytes, Tuple[subprocess.Popen, Future]]:
    if hasattr(stdin, "read"):
        stdin_file = stdin
        stdin_text = ""
    elif isinstance(stdin, str):
        stdin_file = subprocess.PIPE
        stdin_text = stdin
    else:
        stdin_file = subprocess.PIPE
        stdin_text = ""
    capture_stdout = stdout_raw or stdout_text or stdout_stripped

    if capture_stdout:
        stdout = subprocess.PIPE
    else:
        stdout = sys.stdout

    capture_stderr = stderr and stderr_text
    if capture_stderr:
        stderr = subprocess.PIPE
    elif stderr:
        stderr = sys.stderr
    else:
        stderr = DEVNULL

    loop = asyncio.get_running_loop()
    process = subprocess.Popen(
        [program, *args],
        stdin=stdin_file,
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    async def get_output(output_future: Optional[Future] = None):
        if stdin_file == subprocess.PIPE:
            stdout, stderr = await loop.run_in_executor(
                None, lambda: process.communicate(stdin_text.encode("utf-8"))
            )
        else:
            stdout, stderr = await loop.run_in_executor(
                None, lambda: process.communicate()
            )

        output = None
        if capture_stdout:
            if stdout_raw:
                output = stdout
            else:
                stdout_text = stdout.decode("utf-8")
                if stdout_stripped:
                    stdout_text = stdout_text.strip()
                output = stdout_text

        exit_code = process.returncode
        exception = None
        if exit_code != 0:
            exception = NonZeroExitCode(
                program,
                args,
                exit_code,
                stdout.decode("utf-8")
                if isinstance(stdout, bytes)
                else stdout,
                stderr.decode("utf-8")
                if isinstance(stderr, bytes)
                else stderr,
            )

        if stdout_future and exception:
            output_future.set_exception(exception)
        elif stdout_future and output_future:
            output_future.set_result(output)
        elif exception:
            raise exception

        return output

    if stdout_future:
        output_future = loop.create_future()
        loop.create_task(get_output(output_future))
        return process, output_future
    else:
        return await get_output()


def system_sync(*args, **kwargs):
    return asyncio.run(system(*args, **kwargs))
