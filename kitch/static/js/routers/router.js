( function() {	
	Kitch.Workspace = Backbone.Router.extend({
		routes: {
			'': 'home'
		},

		home: function(){
			
		}
	});

	new Kitch.Workspace();
	Backbone.history.start();
})();