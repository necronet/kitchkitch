from flask.views import MethodView
from flask import request, jsonify, make_response, render_template

def to_json(datas):
    if type(datas)==list:
        return jsonify(items=datas)        
    return jsonify(datas)

encoders={'application/json':to_json,'text/html':render_template}

class KitchObject(object):
    def __init__(self, obj):        
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, KitchObject(v))
            else:
                setattr(self, k, v)


class BaseService(MethodView):
    def get(self,id,template=None):
        self.offset= int(self.get_parameter('offset'))
        self.limit= int(self.get_parameter('limit',50))
        self.expand=request.args.get('expand')
        self.template=template
        

    def get_parameter(self, param_name, default_value=0):
        parameter=request.args.get(param_name)
        return default_value if parameter is None or type(parameter)!=type(default_value) else parameter

    def get_response(self, datas):
        #Will get the best match between supported mimes see encoder_types dictionary
        encoder_key=request.accept_mimetypes.best_match(encoders.keys())
        
        #This is very clever way to mutate, will dinamically return  a function and will pass the proper data
        return encoders[encoder_key](datas)

    def post_response(self):
        return make_response(to_json({'message':'Create succesfully'}),201,{'Location':request.url})

    def put_response(self):
        return make_response(to_json({'message':'Replace succesfully'}),200,{'Location':request.url})

    def delete_response(self):
        return make_response(to_json({ 'message':'Delete succesfully'}), 202)
        

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



