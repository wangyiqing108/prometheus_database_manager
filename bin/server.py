import json
import datetime
import os.path
import shutil
import logging

import yaml
import requests
from flask import Flask
from flask import request

from config import config
from views import generate_supervisor_conf
from utils import get_free_tcp_port, reverse_name, run_cmd

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/v1/monitor", methods=["POST"])
def create_monitor():
    """
    创建Prometheus监控
    :return:
    """
    data = request.get_json()
    logger.info(json.dumps(data))
    project_name = data.get("project_name")  # 项目名称
    db_address = data.get("db_address")  # 数据库的链接地址
    db_type = data.get("db_type")  # 数据库类型, mysql, redis, mongodb
    service_port = get_free_tcp_port()

    if not all([project_name, db_address, db_type]):
        return json.dumps({"status_code": 404, "data": "参数缺失!"}, ensure_ascii=False)

    # 请求抓取数据库agent接口
    req = requests.post(url=config.DB_AGENT_API, json=data, timeout=10)
    result = req.json()
    if result["status_code"] == 200:
        scraped_port = result["data"]["port"]
    else:
        logger.warning(json.dumps(result))
        return json.dumps(result)

    # 参数处理, 业务监控相关配置
    reversed_name = "{0}_{1}".format(reverse_name(project_name), service_port)
    # 该项目对应的Prometheus程序所在目录
    prom_path = os.path.join(config.PROM_BASE_DIR, reversed_name)
    # 该项目对应的supervisor配置文件的路径
    super_path = os.path.join(config.SUPERVISOR_BASE_DIR, reversed_name + ".ini")

    # 判断目标目录是否存在, 存在的话mv到临时文件夹中
    if os.path.exists(prom_path):
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        old_dirpath = os.path.join(config.TMP_DIR, reversed_name + ts)
        shutil.move(prom_path, old_dirpath)

    # 拷贝Prometheus模板目录
    shutil.copytree(config.PROM_TEMPLATE_DIR, prom_path)

    # 初始化服务监控配置文件
    prom_template_path = os.path.join(config.PROM_TEMPLATE_DIR, "prometheus.yml")
    prom_template_obj = yaml.load(open(prom_template_path))
    targets = ["{0}:{1}".format(config.DB_AGENT_IP, scraped_port)]
    # obj["scrape_configs"][0]
    # {'job_name': 'prometheus', 'metrics_path': '/metrics', 'static_configs': [{'targets': ['localhost:9090']}]}
    prom_template_obj["scrape_configs"][0]["metrics_path"] = "/metrics"
    prom_template_obj["scrape_configs"][0]["job_name"] = project_name
    prom_template_obj["scrape_configs"][0]["static_configs"][0]["targets"] = targets
    prom_conf_obj = open(os.path.join(prom_path, "prometheus.yml"), 'w')
    yaml.dump(prom_template_obj, prom_conf_obj)

    # 生成supervisor配置文件
    generate_supervisor_conf(reversed_name, service_port, prom_path, super_path)

    # 更新supervisor进程, 让新加入的配置生效
    try:
        cmd = "/usr/bin/supervisorctl update"
        run_cmd(cmd)
    except Exception as e:
        logger.error(e)
        logger.warning("更新supervisor出错, 请手工更新supervisor!")
        return json.dumps({"status_code": 503, "data": "监控添加成功, 但supervisor更新失败!"}, ensure_ascii=False)

    return json.dumps({"status_code": 200, "data": "{0}:{1}".format(config.DB_DS_PREFIX, service_port)}, ensure_ascii=False)
