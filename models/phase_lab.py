from typing import Required
from odoo import models, fields, api

class PhaseLab(models.Model):
    _name = 'tech.fashion.phase.lab'
    _description = 'Fase di Lavorazione'

    sequence = fields.Integer(string='Sequenza')

    phase_id = fields.Many2one(
        'tech.fashion.phase',
        string = 'Fase Lavorazione',
        help='Seleziona la fase di lavorazione',
        required = True
    )

    # Campo per selezionare il laboratorio (filtrando solo i partner con flag "laboratorio")
    laboratory_id = fields.Many2one(
        'res.partner',
        string='Laboratorio',
        # domain=[('is_laboratory', '=', True)],
        help='Laboratorio assegnato per questa fase'
    )


    price = fields.Float(
        string='Costo',
        default = 0.0,
    )

    time = fields.Integer(
        string='Tempo/Pezzo',
        default=1
    )


    # Costo computato
    tot_cost = fields.Float(
        string='Costo Totale',
        help='Costo Totale',
        compute='_compute_tot_cost'
    )

    # Relazione con la BOM
    bom_id = fields.Many2one(
        'mrp.bom',
        string='BOM',
        ondelete='cascade',
        help='Riferimento alla BOM associata'
    )

    # varianti
    variant_ids = fields.Many2many(
    'product.product',
    'tech_fashion_phase_lab_product_rel', 
    'phase_lab_id',                        
    'product_id',                          
    string='Applica alle Varianti',
    help="Seleziona le varianti a cui si applica questa fase"
    )

    # Campo computed per il dominio, contenente le varianti consentite
    allowed_variant_ids = fields.Many2many(
        'product.product',
        string='Allowed Variants',
        compute='_compute_allowed_variant_ids'
    )

    @api.depends('bom_id')
    def _compute_allowed_variant_ids(self):
        for rec in self:
            if rec.bom_id and rec.bom_id.product_tmpl_id:
                rec.allowed_variant_ids = rec.bom_id.product_tmpl_id.product_variant_ids
            else:
                rec.allowed_variant_ids = self.env['product.product']


    @api.depends('price','time')
    def _compute_tot_cost(self):
        for rec in self:
            rec.tot_cost = rec.time * rec.price