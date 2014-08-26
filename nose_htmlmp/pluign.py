__author__ = 'roy'

import multiprocessing
import os
from nose.plugins.base import Plugin

from jinja2 import Environment
from jinja2 import FileSystemLoader

import codecs

import traceback
from nose.exc import SkipTest

from nose_htmloutput import Group, id_split, nice_classname, exc_message, TEST_ID


MANAGER = multiprocessing.Manager()

MP_ERRORLIST = MANAGER.list()
MP_REPROT = MANAGER.dict()
MP_STATS = MANAGER.dict()


class HtmlMp(Plugin):
    name = 'htmlmp'
    score = 2000
    encoding = 'UTF-8'
    report_file = None

    def options(self, parser, env):
        """Sets additional command line options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            '--htmlmp-file', action='store',
            dest='htmlmp_file', metavar="FILE",
            default=env.get('NOSE_HTML_FILE', 'nosetests.html'),
            help="Path to html file to store the report in. "
                 "Default is nosetests.html in the working directory "
                 "[NOSE_HTML_FILE]")

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            self.jinja = Environment(
                loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
                trim_blocks=True,
                lstrip_blocks=True
            )
            self.stats = MP_STATS
            if not self.stats:
                self.stats.update(
                    {'errors': 0,
                     'failures': 0,
                     'passes': 0,
                     'skipped': 0})
            self.errorlist = MP_ERRORLIST
            self.report_data = MP_REPROT
            self.report_file_name = options.htmlmp_file

    def report(self, stream):
        self.report_file = codecs.open(self.report_file_name, 'w', self.encoding, 'replace')

        self.stats['total'] = sum(self.stats.values())

        for name, group in self.report_data.items():
            group.stats['total'] = sum(group.stats.values())
            self.report_data.update({name: group})

        self.report_file.write(self.jinja.get_template('report.html').render(
            report=self.report_data,
            stats=self.stats,
        ))
        self.report_file.close()
        if self.config.verbosity > 1:
            stream.writeln("-" * 70)
            stream.writeln("HTML: %s" % self.report_file.name)

    def addSuccess(self, test):
        name = id_split(test.id())
        group = self.report_data.get(name[0], Group())

        self.stats['passes'] += 1
        group.stats['passes'] += 1
        group.tests.append({
            'name': name[-1],
            'failed': False,
        })
        self.report_data.update({name[0]: group})

    def addError(self, test, err, capt=None):
        tb = ''.join(traceback.format_exception(*err))
        name = id_split(test.id())

        group = self.report_data.get(name[0], Group())

        if issubclass(err[0], SkipTest):
            type = 'skipped'
            self.stats['skipped'] += 1
            group.stats['skipped'] += 1
        else:
            type = 'error'
            self.stats['errors'] += 1
            group.stats['errors'] += 1
        group.tests.append({
            'name': name[-1],
            'failed': True,
            'type': type,
            'errtype': nice_classname(err[0]),
            'message': exc_message(err),
            'tb': tb,
        })
        self.report_data.update({name[0]: group})

    def addFailure(self, test, err, capt=None, tb_info=None):
        tb = ''.join(traceback.format_exception(*err))
        name = id_split(test.id())

        group = self.report_data.get(name[0], Group())

        self.stats['failures'] += 1
        group.stats['failures'] += 1
        group.tests.append({
            'name': name[-1],
            'failed': True,
            'errtype': nice_classname(err[0]),
            'message': exc_message(err),
            'tb': tb,
        })
        self.report_data.update({name[0]: group})
