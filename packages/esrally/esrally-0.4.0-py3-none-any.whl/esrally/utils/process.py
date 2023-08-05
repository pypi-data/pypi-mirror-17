import shlex
import logging
import subprocess
import os
import psutil

logger = logging.getLogger("rally.process")


def run_subprocess(command_line):
    return os.system(command_line)


def run_subprocess_with_output(command_line):
    return os.popen(command_line).readlines()


def run_subprocess_with_logging(command_line, header=None):
    """
    Runs the provided command line in a subprocess. All output will be captured by a logger.

    :param command_line: The command line of the subprocess to launch.
    :param header: An optional header line that should be logged (on info level)
    :return: True iff the subprocess has terminated successfully.
    """
    command_line_args = shlex.split(command_line)
    if header is not None:
        logger.info(header)
    logger.debug("Invoking subprocess '%s'" % command_line)
    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        has_output = True
        while has_output:
            line = command_line_process.stdout.readline()
            if line:
                logger.info(line)
            else:
                has_output = False
    except OSError as exception:
        logger.warn("Exception occurred when running '%s': '%s'" % (command_line, str(exception)))
        return False
    else:
        logger.debug("Subprocess '%s' finished" % command_line)

    return True


def kill_running_es_instances(node_prefix):
    """
    Kills all instances of Elasticsearch that are currently running on the local machine by sending SIGKILL.

    :param node_prefix a prefix of the node names that should be killed.
    """
    logger.info("Killing all processes which match [java], [elasticsearch] and [%s]" % node_prefix)
    for p in psutil.process_iter():
        try:
            if p.name() == "java" and any("elasticsearch" in e for e in p.cmdline()) and any("node.name=rally" in e for e in p.cmdline()):
                # check if command line contains elasticsearch and rally
                logger.info("Killing lingering ES benchmark instance with PID [%s] and command line [%s]." % (p.pid, p.cmdline()))
                p.kill()
            else:
                logger.debug("Skipping [%s]" % p.cmdline())
        except (psutil.ZombieProcess, psutil.AccessDenied):
            pass
