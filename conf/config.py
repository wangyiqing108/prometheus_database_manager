import os


class Config(object):
    # 服务监听端口
    PORT = 8888
    TIMEOUT = 10

    # supervisor配置文件路径
    SUPERVISOR_BASE_DIR = "/etc/supervisord.d"

    # 数据库agent API地址
    DB_AGENT_API = "http://192.168.209.25:8888/v1/monitor"
    DB_AGENT_IP = "192.168.209.25"
    DB_DS_PREFIX = "http://192.168.112.233"

    # Prometheus相关配置
    PROM_TEMPLATE_DIR = "/data/software/base"
    PROM_BASE_DIR = "/data/apps"
    PROM_DEFAULT_SERVICE_PORT = 9091
    PROM_DEFAULT_BASE_PORT = 9100

    # 临时文件存放路径
    TMP_DIR = "/data/tmp"

    # 日志文件路径
    LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log", "app.log")


class ProductionConfig(Config):
    # 日志配置
    DEBUG = False
    LOG_LEVEL = "INFO"

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


config = ProductionConfig
# config = DevelopmentConfig

