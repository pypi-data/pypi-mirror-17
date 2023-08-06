import sys

from fabric import colors, api as fab

from fabricio import utils


def _command(
    fabric_method,
    command,
    ignore_errors=False,
    quiet=True,
    hide=('running', ),
    show=(),
    **kwargs
):
    if quiet:
        hide += ('output', 'warnings')
    log('{method}: {command}'.format(
        method=fabric_method.__name__,
        command=command,
    ))
    with fab.settings(fab.hide(*hide), fab.show(*show), warn_only=True):
        result = fabric_method(command, **kwargs)
        if not ignore_errors and result.failed:
            raise RuntimeError(result)
    return result


def run(command, sudo=False, stdout=sys.stdout, stderr=sys.stderr, **kwargs):
    fabric_method = sudo and fab.sudo or fab.run
    return _command(
        fabric_method=fabric_method,
        command=command,
        stdout=stdout,
        stderr=stderr,
        **kwargs
    )


def local(command, use_cache=False, **kwargs):
    if use_cache and command in local.cache:
        def from_cache(*args, **kwargs):
            return local.cache[command]
        return _command(
            fabric_method=from_cache,
            command=command,
            **kwargs
        )
    result = _command(
        fabric_method=fab.local,
        command=command,
        **kwargs
    )
    if use_cache:
        local.cache[command] = result
    return result
local.cache = {}


def log(message, color=colors.yellow, output=sys.stdout):
    with utils.patch(sys, 'stdout', output):
        fab.puts(color(message))
