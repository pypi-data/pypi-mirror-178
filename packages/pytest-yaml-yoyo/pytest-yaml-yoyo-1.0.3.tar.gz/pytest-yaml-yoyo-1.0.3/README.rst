# 说明

基于 httprunner 框架的用例结构，我自己开发了一个pytest + yaml 的框架，那么是不是重复造轮子呢？
不可否认 httprunner 框架设计非常优秀，但是也有缺点，httprunner3.x的版本虽然也是基于pytest框架设计，结合yaml执行用例，但是会生成一个py文件去执行。
在辅助函数的引用也很局限，只能获取函数的返回值，不能在yaml中对返回值重新二次取值。
那么我的这个框架，就是为了解决这些痛点。。。。

# 环境准备

Python 3.8版本
Pytest 7.2.0 最新版

pip 安装插件

```
pip install pytest-yaml-yoyo
```


# 第一个 hello world

yaml 用例编写规则，跟pytest识别默认规则一样，必须是test 开头的，以`.yml` 结尾的文件才会被识别

新建一个`test_hello.yml`文件

```
config:
  name: yy

teststeps:
-
  name: demo
  print: hello world
```

用例整体结构延续了 httprunner 框架的用例结果，主要是为了大家快速上手，减少新的规则学习
- config  是必须的里面必须有 name 用例名称，base_url 和 variables 是可选的
- teststeps 用例的步骤，用例步骤是一个array 数组类型，可以有多个步骤

从上面的运行可以看出，request 不是必须的，我们可以直接调用python内置函数print 去打印一些内容了。

# 一个简单的 http 请求

以`http://www.example.com/` get 请求示例
test_get_demo.yml

```
config:
  name: get

teststeps:
-
  name: get
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
```

命令行输入 pytest 后直接运行

```
>pytest
======================= test session starts =======================
platform win32 -- Python 3.8.5, pytest-7.2.0, pluggy-1.0.0
rootdir: D:\demo\yaml_yoyo
plugins: yaml-yoyo-1.0.1
collected 2 items

test_get_demo.yml .                                          [ 50%]
test_hello.yml .                                             [100%]

======================== 2 passed in 0.49s ========================

```

# 再来一个post请求

test_post_demo.yml

```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```

# validate校验

比如返回的response内容

```
HTTP/1.1 200 OK
Date: Wed, 23 Nov 2022 06:26:25 GMT
Content-Type: application/json
Content-Length: 483
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {},
  "data": "{\r\n    \"username\": \"test\",\r\n    \"password\": \"123456\"\r\n}",
  "files": {},
  "form": {},
  "headers": {
    "Content-Length": "55",
    "Content-Type": "application/json",
    "Host": "httpbin.org",
    "User-Agent": "Fiddler",
    "X-Amzn-Trace-Id": "Root=1-637dbd11-7d9943ba1fb93a9331f6cf8d"
  },
  "json": {
    "password": "123456",
    "username": "test"
  },
  "origin": "198.187.30.113",
  "url": "http://httpbin.org/post"
}

```

校验方式延续了httprunner的校验语法，可以支持response取值对象：status_code, url, ok, headers, cookies, text, json, encoding
其中返回的是json格式，那么可以支持
- jmespath 取值语法: `body.json.username`
- jsonpath 语法: `$..username`
- re 正则语法

如果返回的不是json格式，那么可以用正则取值

# 变量的声明与引用

变量的声明，只支持在config 声明整个yml文件的全局变量（不支持单个step的变量，减少学习成本）
在 httprunner 里面变量引用语法是`$user`, 引用函数是`${function()}`
我这里统一改成了一个语法变量引用`${var}` 和 引用函数`${function()}`
（表面上没多大变量，实际上功能强大了很多，使用了强大的jinja2 模板引擎)
可以在引用函数后继续对结果操作， 这就解决了很多人提到了函数返回一个list，如何在yaml中取某一个值的问题

```
config:
  name: post示例
  variables:
    username: test
    password: "123456"

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: ${password}
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```
运行结果

![](https://img2022.cnblogs.com/blog/1070438/202211/1070438-20221123143938244-1854561508.png)

# extract 提取接口返回参数关联
在自动化用例中，我们经常会看到有人提问，上一个接口的返回的结果，如何取出来给到下个接口的入参。
我们用 extract 关键字提取接口的返回结果（需要更新v1.0.2版本）。

举个例子
用个post请求`http://httpbin.org/post`
```
POST http://httpbin.org/post HTTP/1.1
User-Agent: Fiddler
Host: httpbin.org
Content-Length: 0

HTTP/1.1 200 OK
Date: Thu, 24 Nov 2022 06:18:03 GMT
Content-Type: application/json
Content-Length: 320
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {},
  "data": "",
  "files": {},
  "form": {},
  "headers": {
    "Content-Length": "0",
    "Host": "httpbin.org",
    "User-Agent": "Fiddler",
    "X-Amzn-Trace-Id": "Root=1-637f0c9a-23b419f4180f6b843ba941af"
  },
  "json": null,
  "origin": "66.112.216.24",
  "url": "http://httpbin.org/post"
}
```
比如我需要提取返回接口里面的url参数，那么我们用extract 关键字

test_demo.yml 文件示例
```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```

# 参数关联

上一个接口提取到了url 变量，接下来在下个接口中引用`${url}`

```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]

-
  name: post
  request:
    method: GET
    url: http://httpbin.org/get
    headers:
      url: ${url}
  validate:
    - eq: [status_code, 200]
```

于是看到请求报文中引用成功
```
GET http://httpbin.org/get HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
url: http://httpbin.org/post

```

# extract 提取结果二次取值

我们在上一篇提到**不能在yaml中对返回值重新二次取值。**,
这也是一些同学提到的问题，对于提取的结果，我想继续取值，比如他是一个字符串，在python中可以用切片取值
那么，在 yaml 中如何实现？

我重新设计的这个框架中，就可以支持python语法，直接用切片取值
```
headers:
      url: ${url[:4]}
```

请求报文
```
GET http://httpbin.org/get HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
url: http

```

**extract 取值语法**

校验方式延续了httprunner的校验语法，可以支持response取值对象：status_code, url, ok, headers, cookies, text, json, encoding
其中返回的是json格式，那么可以支持
- jmespath 语法: body.json.username
- jsonpath 语法: $..username
- re 正则语法：'code: (.+?),'

如果返回的不是json格式，那么可以用正则取值


# 其它功能

目前第一个版本只实现了一些基础功能，还有一些功能待实现。
后续计划：
- 1、全局使用一个 token，仅登录一次，完成全部用例测试
- 2、yaml 中调用 fixture 功能实现
- 3、辅助函数功能使用
- 4、结合 allure 生成报告
- 5、对 yaml 数据格式校验
- 6、添加日志
- 7、新增另外一套yaml用例规范

更多功能持续开发中....大家有好的建议想法也欢迎提出， 微信交流联系wx:283340479

# 版本变更记录

v1.0.0  -- 发布的第一个版本（已删除)
v1.0.1  -- 可以安装的第一个版本
1.实现基础的 pytest 命令 执行yaml 文件用例功能

v1.0.2
1.新增extract 关键字，在接口中提取返回结果
2.参数关联，上一个接口的返回值可以作为下个接口的入参
详细功能参阅 extract 关键字文档

v1.0.3
1.config 新增fixtures 关键字,传 pytest 的fixture参数
2.新增parameters 关键字，实现用例参数化

