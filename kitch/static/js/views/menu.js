var app = app || {};

( function(){
	
	app.MenuList = Backbone.Collection.extend({
		model: app.Menu,
		url: '/menus',
		parse: function(resp, xhr) {
        	return resp.items;
    	}	
	})

	

	app.MenuListView = Backbone.View.extend({
		
		template: _.template($('#menu-template').html()),

		initialize: function(){
			this.menuList = new app.MenuList();
			_.bindAll(this, 'render');
			this.menuList.on('reset', this.render, this);
			this.menuList.fetch( { data: {expand:'items'} } )
		},

		render: function(){
			this.$el.empty(); 
	        var self = this; 
			
		  	this.menuList.each(function(menu) { // iterate through the collection
		  		var menuView = new app.MenuView({model: menu}); 
		    	self.$el.append(menuView.el);
		  	});

	        return this;
		}
	});


	app.MenuView = Backbone.View.extend({

		initialize: function(){
			this.render();
		},

		render: function(){

			var template = _.template($('#menu-item-template').html(), this.model.toJSON());

			this.$el.html( template );

		}
	});

})();
	