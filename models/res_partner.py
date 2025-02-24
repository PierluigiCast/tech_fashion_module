from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_laboratory = fields.Boolean(
        string='Laboratorio',
        default=False,
        help='Se attivato, indica che il partner è un laboratorio esterno.'
    )