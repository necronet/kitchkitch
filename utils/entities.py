class KitchObject(object):
	def __init__(self, obj):
		for k, v in obj.iteritems():
			if isinstance(v, dict):
				setattr(self, k, KitchObject(v))
			else:
				setattr(self, k, v)
