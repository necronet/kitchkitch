
(function(){
	Kitch.Views.App = Backbone.View.extend({
		el: "#container",
		

		initialize: function(){
			
		},
		render: function(view){
			this.$el.html(view.el);
			this.currentView = view;

			return this;

		}


	});

	//General application View
	Kitch.Views.App = new Kitch.Views.App();

})();