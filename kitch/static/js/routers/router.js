( function() {	
	Kitch.Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'logout':'logout'
		},

		home: function(){
			
		}
	});

	new Kitch.Workspace();
	Backbone.history.start();
})();