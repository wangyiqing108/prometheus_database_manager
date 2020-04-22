#### 接口说明

`创建数据库监控`

给某个项目下的数据库新增Prometheus监控, 该接口会同时自动创建数据库agent的配置.

###### 接口地址

`http://192.168.112.233:8888/v1/monitor`

###### 请求方式

`POST`

###### 请求参数

```
{
	"project_name": "mp-sre-platform",
	"db_address": "rm-2ze335le341qorhly.mysql.rds.aliyuncs.com",
	"db_type": "mysql", # 数据库类型, 可以是mysql, redis, mongodb
	"db_password": "" # redis 需要
}
```

###### 返回示例

```
{
    "status_code": 200,
    "data": "http://192.168.112.233:51119"
}
```

---