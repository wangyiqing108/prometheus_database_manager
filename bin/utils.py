import logging
import socket
import subprocess
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from config import config




def create_logger():
    logger = logging.getLogger()

    formatter = logging.Formatter(
        fmt="%(levelname)s|%(asctime)s|%(process)d|%(thread)d|%(filename)s:%(lineno)s|%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    stream_handler = StreamHandler()
    file_handler = TimedRotatingFileHandler(filename=config.LOG_FILE_PATH, when='D', backupCount=3)

    if config.DEBUG:
        handlers = [stream_handler]
    else:
        handlers = [stream_handler, file_handler]

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(config.LOG_LEVEL)


def reverse_name(name):
    """
    项目名称处理, 项目中的所有短横杠全部转换成下划线
    :param name: 项目名称
    :return:
    """
    return name.replace("-", "_")


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def run_cmd(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait(timeout=30)
        out = p.stdout.read()  # type: str
        err = p.stderr.read()  # type: str
        return p.returncode, out, err
    except:
        raise
    finally:
        p.kill()  # The child process is not killed if the timeout expires
