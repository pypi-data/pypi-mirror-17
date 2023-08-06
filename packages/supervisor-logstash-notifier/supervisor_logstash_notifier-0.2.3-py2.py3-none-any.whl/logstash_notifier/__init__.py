#!/usr/bin/env python
#
# Copyright 2016 Dohop hf.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A module for dispatching Supervisor PROCESS_STATE events to a Syslog instance
"""

import argparse
import logging
import os
import signal
import sys
import warnings

import logstash


def get_headers(line):
    """
    Parse Supervisor message headers.
    """
    return dict([x.split(':') for x in line.split()])


def eventdata(payload):
    """
    Parse a Supervisor event.
    """
    if '\n' in payload:
        headerinfo, data = payload.split('\n', 1)
    else:
        headerinfo = payload
        data = ''
    headers = get_headers(headerinfo)
    return headers, data


def send_ready(stdout):
    """
    Sends the READY signal to supervisor
    """
    stdout.write('READY\n')
    stdout.flush()


def send_ok(stdout):
    """
    Sends an ack to supervisor
    """
    stdout.write('RESULT 2\nOK')
    stdout.flush()


def supervisor_events(stdin, stdout, *events):
    """
    Runs forever to receive supervisor events
    """
    while True:
        send_ready(stdout)

        line = stdin.readline()
        headers = get_headers(line)

        payload = stdin.read(int(headers['len']))
        event_body, event_data = eventdata(payload)

        if headers['eventname'] not in events:
            send_ok(stdout)
            continue

        if event_body['processname'] == 'logstash-notifier':
            send_ok(stdout)
            continue

        yield headers, event_body, event_data

        send_ok(stdout)


def get_value_from_input(text):
    """
    Parses the input from the command line to work out if we've been given the
    name of an environment variable to include or a keyval of arbitrary data to
    include instead
    """
    values = {}
    if '=' in text:
        key, val = text.split('=', 1)
        values[key] = val
    else:
        if text in os.environ:
            values[text] = os.getenv(text)
    return values


def __newline_formatter(func):
    """
    Wrap a formatter function so a newline is appended if needed to the output
    """
    def __wrapped_func(*args, **kwargs):
        """
        Wrapper function that appends a newline to result of original fucntion
        """
        result = func(*args, **kwargs)

        # The result may be a string, or bytes. In python 2 they are the
        # same, but in python 3, they are not. First, check for strings
        # as that works the same in python 2 and 3, THEN check for bytes,
        # as that implementation is python 3 specific. If it's neither
        # (future proofing), we use a regular new line
        line_ending = "\n"
        if isinstance(result, str):
            line_ending = "\n"
        elif isinstance(result, bytes):
            # We are redefining the variable type on purpose since python
            # broke backwards compatibility between 2 & 3. Pylint will
            # throw an error on this, so we have to disable the check.
            # pylint: disable=redefined-variable-type
            line_ending = b"\n"

        # Avoid double line endings
        if not result.endswith(line_ending):
            result = result + line_ending

        return result

    # Return the wrapper
    return __wrapped_func


def get_logger(append_newline=False):
    """
    Sets up the logger used to send the supervisor events and messages to
    the logstash server, via the socket type provided, port and host defined
    in the environment
    """

    try:
        host = os.environ['LOGSTASH_SERVER']
        port = int(os.environ['LOGSTASH_PORT'])
        socket_type = os.environ['LOGSTASH_PROTO']
    except KeyError:
        sys.exit("LOGSTASH_SERVER, LOGSTASH_PORT and LOGSTASH_PROTO are "
                 "required.")

    logstash_handler = None
    if socket_type == 'udp':
        logstash_handler = logstash.UDPLogstashHandler
    elif socket_type == 'tcp':
        logstash_handler = logstash.TCPLogstashHandler
    else:
        raise RuntimeError('Unknown protocol defined: %r' % socket_type)

    logger = logging.getLogger('supervisor')
    handler = logstash_handler(host, port, version=1)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # To be able to append newlines to the logger output, we'll need to
    # wrap the formatter. As we can't predict the formatter class, it's
    # easier to wrap the format() function, which is part of the logger
    # spec than it is to override/wrap the formatter class, whose name
    # is determined by the logstash class.
    if append_newline:
        handler.formatter.format = \
            __newline_formatter(handler.formatter.format)

    return logger


def application(include=None, capture_output=False, append_newline=False):
    """
    Main application loop.
    """
    logger = get_logger(append_newline=append_newline)

    events = ['BACKOFF', 'FATAL', 'EXITED', 'STOPPED', 'STARTING', 'RUNNING']
    events = ['PROCESS_STATE_' + state for state in events]

    if capture_output:
        events += ['PROCESS_LOG_STDOUT', 'PROCESS_LOG_STDERR']

    for headers, event_body, event_data in supervisor_events(
            sys.stdin, sys.stdout, *events):
        extra = event_body.copy()
        extra['eventname'] = headers['eventname']

        if include is not None:
            user_data = {}
            for variable in include:
                user_data.update(get_value_from_input(variable))

            if len(user_data) > 0:
                extra['user_data'] = user_data

        # Events, like starting/stopping don't have a message body and
        # the data is set to '' in event_data(). Stdout/Stderr events
        # do have a message body, so use that if it's present, or fall
        # back to eventname/processname if it's not.
        if not len(event_data) > 0:
            event_data = '%s %s' % (
                headers['eventname'],
                event_body['processname']
            )

        logger.info(event_data, extra=extra)


def run_with_coverage():  # pragma: no cover
    """
    Invoked when `-c|--coverage` is used on the command line
    """
    try:
        import coverage
    except ImportError:
        warnings.warn(
            'Coverage data will not be generated because coverage is not '
            'installed. Please run `pip install coverage` and try again.'
        )
        return

    coverage.process_startup()
    # need to register a shutdown handler for SIGTERM since it won't run the
    # atexit functions required by coverage
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))


def main():  # pragma: no cover
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--include',
        nargs='*', default=list(),
        help='include named environment variables and/or arbitrary metadata '
             'keyvals in messages')
    parser.add_argument(
        '-c', '--coverage',
        action='store_true', default=False,
        help='enables coverage when running tests'
    )
    parser.add_argument(
        '-o', '--capture-output',
        action='store_true', default=False,
        help='capture stdout/stderr output from supervisor '
             'processes in addition to events'
    )
    parser.add_argument(
        '-n', '--append-newline',
        action='store_true', default=False,
        help='ensure all messages sent end with a newline character'
    )
    args = parser.parse_args()
    if args.coverage:
        run_with_coverage()

    application(
        include=args.include,
        capture_output=args.capture_output,
        append_newline=args.append_newline,
    )


if __name__ == '__main__':  # pragma: no cover
    main()
