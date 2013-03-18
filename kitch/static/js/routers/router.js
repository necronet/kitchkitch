( function() {	
	Kitch.Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'logout':'logout',
			'account':'account',
			'menu':'menu'
		},
		menu: function(){
			console.log('menu');
			Kitch.Views.App.render(new Kitch.Views.MenuList());
		},
		account: function(){
			Kitch.Views.App.render(new Kitch.Views.Account());
		},

		home: function(){
			Kitch.Views.App.render(new Kitch.Views.MenuList());
		}
	});

	new Kitch.Workspace();
	Backbone.history.start();
})();