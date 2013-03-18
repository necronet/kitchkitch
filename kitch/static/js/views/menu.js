( function(){
	
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
				self = this;
				menu.save(null, {
					success: function(model, response){
						//add only when success
						self.collection.add(model);
					}

				});
				
				
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
			this.model.on('destroy', this.remove, this);
		},		

		events:{
			'click button[name=delete]':'deleteItem'
		},

		render: function(){
			
			this.$el.html( template('menu', this.model.toJSON()) );
			
			itemList = new Kitch.Views.MenuItemList( { collection : this.model.get("items"), parentId: this.model.get('uid') });
			this.$el.html( template('menu', this.model.toJSON()) );
			this.$el.append( itemList.render().el );

			return this;
		},

		deleteItem: function(e){
			this.model.destroy();
		},

		remove: function(e){

			this.$el.remove();	
		}

	});

	Kitch.Views.MenuItemList = Backbone.View.extend({


		initialize: function(){			
			this.collection = new Kitch.Collections.MenuItem(this.collection);
			this.collection.on('add', this.addMenuItem, this);
		},

		render: function(){			
			this.$el.empty();	
			this.$el.append( template('item-add') );

			if(this.collection.length > 0 && this.collection.at(0).has("description") ) {

				this.collection.each(this.addMenuItem, this);
			}
			
	        return this;
		},

		addMenuItem: function(item){
			
			var menuItemView = new Kitch.Views.MenuItem({model: item, parentId: this.options.parentId}); 
			
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
			addon = $(e.currentTarget).find('input[name=addon]').is(":checked");
			
			if (price && description && price ){
				menuItem = new Kitch.Models.MenuItem( {
					title: title,
					price: price,
					description: description,
					addon: addon
				} );
				menuItem.parentId = this.options.parentId;

				self = this;

				menuItem.save(null, {
					success: function(model, response){
						self.collection.add(model);		
					}
				});
			}else{
				console.log('validation here');
			}

		},
	});

	Kitch.Views.MenuItem = Backbone.View.extend({

		tagName:'li',

		initialize: function(){
			this.model.parentId = this.options.parentId; //specify the menu that it belongs
			this.model.on('destroy', this.remove, this);
			this.model.on('change', this.render, this);

		},
		render: function(){
			
			this.$el.html(template('menu-item', this.model.toJSON()));

			return this;
		},

		events:{
			'click button[name=delete]': 'deleteItem',
			'dblclick span': 'edit',
			'dblclick h2': 'edit',
			'submit form[id=edit-form]': 'finishEdit'
		},

		finishEdit: function(e){
			e.preventDefault();

			title = $(e.currentTarget).find('input[name=title]').val();
			description = $(e.currentTarget).find('input[name=description]').val();
			price = $(e.currentTarget).find('input[name=price]').val();
			addon = $(e.currentTarget).find('input[name=addon]').is(":checked");
			

			this.model.set("title", title);
			this.model.set("description", description);
			this.model.set("price", price);
			this.model.set("addon", addon);

			this.model.save();

			this.$el.removeClass('editing');
		},

		edit: function(e){
			this.$el.addClass('editing');
		},

		remove: function(e){
			this.$el.remove();
		},

		deleteItem: function(e){
			this.model.destroy();
		}


	});


})();
	