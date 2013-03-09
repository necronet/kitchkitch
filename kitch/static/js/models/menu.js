( function(){

	Kitch.Models.Menu = Backbone.Model.extend({

		defaults:{
			items: []
		},
		validate: function(attrs, options){
			if(attrs.title == undefined) {
				return 'Title must be defined';
			}
		}
	});

	Kitch.Models.MenuItem = Backbone.Model.extend({

		defaults:{
			addon: false
		},
		validate: function(attrs, options){
			if(attrs.title == undefined) {
				return 'Title must be defined';
			}

			if (attrs.description == undefined) {
				return 'Description must be defined';
			}
			
			if (attrs.price == undefined) {
				return 'Price must be defined';
			}	
		}
	});

})();