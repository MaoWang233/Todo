    (function ($) {

        // define model
        // ---------------
        var todo = Backbone.Model.extend({

            defaults:{
                title: "empty todo",
                completed : false,
            },

            toggle: function() {
                this.save({completed: !this.get("completed")});
            },
        });


        // define collection
        // ---------------
        var todoslist = Backbone.Collection.extend({
            model: todo,
            url: '/todos/',

            // reutrn completed todos
            completed: function() {
                return this.where({completed: true});
            },

            // return uncompleted todos
            uncompleted: function() {
                return this.where({completed: false});
            },

        });

        var todos = new todoslist;



        // define single model view
        // ---------------
        var itemview = Backbone.View.extend({

            tagName: "li",

            // use usderscore template
            template: _.template($('#item-template').html()),

            initialize: function() {
                this.listenTo(this.model, "destroy", this.remove);
                this.listenTo(this.model, "change", this.render);
            },

            events: {
                "click a.destroy": "clear",
                "dblclick .view": "edit",
                "blur .edit": "close",
                "keypress .edit": "updateOnEnter",
                "click .toggle": "complete",
            },

            render: function() {
                this.$el.html(this.template(this.model.toJSON()));
                this.$el.toggleClass('completed', this.model.get('completed'));
                // why put here not in the initialize???
                this.input = this.$(".edit");
                return this;
            },

            // destory a model from collection
            clear: function() {
                this.model.destroy();
            },

            // edit the tile of the model
            edit: function() {
                this.$el.addClass("editing");
                this.input.focus();
            },

            updateOnEnter: function(e) {
                if (e.keyCode === 13) this.close();
            },

            // save the data and return to hte view mode
            close: function() {
                var value = this.input.val();
                if (!value) {
                    this.clear();
                } else {
                    this.model.save({title: value});
                    this.$el.removeClass("editing");
                }
            },

            // mark the todo-item completed and render the todo-item
            complete: function() {
                this.model.toggle();
            },

        });



        // define list view 
        // ---------------
        var listview = Backbone.View.extend({
            el: $('body'),

            initialize: function() {
                this.listenTo(todos, "add", this.addOneTodo);
                this.listenTo(todos, "all", this.render);
                this.checkall = $("#toggle-all")[0];
                this.input = $("#content");
                this.section = $("section");
                this.footer = $("footer");
                todos.fetch();
            },

            stausTemplate: _.template($('#list-template').html()),

            
            // update the status and todoitem
            render: function() {
                var completed = todos.completed().length;
                var uncompleted = todos.uncompleted().length;
                if (todos.length){
                    this.section.show();
                    this.footer.show();
                    $("footer").html(this.stausTemplate({completed: completed, uncompleted: uncompleted}));
                } else {
                    this.section.hide();
                    this.footer.hide();
                }
                this.checkall.checked = !uncompleted;
                // this.checkall.attr("checked", !uncompleted); why didn't work???
            },

            events: {
                "keypress #content" : "createOnEnter",
                "click #clear-completed " : "clearCompleted",
                "click #toggle-all" : "markAllCompleted"
            },

            // create one model add into collection and trigger the "add" event
            createOnEnter: function(e) {
                // id don't hit Enter or no content return nothing
                if(e.keyCode != 13) return;
                if(!this.input.val()) return;

                todos.create({title: this.input.val()});
                this.input.val('');
            },

            // add the view to the html
            addOneTodo: function(todo) {
                var view = new itemview({model: todo});
                $("#todo-list").append(view.render().el);
            },

            // clear all completed item
            clearCompleted : function() {
                // usderscore method invoke use menthod in collection
                _.invoke(todos.completed(), "destroy");
            },

            // toggle all the todoitem's complete status
            markAllCompleted : function() {
                var completed =  this.checkall.checked;
                todos.each(function (todo) { todo.save({"completed": completed}); });
            },

        });
    
        var view = new listview;

        })(jQuery);