
(function(){
	app.AppView = Backbone.View.extend({
		el: "#app-container",

		initialize: function(){
			this.render();
		},
		render: function(){
			menuListView = new app.MenuListView();

			this.$el.append(menuListView.el);
		}


	});

})();