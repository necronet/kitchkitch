( function() {	
	Kitch.Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'logout':'logout',
			'account':'account',
			'menu':'menu',
			'dashboard':'home',
			'order':'order',
			'table':'table'
		},
		menu: function(){
			Kitch.Views.App.render(new Kitch.Views.MenuList());
		},
		account: function(){
			Kitch.Views.App.render(new Kitch.Views.Account());
		},
		order: function(){
			Kitch.Views.App.render(new Kitch.Views.Order());
		},
		table: function(){
			Kitch.Views.App.render(new Kitch.Views.Table());
		},
		home: function(){
			//TODO: do a dashboard view
			Kitch.Views.App.render(new Kitch.Views.MenuList());
		}
	});

	new Kitch.Workspace();
	Backbone.history.start();
})();