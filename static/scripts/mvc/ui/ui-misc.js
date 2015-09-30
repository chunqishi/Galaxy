define(["utils/utils","mvc/ui/ui-select-default","mvc/ui/ui-slider","mvc/ui/ui-options","mvc/ui/ui-drilldown","mvc/ui/ui-buttons","mvc/ui/ui-modal"],function(a,b,c,d,e,f,g){var h=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{url:"",cls:""}),this.setElement(this._template(this.options))},_template:function(a){return'<img class="ui-image '+a.cls+'" src="'+a.url+'"/>'}}),i=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{title:"",cls:""}),this.setElement(this._template(this.options))},title:function(a){this.$el.html(a)},value:function(){return options.title},_template:function(a){return'<label class="ui-label '+a.cls+'">'+a.title+"</label>"}}),j=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{floating:"right",icon:"",tooltip:"",placement:"bottom",title:"",cls:""}),this.setElement(this._template(this.options)),$(this.el).tooltip({title:b.tooltip,placement:"bottom"})},_template:function(a){return'<div><span class="fa '+a.icon+'" class="ui-icon"/>&nbsp;'+a.title+"</div>"}}),k=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{title:"",cls:""}),this.setElement(this._template(this.options)),$(this.el).on("click",b.onclick)},_template:function(a){return'<div><a href="javascript:void(0)" class="ui-anchor '+a.cls+'">'+a.title+"</a></div>"}}),l=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{message:null,status:"info",cls:"",persistent:!1}),this.setElement('<div class="'+this.options.cls+'"/>'),this.options.message&&this.update(this.options)},update:function(b){if(this.options=a.merge(b,this.options),""!=b.message){if(this.$el.html(this._template(this.options)),this.$el.fadeIn(),this.timeout&&window.clearTimeout(this.timeout),!b.persistent){var c=this;this.timeout=window.setTimeout(function(){c.$el.is(":visible")?c.$el.fadeOut():c.$el.hide()},3e3)}}else this.$el.fadeOut()},_template:function(a){var b="ui-message alert alert-"+a.status;return a.large&&(b=("success"==a.status&&"done"||"danger"==a.status&&"error"||a.status)+"messagelarge"),'<div class="'+b+'" >'+a.message+"</div>"}}),m=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{onclick:null,searchword:""}),this.setElement(this._template(this.options));var c=this;this.options.onclick&&this.$el.on("submit",function(){var a=c.$el.find("#search");c.options.onclick(a.val())})},_template:function(a){return'<div class="ui-search"><form onsubmit="return false;"><input id="search" class="form-control input-sm" type="text" name="search" placeholder="Search..." value="'+a.searchword+'"><button type="submit" class="btn search-btn"><i class="fa fa-search"></i></button></form></div>'}}),n=Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{type:"text",placeholder:"",disabled:!1,visible:!0,cls:"",area:!1}),this.setElement(this._template(this.options)),void 0!==this.options.value&&this.value(this.options.value),this.options.disabled&&this.$el.prop("disabled",!0),this.options.visible||this.$el.hide();var c=this;this.$el.on("input",function(){c.options.onchange&&c.options.onchange(c.$el.val())})},value:function(a){return void 0!==a&&this.$el.val(a),this.$el.val()},_template:function(a){return a.area?'<textarea id="'+a.id+'" class="ui-textarea '+a.cls+'"></textarea>':'<input id="'+a.id+'" type="'+a.type+'" value="'+a.value+'" placeholder="'+a.placeholder+'" class="ui-input '+a.cls+'">'}}),o=Backbone.View.extend({initialize:function(a){this.options=a,this.setElement(this._template(this.options)),void 0!==this.options.value&&this.value(this.options.value)},value:function(a){return void 0!==a&&this.$("hidden").val(a),this.$("hidden").val()},_template:function(a){var b='<div id="'+a.id+'" >';return a.info&&(b+="<div>"+a.info+"</div>"),b+='<hidden value="'+a.value+'"/></div>'}});return{Anchor:k,Button:f.ButtonDefault,ButtonIcon:f.ButtonIcon,ButtonCheck:f.ButtonCheck,ButtonMenu:f.ButtonMenu,ButtonLink:f.ButtonLink,Icon:j,Image:h,Input:n,Label:i,Message:l,Modal:g,RadioButton:d.RadioButton,Checkbox:d.Checkbox,Radio:d.Radio,Searchbox:m,Select:b,Hidden:o,Slider:c,Drilldown:e}});
//# sourceMappingURL=../../../maps/mvc/ui/ui-misc.js.map