( function(){
	
	Kitch.Collections.Menu = Backbone.Collection.extend({
		model: Kitch.Models.Menu,
		url: '/menus',
		parse: function(resp, xhr) {
        	return resp.items;
    	}	
	});	

	Kitch.Collections.MenuItem = Backbone.Collection.extend({
		model: Kitch.Models.MenuItem,
		url: '/menuItems/'
	});

	Kitch.Views.MenuList = Backbone.View.extend({		


		initialize: function(){
			this.collection = new Kitch.Collections.Menu();			
			this.collection.on('reset', this.render, this);
			this.collection.on('add', this.addMenu, this);
			this.collection.fetch( { data: {expand:'items'} } )

		},

		render: function(){
			this.$el.empty(); 
	        
	        this.$el.html( template('menu-add'));

	        this.collection.each(this.addMenu, this);

	        return this;
		},

		events: {
			'submit form[id=add-menu ]': 'add'
		},

		add: function(e){
			e.preventDefault();
			title = $(e.currentTarget).find('input[name=title]').val();
			
			if(title){
				menu = new Kitch.Models.Menu({title: title});
				this.collection.add(menu);
				
			}else{
				alert('something wrong');
			}
		},
		
		addMenu:function(menu) { 
		  		var menuView = new Kitch.Views.Menu({model: menu}); 
		    	this.$el.append(menuView.render().el);
		 }

	});


	Kitch.Views.Menu = Backbone.View.extend({

		initialize: function(){
			
		},		

		render: function(){
			this.$el.html( template('menu', this.model.toJSON()) );
			itemList = new Kitch.Views.MenuListItem( { collection : this.model.get("items") });
			this.$el.html( template('menu', this.model.toJSON()) );
			this.$el.append( itemList.render().el );

			return this;
		}
	});

	Kitch.Views.MenuListItem = Backbone.View.extend({


		initialize: function(){
			
			this.collection = new Kitch.Collections.MenuItem(this.collection);
			this.collection.on('add', this.addMenuItem, this);
		
		},

		render: function(){			
			this.$el.empty();	
			this.$el.append( template('item-add') );
			if(this.collection.length > 0) {
				this.collection.each(this.addMenuItem, this);
			}
			
	        return this;
		},

		addMenuItem: function(item){
				
			var menuItemView = new Kitch.Views.MenuItem({model: item}); 
			
			this.$el.find('#add-form').before(menuItemView.render().el);

		},

		events:{
			'submit form[id=add-form]': 'add'
		},

		add: function(e){
			e.preventDefault();
			title = $(e.currentTarget).find('input[name=title]').val();
			description = $(e.currentTarget).find('input[name=description]').val();
			price = $(e.currentTarget).find('input[name=price]').val();

			if (price && description && price ){
				menuItem = new Kitch.Models.MenuItem( {
					title: title,
					price: price,
					description: description
				} );

				this.collection.add(menuItem);
			}else{
				console.log('validation here');
			}

		},
	});

	Kitch.Views.MenuItem = Backbone.View.extend({

		tagName:'li',

		initialize: function(){
			this.model.on('destroy', this.remove, this);
			this.model.on('change', this.render, this);

		},
		render: function(){
			
			this.$el.html(template('menu-item', this.model.toJSON()));

			return this;
		},

		events:{
			'click button[name=delete]': 'delete',
			'dblclick span': 'edit',
			'submit form[id=edit-form]': 'finishEdit'
		},

		finishEdit: function(e){
			e.preventDefault();
			
			title = $(e.currentTarget).find('input[name=title]').val();
			description = $(e.currentTarget).find('input[name=description]').val();
			price = $(e.currentTarget).find('input[name=price]').val();

			this.model.set("title", title);
			this.model.set("description", description);
			this.model.set("price", price);
			console.log('uid: '+this.model.isNew());
			this.model.save();

			this.$el.removeClass('editing');
		},

		edit: function(e){
			this.$el.addClass('editing');
		},

		remove: function(e){
			this.$el.remove();
		},

		delete: function(e){
			this.model.destroy();
		}


	});


})();
	