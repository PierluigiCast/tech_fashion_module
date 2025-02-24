odoo.define('custom_bom.m2m_image_tags', function (require) {
    "use strict";

    var FieldMany2ManyTags = require('web.relational_fields').FieldMany2ManyTags;

    FieldMany2ManyTags.include({
        _renderTag: function (tag) {
            var $tag = this._super.apply(this, arguments);
            if (tag.image) {
                $tag.prepend(
                    $('<img>')
                        .attr('src', 'data:image/png;base64,' + tag.image)
                        .css({ width: '20px', height: '20px', 'margin-right': '5px' })
                );
            }
            return $tag;
        }
    });
});