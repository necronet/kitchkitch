var app = app || {};

( function() {
	
	var Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'/login/': 'login'

		},

		home: function(){
			console.log('home')
		},

		login: function(){
			console.log('login')
		}
	});

	app.Router = new Workspace();

	Backbone.history.start();

})();