import json


def fun_lstrip(value,trimStr):
    return value.lstrip(trimStr)
def fun_index(value,indexStr):
    return value.find(indexStr)
def fun_substr(value,start,end=None):
    if(end is not None):
        return value[start:end]
    return value[start:]
def fun_split(value,splitStr):
    return value.split(splitStr)
def fun_jsonParse(value):
    if(value is not None and value!=""):
        return json.loads(value)
    return None;
def fun_json(dict,key,value):
    dict[key]=value;
    return True;
def fun_boolToInt(boolStr):
    if boolStr and boolStr!="":
        if "1"==boolStr:
            return True
    return False;
def fun_btos(boolStr):
    return str(boolStr)
def fun_dict(dict,*keys):
    for v in range(0,len(keys)):
        if keys[v] in dict:
            return dict[keys[v]]
    return "";
def fun_firstLower(str):
    return str[0:1].lower()+str[1:];
def initCommonFilter(app):
    app.add_template_filter(fun_lstrip, 'lstrip')
    app.add_template_filter(fun_substr, 'substr')
    app.add_template_filter(fun_index, 'index')
    app.add_template_filter(fun_jsonParse, 'jsonParse')
    app.add_template_filter(fun_split, 'split')
    app.add_template_filter(fun_json, 'json')
    app.add_template_filter(fun_boolToInt, 'boolToInt')
    app.add_template_filter(fun_btos, 'btos')
    app.add_template_filter(fun_dict, 'dict')
    app.add_template_filter(fun_firstLower, 'firstLower')