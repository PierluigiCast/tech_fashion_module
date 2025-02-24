from odoo import models, fields

class CompositionLabel(models.Model):
    _name = 'tech.fashion.composition.label'
    _description = 'Composizione'

    name = fields.Char(string='Composizione', required=True)
    engname = fields.Char(string='Composizione Inglese', required=False)
    japname = fields.Char(string='Composizione Giapponese', required=False)
