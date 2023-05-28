odoo.define('sync_deta.button', function (require) {
    'use strict';
    
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var field_registry = require('web.field_registry');
    
    var _t = core._t;
    
    var WidgetSyncDetaButton = AbstractField.extend({
        className: 'o_stat_info',
        supportedFieldTypes: ['boolean'], 
        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------
    
        /**
         * A boolean field is always set since false is a valid value.
         *
         * @override
         */
        isSet: function () {
            return true;
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * This widget is supposed to be used inside a stat button and, as such, is
         * rendered the same way in edit and readonly mode.
         *
         * @override
         * @private
         */
        _render: function () {
            this.$el.empty();
            var text = this.value ? _t("Deta Sync") : _t("Deta Sync");
            var hover = this.value ? _t("Deta Sync") : _t("Deta Sync");
            var valColor = this.value ? 'text-success' : 'text-danger';
            var hoverColor = this.value ? 'text-danger' : 'text-success';
            var $val = $('<span>').addClass('o_stat_text o_not_hover ' + valColor).text(text);
            var $hover = $('<span>').addClass('o_stat_text o_hover ' + hoverColor).text(hover);
            this.$el.append($val).append($hover);
        },     
    });
    
    field_registry
        .add('widget_sync_deta', WidgetSyncDetaButton);
    });
    