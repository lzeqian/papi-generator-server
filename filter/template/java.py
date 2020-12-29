from flask import Blueprint

"""
   转换yapi类型为java类型
"""
def  typeToJavaType(ytype):
    if(ytype=="string" or ytype=="text"):
        return "String"
    if (ytype == "integer"):
        return "Integer"
    if (ytype == "number"):
        return "Double"
    if (ytype == "boolean"):
        return "Boolean"
    if (ytype == "file"):
        return "MultipartFile"
    return None
"""
  获取请求路径。
  比如传入路径是:/ums/tpauth/supportType,那么生成的注解路径就应该是/tpauth/supportType。
  比如传入路径是:/ums/api/v1/users,比如类注解路径是/api/v1 方法注解路径是/users
"""
def  getRequestPath(path):
    if path:
        requestPath = path.lstrip("/")
        index=requestPath.find("/")
        if(index>-1):
            requestPath = requestPath[index:]
        return requestPath
"""
    获取方法名称
"""
def  getMethodName(requestMethod,requestPath):
    methodName=requestMethod.lower();
    for splitTmp in requestPath.split("/"):
        if splitTmp and splitTmp.startswith("{"):
            methodName = methodName + "By" + (splitTmp.replace("{", "").replace("}", "").capitalize())
        else:
            methodName = methodName + splitTmp.capitalize()
    return methodName

def initJavaFilter(app):
    app.add_template_filter(typeToJavaType, 'typeToJavaType')
    app.add_template_filter(getRequestPath, 'getRequestPath')
    app.add_template_filter(getMethodName, 'getMethodName')
