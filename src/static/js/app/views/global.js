(function($,log,_,Backbone,NavView){
    
    window.GlobalView = Backbone.View.extend({

        el: '',

        events:
        {
        },

        initialize: function()
        {
            this.nav_view = new NavView({el: $(this.el).find('#hd')});

        }



    });

}(jQuery,window.log,window._,window.Backbone,window.NavView));