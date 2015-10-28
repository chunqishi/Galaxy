define(["mvc/list/list-panel","mvc/history/history-model","mvc/history/history-contents","mvc/history/hda-li","mvc/history/hdca-li","mvc/collection/collection-panel","mvc/user/user-model","ui/fa-icon-button","mvc/ui/popup-menu","mvc/base-mvc","utils/localization","ui/search-input"],function(a,b,c,d,e,f,g,h,i,j,k){var l=j.SessionStorageModel.extend({defaults:{expandedIds:{},show_deleted:!1,show_hidden:!1},addExpanded:function(a){var b="expandedIds";this.save(b,_.extend(this.get(b),_.object([a.id],[a.get("id")])))},removeExpanded:function(a){var b="expandedIds";this.save(b,_.omit(this.get(b),a.id))},toString:function(){return"HistoryPrefs("+this.id+")"}});l.storageKeyPrefix="history:",l.historyStorageKey=function(a){if(!a)throw new Error("HistoryPrefs.historyStorageKey needs valid id: "+a);return l.storageKeyPrefix+a},l.get=function(a){return new l({id:l.historyStorageKey(a)})},l.clearAll=function(){for(var a in sessionStorage)0===a.indexOf(l.storageKeyPrefix)&&sessionStorage.removeItem(a)};var m=a.ModelListPanel,n=m.extend({HDAViewClass:d.HDAListItemView,HDCAViewClass:e.HDCAListItemView,collectionClass:c.HistoryContents,modelCollectionKey:"contents",tagName:"div",className:m.prototype.className+" history-panel",emptyMsg:k("This history is empty"),noneFoundMsg:k("No matching datasets found"),searchPlaceholder:k("search datasets"),initialize:function(a){m.prototype.initialize.call(this,a),this.linkTarget=a.linkTarget||"_blank"},freeModel:function(){return m.prototype.freeModel.call(this),this.model&&this.model.clearUpdateTimeout(),this},_setUpListeners:function(){m.prototype._setUpListeners.call(this),this.on({error:function(a,b,c,d,e){this.errorHandler(a,b,c,d,e)},"loading-done":function(){this.views.length||this.trigger("empty-history",this)},"views:ready view:attached view:removed":function(){this._renderSelectButton()}})},loadHistoryWithDetails:function(a,b,c,d){this.info("loadHistoryWithDetails:",a,b,c,d);var e=function(a){return _.values(l.get(a.id).get("expandedIds"))};return this.loadHistory(a,b,c,d,e)},loadHistory:function(a,c,d,e,f){this.info("loadHistory:",a,c,d,e,f);var g=this;c=c||{},g.trigger("loading",g);var h=b.History.getHistoryData(a,{historyFn:d,contentsFn:e,detailIdsFn:c.initiallyExpanded||f});return g._loadHistoryFromXHR(h,c).fail(function(b,d,e){g.trigger("error",g,b,c,k("An error was encountered while "+d),{historyId:a,history:e||{}})}).always(function(){g.trigger("loading-done",g)})},_loadHistoryFromXHR:function(a,b){var c=this;return a.then(function(a,d){c.JSONToModel(a,d,b),c.render()}),a.fail(function(){c.render()}),a},refreshContents:function(a,b){return this.model?this.model.refresh(a,b):$.when()},JSONToModel:function(a,c,d){this.log("JSONToModel:",a,c,d),d=d||{};var e=new b.History(a,c,d);return this.setModel(e),e},setModel:function(a,b){b=b||{},m.prototype.setModel.call(this,a,b),this.model&&this._setUpWebStorage(b.initiallyExpanded,b.show_deleted,b.show_hidden)},_setUpWebStorage:function(a,b,c){return this.storage&&this.stopListening(this.storage),this.storage=new l({id:l.historyStorageKey(this.model.get("id"))}),_.isObject(a)&&this.storage.set("expandedIds",a),_.isBoolean(b)&&this.storage.set("show_deleted",b),_.isBoolean(c)&&this.storage.set("show_hidden",c),this.trigger("new-storage",this.storage,this),this.log(this+" (init'd) storage:",this.storage.get()),this.listenTo(this.storage,{"change:show_deleted":function(a,b){this.showDeleted=b},"change:show_hidden":function(a,b){this.showHidden=b}},this),this.showDeleted=void 0!==b?b:this.storage.get("show_deleted"),this.showHidden=void 0!==c?c:this.storage.get("show_hidden"),this},_buildNewRender:function(){var a=m.prototype._buildNewRender.call(this);return this._renderSelectButton(a),a},_renderSelectButton:function(a){if(a=a||this.$el,!this.multiselectActions().length)return null;if(!this.views.length)return this.hideSelectors(),a.find(".controls .actions .show-selectors-btn").remove(),null;var b=a.find(".controls .actions .show-selectors-btn");return b.size()?b:h({title:k("Operations on multiple datasets"),classes:"show-selectors-btn",faIcon:"fa-check-square-o"}).prependTo(a.find(".controls .actions"))},_getItemViewClass:function(a){var b=a.get("history_content_type");switch(b){case"dataset":return this.HDAViewClass;case"dataset_collection":return this.HDCAViewClass}throw new TypeError("Unknown history_content_type: "+b)},_filterItem:function(a){var b=this;return m.prototype._filterItem.call(b,a)&&(!a.hidden()||b.showHidden)&&(!a.isDeletedOrPurged()||b.showDeleted)},_getItemViewOptions:function(a){var b=m.prototype._getItemViewOptions.call(this,a);return _.extend(b,{linkTarget:this.linkTarget,expanded:!!this.storage.get("expandedIds")[a.id],hasUser:this.model.ownedByCurrUser()})},_setUpItemViewListeners:function(a){var b=this;return m.prototype._setUpItemViewListeners.call(b,a),a.on("expanded",function(a){b.storage.addExpanded(a.model)}),a.on("collapsed",function(a){b.storage.removeExpanded(a.model)}),this},getSelectedModels:function(){var a=m.prototype.getSelectedModels.call(this);return a.historyId=this.collection.historyId,a},events:_.extend(_.clone(m.prototype.events),{"click .show-selectors-btn":"toggleSelectors","click .messages [class$=message]":"clearMessages"}),toggleShowDeleted:function(a,b){return a=void 0!==a?a:!this.showDeleted,b=void 0!==b?b:!0,this.showDeleted=a,b&&this.storage.set("show_deleted",a),this.renderItems(),this.trigger("show-deleted",a),this.showDeleted},toggleShowHidden:function(a,b){return a=void 0!==a?a:!this.showHidden,b=void 0!==b?b:!0,this.showHidden=a,b&&this.storage.set("show_hidden",a),this.renderItems(),this.trigger("show-hidden",a),this.showHidden},_firstSearch:function(a){var b=this,c=".history-search-input";return this.log("onFirstSearch",a),b.model.contents.haveDetails()?void b.searchItems(a):(b.$el.find(c).searchInput("toggle-loading"),void b.model.contents.fetchAllDetails({silent:!0}).always(function(){b.$el.find(c).searchInput("toggle-loading")}).done(function(){b.searchItems(b.searchFor)}))},errorHandler:function(a,b,c,d,e){if(this.error(a,b,c,d,e),b&&0===b.status&&0===b.readyState);else if(b&&502===b.status);else{var f=this._parseErrorMessage(a,b,c,d,e);this.$messages().is(":visible")?this.displayMessage("error",f.message,f.details):this.once("rendered",function(){this.displayMessage("error",f.message,f.details)})}},_parseErrorMessage:function(a,b,c,d,e){var f=Galaxy.currUser,h={message:this._bePolite(d),details:{message:d,raven:window.Raven&&_.isFunction(Raven.lastEventId)?Raven.lastEventId():void 0,agent:navigator.userAgent,url:window.Galaxy?Galaxy.lastAjax.url:void 0,data:window.Galaxy?Galaxy.lastAjax.data:void 0,options:b?_.omit(c,"xhr"):c,xhr:b,source:_.isFunction(a.toJSON)?a.toJSON():a+"",user:f instanceof g.User?f.toJSON():f+""}};if(_.extend(h.details,e||{}),b&&_.isFunction(b.getAllResponseHeaders)){var i=b.getAllResponseHeaders();i=_.compact(i.split("\n")),i=_.map(i,function(a){return a.split(": ")}),h.details.xhr.responseHeaders=_.object(i)}return h},_bePolite:function(a){return a=a||k("An error occurred while getting updates from the server"),a+". "+k("Please contact a Galaxy administrator if the problem persists")+"."},displayMessage:function(a,b,c){var d=this;this.scrollToTop();var e=this.$messages(),f=$("<div/>").addClass(a+"message").html(b);if(!_.isEmpty(c)){var g=$('<a href="javascript:void(0)">Details</a>').click(function(){return Galaxy.modal.show(d._messageToModalOptions(a,b,c)),!1});f.append(" ",g)}return e.append(f)},_messageToModalOptions:function(a,b,c){var d=this,e={title:"Details"};if(_.isObject(c)){c=_.omit(c,_.functions(c));var f=JSON.stringify(c,null,"  "),g=$("<pre/>").text(f);e.body=$("<div/>").append(g)}else e.body=$("<div/>").html(c);return e.buttons={Ok:function(){Galaxy.modal.hide(),d.clearMessages()}},e},clearMessages:function(a){var b=_.isUndefined(a)?this.$messages().children('[class$="message"]'):$(a.currentTarget);return b.fadeOut(this.fxSpeed,function(){$(this).remove()}),this},scrollToHid:function(a){return this.scrollToItem(_.first(this.viewsWhereModel({hid:a})))},toString:function(){return"HistoryPanel("+(this.model?this.model.get("name"):"")+")"}});return n.prototype.templates=function(){var a=j.wrapTemplate(['<div class="controls">','<div class="title">','<div class="name"><%= history.name %></div>',"</div>",'<div class="subtitle"></div>','<div class="history-size"><%= history.nice_size %></div>','<div class="actions"></div>','<div class="messages">',"<% if( history.deleted && history.purged ){ %>",'<div class="deleted-msg warningmessagesmall">',k("This history has been purged and deleted"),"</div>","<% } else if( history.deleted ){ %>",'<div class="deleted-msg warningmessagesmall">',k("This history has been deleted"),"</div>","<% } else if( history.purged ){ %>",'<div class="deleted-msg warningmessagesmall">',k("This history has been purged"),"</div>","<% } %>","<% if( history.message ){ %>",'<div class="<%= history.message.level || "info" %>messagesmall">',"<%= history.message.text %>","</div>","<% } %>","</div>",'<div class="tags-display"></div>','<div class="annotation-display"></div>','<div class="search">','<div class="search-input"></div>',"</div>",'<div class="list-actions">','<div class="btn-group">','<button class="select-all btn btn-default"','data-mode="select">',k("All"),"</button>",'<button class="deselect-all btn btn-default"','data-mode="select">',k("None"),"</button>","</div>",'<div class="list-action-menu btn-group">',"</div>","</div>","</div>"],"history");return _.extend(_.clone(m.prototype.templates),{controls:a})}(),{HistoryPanel:n}});
//# sourceMappingURL=../../../maps/mvc/history/history-panel.js.map