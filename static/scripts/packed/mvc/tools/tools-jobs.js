define(["utils/utils"],function(a){return Backbone.Model.extend({initialize:function(c,b){this.app=c;this.options=a.merge(b,this.optionsDefault)},submit:function(){var b=this;var c={tool_id:this.app.options.id,inputs:this.app.tree.finalize()};this.app.reset();a.request("POST",galaxy_config.root+"api/tools",c,function(d){if(!d.outputs||d.outputs.length==0){console.debug(d)}b.app.message({text:"A job has been successfully added to the queue. You can check the status of queued jobs and view the resulting data by refreshing the History pane. When the job has been run the status will change from 'running' to 'finished' if completed successfully or 'error' if problems were encountered."});b._refreshHdas()},function(d){console.debug(d);if(d&&d.message&&d.message.data){var g=b.app.tree.match(d.message.data);for(var f in g){var e=g[f];if(!e){e="Please verify this parameter."}b.app.element_list[f].error(e)}}})},_refreshHdas:function(){if(parent.Galaxy&&parent.Galaxy.currHistoryPanel){parent.Galaxy.currHistoryPanel.refreshContents()}}})});