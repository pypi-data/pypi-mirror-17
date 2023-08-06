import click
import json
import importlib
import os
import sys

from shakedown.cli.helpers import *


@click.command('shakedown')
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('--dcos-url', help='URL to a running DCOS cluster.')
@click.option('--fail', type=click.Choice(['fast', 'never']), help='Sepcify whether to continue testing when encountering failures. (default: fast)')
@click.option('--ssh-key-file', type=click.Path(), help='Path to the SSH keyfile to use for authentication')
@click.option('--no-banner', is_flag=True, help='Suppress the product banner.')
@click.option('--quiet', is_flag=True, help='Suppress all superfluous output.')
@click.option('--report', type=click.Choice(['json', 'junit']), help='Return a report in the specified format.')
@click.option('--ssl-no-verify', is_flag=True, help='Suppress SSL certificate verification')
@click.option('--stdout', type=click.Choice(['pass', 'fail', 'skip', 'all', 'none']), help='Print the standard output of tests with the specified result. (default: fail)')
@click.option('--stdout-inline', is_flag=True, help='Display output inline rather than after test phase completion.')
@click.version_option(version=shakedown.VERSION)


def cli(**args):
    """ Main CLI entry-point; perform pre-flight and parse arguments
    """
    import shakedown

    # Read configuration options from ~/.shakedown (if exists)
    args = read_config(args)

    # Set configuration defaults
    args = set_config_defaults(args)

    if args['quiet']:
        shakedown.cli.quiet = True

    if not args['dcos_url']:
        click.secho('error: --dcos-url is a required option; see --help for more information.', fg='red', bold=True)
        sys.exit(1)

    if args['ssh_key_file']:
        shakedown.cli.ssh_key_file = args['ssh_key_file']

    if not args['no_banner']:
        echo(banner(), n=False)

    echo('Running pre-flight checks...', d='step-maj')

    # required modules and their 'version' method
    imported = {}
    requirements = {
        'pytest': '__version__',
        'dcos': 'version'
    }

    for req in requirements:
        ver = requirements[req]

        echo("Checking for {} library...".format(req), d='step-min', n=False)
        try:
            imported[req] = importlib.import_module(req, package=None)
        except ImportError:
            click.secho("error: {p} is not installed; run 'pip install {p}'.".format(p=req), fg='red', bold=True)
            sys.exit(1)

        echo(getattr(imported[req], requirements[req]))

    if args['ssl_no_verify']:
        imported['dcos'].config.set_val('core.ssl_verify', 'False')

    echo('Checking for DC/OS cluster...', d='step-min', n=False)

    with stdchannel_redirected(sys.stderr, os.devnull):
        imported['dcos'].config.set_val('core.dcos_url', args['dcos_url'])

    try:
        echo(shakedown.dcos_version())
    except:
        click.secho("error: cluster '" + args['dcos_url'] + "' is unreachable.", fg='red', bold=True)
        sys.exit(1)

    if set(['username', 'password']).issubset(args):
        echo('Authenticating with cluster...', d='step-maj')

        try:
            echo('Retrieving ACS token...', d='step-min', n=False)
            token = shakedown.authenticate(args['username'], args['password'])

            with stdchannel_redirected(sys.stderr, os.devnull):
                imported['dcos'].config.set_val('core.dcos_acs_token', token)

            echo('ok')
        except:
            click.secho("error: authentication failed.", fg='red', bold=True)
            sys.exit(1)


    class shakedown:
        """ This encapsulates a PyTest wrapper plugin
        """

        state = {}

        stdout = []

        tests = {
            'file': {},
            'test': {}
        }

        report_stats = {
            'passed':[],
            'skipped':[],
            'failed':[],
            'total_passed':0,
            'total_skipped':0,
            'total_failed':0,
        }


        def output(title, state, text, status=True):
            """ Capture and display stdout/stderr output

                :param title: the title of the output box (eg. test name)
                :type title: str
                :param state: state of the result (pass, fail)
                :type state: str
                :param text: the stdout/stderr output
                :type text: str
                :param status: whether to output a status marker
                :type status: bool
            """
            if status:
                if state == 'fail':
                    echo(fchr('FF'), d='fail')
                elif state == 'pass':
                    echo(fchr('PP'), d='pass')

            if text and args['stdout'] in [state, 'all']:
                o = decorate('Output during ', 'quote-head-' + state)
                o += click.style(decorate(title, style=state), bold=True) + "\n"
                o += decorate(str(text).strip(), style='quote-' + state)

                if args['stdout_inline']:
                    echo(o)
                    if state == 'pass':
                        echo('')
                else:
                    shakedown.stdout.append(o)


        def pytest_collectreport(self, report):
            """ Collect and validate individual test files
            """

            if not 'collect' in shakedown.state:
                shakedown.state['collect'] = 1
                echo('Collecting and validating test files...', d='step-min')

            if report.nodeid:
                echo(report.nodeid, d='item-maj', n=False)

                state = None

                if report.failed:
                    state = 'fail'
                if report.passed:
                    state = 'pass'
                if report.skipped:
                    state = 'skip'

                if state:
                    if report.longrepr:
                        shakedown.output(report.nodeid, state, report.longrepr)
                    else:
                        shakedown.output(report.nodeid, state, None)


        def pytest_sessionstart(self):
            """ Tests have been collected, begin running them...
            """

            echo('Initiating testing phase...', d='step-maj')


        def pytest_report_teststatus(self, report):
            """ Print report results to the console as they are run
            """

            try:
                report_file, report_test = report.nodeid.split('::', 1)
            except ValueError:
                return

            if not 'test' in shakedown.state:
                shakedown.state['test'] = 1
                echo('Running individual tests...', d='step-min')

            if not report_file in shakedown.tests['file']:
                shakedown.tests['file'][report_file] = 1
                echo(report_file, d='item-maj')
            if not report.nodeid in shakedown.tests['test']:
                shakedown.tests['test'][report.nodeid] = {}
                echo(report_test, d='item-min', n=False)

            if report.failed:
                shakedown.tests['test'][report.nodeid]['fail'] = True

            if report.when == 'teardown' and not 'tested' in shakedown.tests['test'][report.nodeid]:
                shakedown.output(report.nodeid, 'pass', None)

            # Suppress excess terminal output
            return report.outcome, None, None


        def pytest_runtest_logreport(self, report):
            """ Log the [stdout, stderr] results of tests if desired
            """

            state = None

            for secname, content in report.sections:
                if report.failed:
                    state = 'fail'
                if report.passed:
                    state = 'pass'
                if report.skipped:
                    state = 'skip'

                if state and report.when == 'call':
                    if 'tested' in shakedown.tests['test'][report.nodeid]:
                        shakedown.output(report.nodeid, state, content, False)
                    else:
                        shakedown.tests['test'][report.nodeid]['tested'] = True
                        shakedown.output(report.nodeid, state, content)

            # Capture execution crashes
            if hasattr(report.longrepr, 'reprcrash'):
                longreport = report.longrepr

                if 'tested' in shakedown.tests['test'][report.nodeid]:
                    shakedown.output(report.nodeid, 'fail', 'error: ' + str(longreport.reprcrash), False)

                    if args['stdout_inline']:
                        echo('')
                else:
                    shakedown.tests['test'][report.nodeid]['tested'] = True
                    shakedown.output(report.nodeid, 'fail', 'error: ' + str(longreport.reprcrash))


        def pytest_runtest_makereport(self, item, call, __multicall__):
            """ Store "simple" (pass, fail, skip) test results
            """

            report = __multicall__.execute()

            # Put job run report data into shakedown.report_status hash
            if report.passed:
                shakedown.report_stats['passed'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_passed'] += 1
            if report.failed:
                shakedown.report_stats['failed'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_failed'] += 1
            if report.skipped:
                shakedown.report_stats['skipped'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_skipped'] += 1

            return report


        def pytest_sessionfinish(self, session, exitstatus):
            """ Testing phase is complete; print extra reports (stdout/stderr, JSON) as requested
            """

            echo('Test phase completed.', d='step-maj')

            if ('stdout' in args and args['stdout']) and shakedown.stdout:
                for output in shakedown.stdout:
                    echo(output)

            if args['report'] == 'json':
                click.echo("\n" + json.dumps(shakedown.report_stats, sort_keys=True, indent=4, separators=(',', ': ')))

    opts = ['-q', '--tb=no']

    if args['fail'] == 'fast':
        opts.append('-x')

    if args['path']:
        opts.append(' '.join(args['path']))

    exitstatus = imported['pytest'].main(' '.join(opts), plugins=[shakedown()])

    sys.exit(exitstatus)
