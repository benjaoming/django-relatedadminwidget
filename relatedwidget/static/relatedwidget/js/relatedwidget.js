function dismissEditRelatedPopup(win, objId, newRepr) {
	objId = html_unescape(objId);
	newRepr = html_unescape(newRepr);
	var name = windowname_to_id(win.name).replace(/^edit_/, '');;
	var elem = document.getElementById(name);
	if (elem) {
		var opts = elem.options,
				l = opts.length;
		for (var i = 0; i < l; i++) {
			if (opts[i] && opts[i].value == objId) {
				opts[i].innerHTML = newRepr;
			}
		}
	}
	win.close();
};

if (!dismissAddAnotherPopup.original) {
	var originalDismissAddAnotherPopup = dismissAddAnotherPopup;
	dismissAddAnotherPopup = function(win, newId, newRepr) {
		originalDismissAddAnotherPopup(win, newId, newRepr);
		newId = html_unescape(newId);
		newRepr = html_unescape(newRepr);
		var id = windowname_to_id(win.name);
		$('#' + id).trigger('change');
	};
	dismissAddAnotherPopup.original = originalDismissAddAnotherPopup;
}

django.jQuery(document).ready(function() {
  
  var $ = $ || jQuery || django.jQuery,
  		relatedWidgetCSSSelector = '.related-widget-wrapper-change-link, .related-widget-wrapper-delete-link',
  		hrefTemplateAttr = 'data-href-template';
  
  $('.related-widget-wrapper').live('change', function(){
  	var siblings = $(this).nextAll(relatedWidgetCSSSelector);
  	if (!siblings.length) return;
  	if (this.value) {
  		var val = this.value;
  		siblings.each(function(){
  			var elm = $(this);
  			elm.attr('href', interpolate(elm.attr(hrefTemplateAttr), [val]));
  		});
  	} else siblings.removeAttr('href');
  });
	
	$('.related-widget-wrapper-link').live('click', function(){
		if (this.href) {
			return showAddAnotherPopup(this);
		} else return false;
	});
  
});
