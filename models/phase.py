from odoo import models, fields, api

class Phase(models.Model):
    _name = 'tech.fashion.phase'
    _description = 'Fasi di Lavorazione'

    name = fields.Char(string="Lavorazione")