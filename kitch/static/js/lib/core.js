var Kitch = Kitch || {
	Views: {},
	Router: {},
	Models:{},
	Collections:{}
};

var template = function(id, model){
	return _.template($('#'+id).html(), model);
}
