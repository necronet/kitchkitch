var app = app || {};

( function() {
	
	var Workspace = Backbone.Router.extend({
		routes: {
			'': 'home'
		},

		home: function(){
			
		}
	});

	app.Router = new Workspace();

	Backbone.history.start();

})();