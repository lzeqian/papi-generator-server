import json
import os
import shutil
import urllib
import uuid
import zipfile

import yaml
from flask import Flask, after_this_request, Response, request, render_template, render_template_string

from filter.template.common import initCommonFilter
from filter.template.java import initJavaFilter

app = Flask(__name__)
"""
    获取项目yaml文件数据（默认缓存时间10s）,全部改造完成后调大缓存时间
    参考：https://hellosean1025.github.io/yapi/openapi.html
    {
        "templateGroupName":java
        "catDescription":"Function"
        "package":""
        interfaceList:[
           {
                _id: 接口id
                title: 接口名称
                path: /a/b
                method：请求类型

           }，
        ]
    }
"""


def renderTemplateData(jsonData):
    configContent = None;
    # 模板组，如java，donet
    templateGroupName = jsonData["templateGroupName"]
    # 分类名称，生成具体的模板名称的拼接
    catDescription = jsonData["catDescription"]
    # 对应生成的包结构
    package = jsonData["package"]
    # 对应生成需要生成的接口列表
    interfaceList = jsonData["interfaceList"]
    dirPath = "templates/" + templateGroupName;
    with open(dirPath + "/config.yaml", encoding="utf-8") as y:
        configContent = yaml.full_load(y.read());
    # 获取需要生成的接口信息
    genernatorList = configContent["genernator"]
    # 获取当前用户目录
    userHome = os.path.expanduser('~')
    # 模板生成文件临时目录:用户目录/.template
    templateDir = userHome + "/.template/"
    # 创建给一个uuid的目录用户压缩
    tmpDirName = str(uuid.uuid4());
    # 生成的临时工作目录，存在生成的代码和亚索包
    curZipDir = templateDir + "/" + tmpDirName
    os.makedirs(curZipDir)
    # zip文件名称
    zipFileName = catDescription + '.zip';
    # 生成zip文件的绝对路径
    zipFilePath = curZipDir + "/" + zipFileName;
    f = zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED);
    for genernator in genernatorList:
        # 模板类型，type表示只生成一个文件，interface表示每个接口生成一个文件，有些接口可能生成为空，此时不需要生成文件
        templateType = genernator["templateType"]
        if "type" == templateType:
            # 获取模板文件名称
            templateFile = render_template_string(genernator["templateFile"], param=jsonData)
            # 获取生成包名称
            generatePackage = render_template_string(genernator["generateDir"], param=jsonData)
            # 获取生成的文件名
            generateName = render_template_string(genernator["generateName"], param=jsonData)
            # 生成对应模板位置
            generateDir = curZipDir + "/" + generatePackage.replace(".", "/")
            os.makedirs(generateDir)
            renderStr = render_template(templateGroupName + "/" + templateFile, param=jsonData)
            print(renderStr)
            fd = os.open(generateDir + "/" + generateName, os.O_RDWR | os.O_CREAT)
            os.write(fd, bytes(renderStr, encoding='utf-8'))
            os.close(fd)
            f.write(generateDir + "/" + generateName, generatePackage.replace(".", "/") + "/" + generateName)
        else:
            interfaceList = jsonData["interfaceList"];
            for ifl in interfaceList:
                # 配置了ifl必须返回了某个参数才需要生成文件
                returnParam = genernator["returnParam"] if "returnParam" in genernator else None;
                ifGen = True;
                if returnParam:
                    for rp in returnParam:
                        if not rp in ifl:
                            ifGen = False;
                if not ifGen:
                    continue
                # 获取模板文件名称
                templateFile = render_template_string(genernator["templateFile"], param=jsonData, interface=ifl)
                # 获取生成包名称
                generatePackage = render_template_string(genernator["generateDir"], param=jsonData, interface=ifl)
                # 获取生成的文件名
                generateName = render_template_string(genernator["generateName"], param=jsonData, interface=ifl)
                # 生成对应模板位置
                generateDir = curZipDir + "/" + generatePackage.replace(".", "/")
                if not os.path.exists(generateDir):
                    os.makedirs(generateDir)
                # 需要生成对应Vo名称
                renderStr = render_template(templateGroupName + "/" + templateFile, param=jsonData, interface=ifl)
                print(renderStr)
                fd = os.open(generateDir + "/" + generateName, os.O_RDWR | os.O_CREAT)
                os.write(fd, bytes(renderStr, encoding='utf-8'))
                os.close(fd)
                f.write(generateDir + "/" + generateName, generatePackage.replace(".", "/") + "/" + generateName)

    f.close()
    return zipFilePath, curZipDir, zipFileName;


"""
 include remote模板生成 https://docs.gitlab.com/ee/ci/yaml/README.html#includeremote
 测试：https://docs.gitlab.com/ee/api/lint.html
"""


@app.route("/template/gen", methods=['POST'])
def ciYamlGen():
    jsonDataStr = request.values.get("jsonData")
    jsonDataStr = urllib.parse.unquote(jsonDataStr)
    print(jsonDataStr)
    jsonData = json.loads(jsonDataStr)
    zipFilePath, curZipDir, zipFileName = renderTemplateData(jsonData)

    @after_this_request
    def cleanup(response):
        return response

    def send_file():
        with open(zipFilePath, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
                if not data:
                    break
                yield data
        shutil.rmtree(curZipDir)

    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % urllib.parse.quote(
        zipFileName)  # 如果不加上这行代码，导致下图的问题
    return response


"""
 include remote模板生成 https://docs.gitlab.com/ee/ci/yaml/README.html#includeremote
 测试：https://docs.gitlab.com/ee/api/lint.html
"""


@app.route("/template/list", methods=['GET'])
def templateList():
    dirPath = "templates/";
    return {"code": 0, "msg": "", "count": 100,
            "data": [name for name in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, name))]}


if __name__ == '__main__':
    # 公共的模板过滤器注入
    initCommonFilter(app)
    initJavaFilter(app)
    app.run(host="0.0.0.0", port=8888, threaded=True)
    app.DEBUG = True
    app.jinja_env.auto_reload = True
