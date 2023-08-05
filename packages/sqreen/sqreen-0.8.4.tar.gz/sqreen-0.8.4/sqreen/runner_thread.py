# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Sqreen Python agent thread composition
"""
import os
import sys
import time
import atexit
import threading
import traceback

from random import randint
from threading import Thread, Event
from logging import getLogger

from sqreen.session import Session, InvalidToken
from sqreen.runtime_infos import RuntimeInfos
from sqreen.http_client import Urllib3Connection
from sqreen.runner import Runner, CappedQueue, RunnerStop, MAX_QUEUE_LENGTH, MAX_OBS_QUEUE_LENGTH
from sqreen.config import Config
from sqreen.remote_command import RemoteCommand
from sqreen.deliverer import SimpleDeliverer
from sqreen.remote_exception import RemoteException
from sqreen.instrumentation import Instrumentation
from sqreen.metrics import MetricsStore
import sqreen.rules_callbacks


RUNNER_THREAD = None

# Graceful timeout, max time waiting for the runner thread to exit before exiting
GRACEFUL_TIMEOUT = 4
GRACEFUL_FAIL_MSG = "Sqreen thread didn't exit after %s seconds"

LOGGER = getLogger(__name__)


# Exit mechanism
def sqreen_exit(runner, queue):
    queue.put(RunnerStop)

    try:
        runner.join(GRACEFUL_TIMEOUT)
    except RuntimeError:
        logger = getLogger(__name__)
        logger.warning(GRACEFUL_FAIL_MSG, GRACEFUL_TIMEOUT)
    else:
        if runner.isAlive():
            logger = getLogger(__name__)
            logger.warning(GRACEFUL_FAIL_MSG, GRACEFUL_TIMEOUT)


def before_hook_point():
    global RUNNER_THREAD
    if RUNNER_THREAD.is_alive() is False:
        runner = RunnerThread()
        runner.queue = RUNNER_THREAD.queue
        runner.observations_queue = RUNNER_THREAD.observations_queue
        runner.instrumentation = RUNNER_THREAD.instrumentation
        runner.start()

        atexit.register(sqreen_exit, runner=runner, queue=runner.queue)
        RUNNER_THREAD = runner


def _dump_thread_stacks():
    """ Try to dump all the currently running thread stacks
    """
    try:
        msg = ["Threads stacks \n"]
        thread_name_map = {thread.ident: thread.name for thread in threading.enumerate()}

        for thread_id, stack in sys._current_frames().items():
            msg.append("# Thread: id '%r', name %r" % (thread_id, thread_name_map[thread_id]))
            msg.append("".join(traceback.format_stack(stack)))

        LOGGER.debug("\n".join(msg))
    except Exception:
        LOGGER.exception("Something happened")


def start():
    """ Start the background thread and start protection
    """
    # Check if the agent is not disabled first
    try:
        disabled = int(os.getenv('SQREEN_DISABLE', 0))
    except ValueError:
        disabled = None

    if disabled:
        LOGGER.critical('Sqreen agent is disabled.')
        return

    global RUNNER_THREAD

    try:
        runner = RunnerThread()
        runner.start()

        atexit.register(sqreen_exit, runner=runner, queue=runner.queue)

        timeout = runner.instrumentation_done.wait(10)

        if timeout is not True:
            msg = "Sqreen couldn't start. Check network connectivity: http://status.sqreen.io/"
            LOGGER.critical(msg)

            # Also dump the stacktraces of all running threads
            _dump_thread_stacks()
        else:
            if runner.isAlive():
                LOGGER.info("Sqreen instrumentation started successfully")
    except Exception:
        LOGGER.critical("Sqreen thread fails to start, you're not protected",
                        exc_info=True)
        return

    RUNNER_THREAD = runner

    return runner


class RunnerThread(Thread):
    """ Class responsible for starting the runner and monitor it
    """

    name = "SqreenRunnerThread"

    def __init__(self):
        super(RunnerThread, self).__init__()
        self.daemon = True
        self.logger = getLogger(__name__)
        self.queue = CappedQueue(MAX_QUEUE_LENGTH)
        self.observations_queue = CappedQueue(MAX_OBS_QUEUE_LENGTH)
        self.instrumentation_done = Event()
        self.runtime_infos = RuntimeInfos().all()
        self.instrumentation = Instrumentation(self.queue.put, before_hook_point)

    def run(self):
        """ Launch the runner
        """
        self.logger.debug('Starting Sqreen %s', sqreen.__version__)
        # FIXME this part should be more tested
        while True:
            session = None
            runner = None

            try:
                # Instantiate configuration
                config = Config()
                config.load()

                try:
                    token = config['TOKEN']
                except KeyError:
                    msg = ("Sorry but we couldn't find your Sqreen token.\n"
                           "Your application is NOT currently protected by Sqreen.\n"
                           "\n"
                           "Have you filled your sqreen.ini?")
                    self.logger.critical(msg)
                    self.instrumentation_done.set()
                    return

                self.logger.warning("Using token %s", token)

                # Connection
                url = config['URL']
                self.logger.warning("Connection to %s", url)

                con = Urllib3Connection(url)

                session = Session(con, token)

                try:
                    session.login(self.runtime_infos)
                except InvalidToken:
                    msg = ("Sorry but your Sqreen token appears to be invalid.\n"
                           "Your application is NOT currently protected by Sqreen.\n"
                           "\n"
                           "Please check the token against the interface")
                    self.logger.critical(msg)
                    self.instrumentation_done.set()
                    return

                self.logger.info("Login success")

                deliverer = SimpleDeliverer(session)
                remote_command = RemoteCommand.with_production_commands()
                metrics_store = MetricsStore()
                metrics_store.register_production_aggregators()

                runner = Runner(self.queue, self.observations_queue, session,
                                deliverer, remote_command, self.instrumentation,
                                metrics_store)
                runner.do_heartbeat()
                self.instrumentation_done.set()
                runner.run()
                # If the runner exit, returns
                return
            except Exception:
                self.logger.exception("An unknown exception occured")

                if session is not None and session.is_connected():
                    try:
                        session.post_sqreen_exception(RemoteException(sys.exc_info()).to_dict())
                        session.logout()
                    except Exception:
                        self.logger.exception("Exception while logout")
                        return

                try:
                    self.instrumentation.deinstrument_all()
                except Exception:
                    # We did not managed to remove instrumentation, state is unclear:
                    # terminate thread
                    self.logger.exception("Exception while trying to clean-up")
                    return

                delay = randint(0, 10)
                self.logger.debug("Sleeping %s seconds before retry", delay)
                time.sleep(delay)
