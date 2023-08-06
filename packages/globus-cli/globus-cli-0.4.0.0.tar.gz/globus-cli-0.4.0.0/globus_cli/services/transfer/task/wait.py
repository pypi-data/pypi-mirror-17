import click
import sys
import time

from globus_cli.safeio import safeprint
from globus_cli.parsing import HiddenOption, common_options, task_id_option

from globus_cli.services.transfer.helpers import get_client


_POLLING_INTERVAL_MINIMUM = 0.1


@click.command('wait', help='Wait for a Task to complete')
@common_options
@task_id_option(helptext='ID of the Task to wait on')
@click.option('--timeout', type=int, metavar='N',
              help=('Wait N seconds. If the Task does not terminate by '
                    'then, exit with status 0'))
@click.option('--polling-interval', default=1, type=float, show_default=True,
              help=(('Number of seconds between Task status checks. '
                     'Can be a fraction of a second in decimal notation, '
                     'but has a minimum of {0}')
                    .format(_POLLING_INTERVAL_MINIMUM)))
@click.option('--heartbeat', '-H', is_flag=True,
              help=('Every polling interval, print "." to stdout to '
                    'indicate that task wait is till active'))
@click.option('--meow', is_flag=True, cls=HiddenOption)
def task_wait(meow, heartbeat, polling_interval, timeout, task_id):
    """
    Executor for `globus transfer task wait`
    """
    if polling_interval < _POLLING_INTERVAL_MINIMUM:
        raise click.UsageError(
            '--polling-interval was less than minimum of {0}'
            .format(_POLLING_INTERVAL_MINIMUM))

    client = get_client()

    def timed_out(waited_time):
        if timeout is None:
            return False
        else:
            return waited_time >= timeout

    # Tasks start out sleepy
    if meow:
        safeprint("""\
   |\      _,,,---,,_
   /,`.-'`'    -.  ;-;;,_
  |,4-  ) )-,_..;\ (  `'-'
 '---''(_/--'  `-'\_)""")

    waited_time = 0
    while not timed_out(waited_time):
        if heartbeat:
            safeprint('.', newline=False)
            sys.stdout.flush()

        task = client.get_task(task_id)

        status = task['status']
        if status != 'ACTIVE':
            if heartbeat:
                safeprint('')
            # meowing tasks wake up!
            if meow:
                safeprint("""\
                  _..
  /}_{\           /.-'
 ( a a )-.___...-'/
 ==._.==         ;
      \ i _..._ /,
      {_;/   {_//""")
            sys.exit(1)

        waited_time += polling_interval
        time.sleep(polling_interval)

    # add a trailing newline to heartbeats
    if heartbeat:
        safeprint('')
