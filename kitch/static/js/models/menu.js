( function(){

	Backbone._sync = Backbone.sync;

	Backbone.sync = function(method, model, options){
		if (method == 'update' ) {
			
			options.url = _.result(model, 'url');
			console.log(_.result(model, 'url'));
		}
		Backbone._sync(method,model, options)
	}

	Kitch.Models.Menu = Backbone.Model.extend({
		idAttribute : "uid",
		urlRoot: '/menus/',
		defaults: {
			items: []
		},

		validate: function(attrs, options) {
			if(attrs.title == undefined) {
				return 'Title must be defined';
			}
		}
	});

	Kitch.Models.MenuItem = Backbone.Model.extend({
		idAttribute: "uid",
		urlRoot: '/menuItems/',

		parentId: null, //reference the menu uid 

		url:  function(){
			
			var base = _.result(this, 'urlRoot') || _.result(this.collection, 'url') || urlError();

			query_parameter = "";
			
			if (this.parentId)
      			query_parameter = "?menus_uid=" + this.parentId;
      		
      		if (this.isNew()) {
      			
      			return base + query_parameter;	
      		} 

      		return base + (base.charAt(base.length - 1) === '/' ? '' : '/') + encodeURIComponent(this.id) + query_parameter;

		},

		defaults:{
			addon: false
		},
		validate: function(attrs, options) {
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