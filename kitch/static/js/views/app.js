
(function(){
	Kitch.Views.App = Backbone.View.extend({
		el: "#app-container",

		initialize: function(){
			this.render();
		},
		render: function(){
			menuListView = new Kitch.Views.MenuList();

			this.$el.append(menuListView.el);
		}


	});

})();