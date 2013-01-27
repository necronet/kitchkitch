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
        

    def get_parameter(self, param_name, default_value=0):
        parameter=request.args.get(param_name)
        
        return default_value if parameter is None or type(parameter)!=type(default_value) else parameter
