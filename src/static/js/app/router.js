(function($,log,_,Backbone,GlobalView,IndexView){

	window.Router = window.Backbone.Router.extend
	({

		dispatcher: _.extend({}, Backbone.Events),

		routes:
		{
			"": "index_page",
		},

		initialize: function()
		{
			this.global_view = new GlobalView();
		},

		// views

		index_page: function()
		{
			this.index_view = new IndexView();
		},
	});

}(jQuery,window.log,window._,window.Backbone,window.GlobalView,window.IndexView));