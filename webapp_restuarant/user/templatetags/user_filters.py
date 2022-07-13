from django import template


register = template.Library()


@register.filter(name="AddAttr")
def AddAttr(value, arg):
    """[summary]
    class:video-form,placeholder:salam
    Args:
        value ([type]): [description]
        arg ([type]): [description]

    Returns:
        [type]: [description]
    """
    lis = arg.split(",")
    dic = {}
    for i in lis:
        att = i.split(":")
        dic[att[0]] = att[1]

    return value.as_widget(attrs=dic)
