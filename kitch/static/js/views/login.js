var app = app || {};

( function(){
	app.LoginView = Backbone.View.extend({
		el: $("#login_container"),

		initialize: function(){
			this.render();
			this.username = $("#username");
    		this.password = $("#password");
    		
		},

		render: function(){			
			var template = _.template( $("#sample_template").html(),{});
			this.$el.html( template );

			return this;
		},

		events: {
			"click input[type=button]" : "login",
			"change #username": "setUsername",
    		"change #password": "setPassword"
		},

		setUsername: function(e){
			this.model.set({username: this.username.val()});			
  		},
		 
		setPassword: function(e){
		  this.model.set({password: this.password.val()});
		},

		login: function(event){
			var user= this.model.get('username');
    		var password = this.model.get('password');
    		this.model.save(null,
				{
				success: function(model, response) {
				
				},
				error: function() {
					alert('Unable to authenticate');
				}});
		}
});
})();
	