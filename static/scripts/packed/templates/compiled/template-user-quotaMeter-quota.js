(function(){var b=Handlebars.template,a=Handlebars.templates=Handlebars.templates||{};a["template-user-quotaMeter-quota"]=b(function(e,l,d,k,j){d=d||e.helpers;var h="",c,g,f="function",i=this.escapeExpression;h+='<div id="quota-meter" class="quota-meter progress">\n    <div id="quota-meter-bar"  class="quota-meter-bar bar" style="width: ';g=d.quota_percent;if(g){c=g.call(l,{hash:{}})}else{c=l.quota_percent;c=typeof c===f?c():c}h+=i(c)+'%"></div>\n    ';h+='\n    <div id="quota-meter-text" class="quota-meter-text"style="top: 6px">\n        Using ';g=d.quota_percent;if(g){c=g.call(l,{hash:{}})}else{c=l.quota_percent;c=typeof c===f?c():c}h+=i(c)+"%\n    </div>\n</div>";return h})})();