from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    composition_label_ids = fields.Many2many(
        'tech.fashion.composition.label',
        string='Composizioni',
        help='Seleziona le composizioni del prodotto'
    )