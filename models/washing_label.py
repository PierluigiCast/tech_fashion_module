from odoo import models, fields

class WashingLabel(models.Model):
    _name = 'tech.fashion.washing.label'
    _description = 'Etichette di Lavaggio'

    name = fields.Char(string='Nome', required=True, help='Nome dell\'etichetta di lavaggio.')
    description = fields.Text(string='Descrizione', help='Descrizione dettagliata dell\'etichetta.')
    image = fields.Binary(string='Immagine', help='Immagine associata all\'etichetta.')