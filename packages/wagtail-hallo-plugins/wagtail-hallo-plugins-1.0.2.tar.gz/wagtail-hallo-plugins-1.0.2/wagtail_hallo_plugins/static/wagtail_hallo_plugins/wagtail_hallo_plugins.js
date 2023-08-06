(function() {
    (function($) {
        return $.widget('IKS.superscriptbutton', {
            populateToolbar: function(toolbar) {
                var button, widget;
                widget = this;

                var getEnclosing = function(tag) {
                    var node = widget.options.editable.getSelection().commonAncestorContainer;
                    return $(node).parents(tag).get(0);
                };



                button = $('<span></span>');
                button.hallobutton({
                                    uuid: this.options.uuid,
                                    editable: this.options.editable,
                                    label: 'Superscript',
                                    icon: 'fa fa-superscript',
                                    command: null,
                                    queryState: function(event) {
                                        return button.hallobutton('checked', !!getEnclosing("sup"));
                                    }
                }); 

                toolbar.append(button);

                button.on('click', function(event) {
                    return widget.options.editable.execute(
                        getEnclosing("sup") ? 'removeFormat' : 'superscript');
                });

                }
        });
    })(jQuery);
}).call(this);
 
(function() {
    (function($) {
        return $.widget('IKS.subscriptbutton', {
            populateToolbar: function(toolbar) {
                var button, widget;
                widget = this;

                var getEnclosing = function(tag) {
                    var node = widget.options.editable.getSelection().commonAncestorContainer;
                    return $(node).parents(tag).get(0);
                };



                button = $('<span></span>');
                button.hallobutton({
                                    uuid: this.options.uuid,
                                    editable: this.options.editable,
                                    label: 'Subscript',
                                    icon: 'fa fa-subscript',
                                    command: null,
                                    queryState: function(event) {
                                        return button.hallobutton('checked', !!getEnclosing("sub"));
                                    }
                }); 

                toolbar.append(button);

                button.on('click', function(event) {
                    return widget.options.editable.execute(
                        getEnclosing("sub") ? 'removeFormat' : 'subscript');
                });

                }
        });
    })(jQuery);
}).call(this);
 