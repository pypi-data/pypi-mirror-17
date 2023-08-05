# -*- coding: utf-8 -*-

import logging
import signal
import sys
import codecs
import os

import mamonsu.lib.platform as platform
from mamonsu.lib.parser import parse_args, print_help
from mamonsu.lib.config import Config
from mamonsu.lib.supervisor import Supervisor
from mamonsu.lib.plugin import Plugin
from mamonsu.lib.zbx_template import ZbxTemplate

from mamonsu.tools.report.start import run_report
from mamonsu.tools.tune.start import run_tune
from mamonsu.tools.zabbix_cli.start import run_zabbix
from mamonsu.tools.agent.start import run_agent


def start():

    def quit_handler(_signo=None, _stack_frame=None):
        logging.info("Bye bye!")
        sys.exit(0)

    signal.signal(signal.SIGTERM, quit_handler)
    if platform.LINUX:
        signal.signal(signal.SIGQUIT, quit_handler)

    commands = sys.argv[1:]
    if len(commands) > 0:
        tool = commands[0]
        if tool == 'report':
            sys.argv.remove('report')
            return run_report()
        elif tool == 'tune':
            sys.argv.remove('tune')
            return run_tune()
        elif tool == 'zabbix':
            sys.argv.remove('zabbix')
            return run_zabbix()
    if len(commands) > 0:
        if tool == 'agent':
            sys.argv.remove('agent')
            return run_agent()
        elif tool == 'export':
            args, commands = parse_args()
            cfg = Config(args.config_file)
            if not len(commands) == 3:
                print_help()
            elif commands[1] == 'config':
                with open(commands[2], 'w') as fd:
                    cfg.config.write(fd)
                    sys.exit(0)
            elif commands[1] == 'template':
                plugins = []
                for klass in Plugin.get_childs():
                    plugins.append(klass(cfg))
                template = ZbxTemplate(args.template, args.application)
                with codecs.open(commands[2], 'w', 'utf-8') as f:
                    f.write(template.xml(plugins))
                    sys.exit(0)
            else:
                print_help()

    args, commands = parse_args()
    cfg = Config(args.config_file)
    # write pid file
    if args.pid is not None:
        try:
            with open(args.pid, 'w') as pidfile:
                pidfile.write(str(os.getpid()))
        except Exception as e:
            sys.stderr.write('Can\'t write pid file, error: %s'.format(e))
            sys.exit(2)

    supervisor = Supervisor(cfg)

    try:
        logging.info("Start mamonsu")
        supervisor.start()
    except KeyboardInterrupt:
        quit_handler()
