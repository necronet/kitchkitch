from flask.views import MethodView
from flask import request

class KitchObject(object):
    def __init__(self, obj):
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, KitchObject(v))
            else:
                setattr(self, k, v)


class BaseService(MethodView):
    def get(self,id):
        self.offset= int(self.get_parameter('offset'))
        self.limit= int(self.get_parameter('limit',50))
        self.expand=request.args.get('expand')



    def get_parameter(self, param_name, default_value=0):
        parameter=request.args.get(param_name)

        return default_value if parameter is None or type(parameter)!=type(default_value) else parameter


    def expand_arguments(self):
        """
        Will check the expand attribute is present and try to get the attributes
        from the expand parameter. i.e

        The following expression:

            http://foo/?expand=item,user

        Should return a list: [item,user]

        """
        if self.expand is None:
            return None

        expand_arguments=[]
        for attribute in self.expand.split(','):
            expand_arguments.append(attribute)

        return expand_arguments



