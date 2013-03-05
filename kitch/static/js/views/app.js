
(function(){
	app.AppView = Backbone.View.extend({
		el: "#feed_app",

		appTemplate: _.template($("#app-template").html()),

		initialize: function(){
			//loginView = new app.LoginView({model: new app.Login()});
		}


	});

})();