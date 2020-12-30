from flask import Blueprint

"""
   转换yapi类型为java类型
"""
def  typeToDonetType(ytype):
    if(ytype=="string" or ytype=="text"):
        return "String"
    if (ytype == "integer"):
        return "Int32"
    if (ytype == "number"):
        return "Double"
    if (ytype == "boolean"):
        return "Boolean"
    return None

def initDonetFilter(app):
    app.add_template_filter(typeToDonetType, 'typeToDonetType')
