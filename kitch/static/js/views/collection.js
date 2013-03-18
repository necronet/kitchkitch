( function(){
	
	Kitch.Collections.Menu = Backbone.Collection.extend({
		model: Kitch.Models.Menu,
		url: '/menus/',
		parse: function(resp, xhr) {
        	return resp.items;
    	}	
	});	

	Kitch.Collections.MenuItem = Backbone.Collection.extend({
		model: Kitch.Models.MenuItem,
		url: '/menuItems/'
	});
	
})();