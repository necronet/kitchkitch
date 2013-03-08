( function(){
	
	Kitch.Collections.MenuList = Backbone.Collection.extend({
		model: Kitch.Models.Menu,
		url: '/menus',
		parse: function(resp, xhr) {
        	return resp.items;
    	}	
	})

	

	Kitch.Views.MenuList = Backbone.View.extend({
		
		template: _.template($('#menu-template').html()),

		initialize: function(){
			this.menuList = new Kitch.Collections.MenuList();
			_.bindAll(this, 'render');
			this.menuList.on('reset', this.render, this);
			this.menuList.fetch( { data: {expand:'items'} } )
		},

		render: function(){
			this.$el.empty(); 
	        var self = this; 
			
		  	this.menuList.each(function(menu) { // iterate through the collection
		  		var menuView = new Kitch.Views.Menu({model: menu}); 
		    	self.$el.append(menuView.el);
		  	});

	        return this;
		}
	});


	Kitch.Views.Menu = Backbone.View.extend({

		events:{
			'click .add-item': 'add'
		},

		add: function(){
			console.log('add new item');
		},

		initialize: function(){
			this.render();
		},

		render: function(){

			var template = _.template($('#menu-item-template').html(), this.model.toJSON());

			this.$el.html( template );

		}
	});

})();
	