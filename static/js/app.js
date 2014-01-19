(function($) {
	var Num = Backbone.Model.extend({
		defaults: {fib: null}
	});

	var NumCollection = Backbone.Collection.extend({
		model: Num,
		url: "/numbers"
	});

	var NumView = Backbone.View.extend({
		tagName: "tr",
		template: _.template($("#number-row").html()),

		events: {
			"click .delete": "deleteRow",
			"mouseenter": "showControls",
			"mouseleave": "hideControls"
		},

		render: function() {
			this.$el.html(this.template(this.model.toJSON()));
			return this;
		},

		deleteRow: function() {
			this.model.destroy();
			this.remove();
		},

		showControls: function() {
			this.$("button.delete").addClass("btn-danger");
		},

		hideControls: function() {
			this.$("button.delete").removeClass("btn-danger");
		}
	});

	var NumCollectionView = Backbone.View.extend({
		el: ".container",

		events: {
			"submit form": "submit"
		},

		initialize: function() {
			this.$("#n").focus();
			this.collection = new NumCollection();
			this.collection.on("sync add remove reset", this.render, this);
		},

		render: function() {
			console.log("Rendering collection...");
			this.$("table tbody").html("");

			this.collection.each(function(number) {
				var numView = new NumView({model: number});
				this.$("table tbody").prepend(numView.render().el);
			});

			this.$("caption span").html(this.collection.length);
		},

		submit: function(e) {
			e.preventDefault();
			var n = this.$("#n").val();
			if (!isNaN(n)) {
				this.collection.create({n: n});
			}
		}
	});
	var numCollectionView = new NumCollectionView();
	numCollectionView.collection.reset(numbers);
})(jQuery);
