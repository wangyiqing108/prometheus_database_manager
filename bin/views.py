import os


def generate_supervisor_conf(reversed_name, server_port, prom_path, super_path):
    """
    生成supervisor配置文件
    :param reversed_name: 项目名称(转化后的)
    :param server_port: 服务端要监听的端口
    :param prom_path: 每个项目对应的Prometheus的程序所在路径
    :param super_path: 每个相对应的supervisor的配置文件路径
    :return:
    """

    template = '''
[program:{0}]
command=/usr/local/bin/prometheus --config.file prometheus.yml --web.listen-address=":{1}" --storage.tsdb.retention=7d
directory={2}
stopsignal=HUP
autostart = true
autorestart = true
redirect_stderr = true
stdout_logfile=/data/log/{0}_stdout.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=1
stderr_logfile=/data/log/{0}_stderr.log
stderr_logfile_maxbytes=50MB
stderr_logfile_backups=1'''.format(reversed_name, server_port, prom_path)

    with open(super_path, "w") as f:
        f.write(template)





