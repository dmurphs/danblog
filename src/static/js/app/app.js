(function($,log,_,Backbone){

	$(function(){
		window.router    = new window.Router();
		Backbone.history.start({pushState:false, hashChange:false});
	});

}(jQuery,window.log,window._,window.Backbone));