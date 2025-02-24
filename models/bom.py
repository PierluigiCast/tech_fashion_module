from odoo import models, fields, api

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    #variabili
    #checkbox "aggiorna listino"
    update_list_price = fields.Boolean(
        string='Aggiorna Listino',
        default=True,
        help='Se attivo, aggiorna automaticamente il prezzo di vendita in base al costo e al margine.'
    )

    #margine di profitto
    profit_margin = fields.Float(
        string='Margine',
        default=2.5,  # Imposta un margine predefinito del 20%
        help='Margine di profitto applicato al costo standard per calcolare il prezzo di vendita.'
    )

    #costi delle varianti
    variant_costs = fields.Html(
        string='Costi per Variante',
        compute='_compute_variant_costs',
        help='Costi calcolati per ogni variante del prodotto.'
    )

    #listini delle varianti
    all_lists = fields.Html(
        string='Listino per Variante',
        compute='_compute_variant_costs',
        help='Listini calcolati per ogni variante del prodotto.'
    )

    #etichette di lavaggio
    washing_label_ids = fields.Many2many(
        'tech.fashion.washing.label',
        string='Etichette di Lavaggio',
        help='Seleziona le etichette di lavaggio per questa BOM.'
    )


    # Campo One2many per gestire le fasi di lavorazione
    phase_ids = fields.One2many(
        'tech.fashion.phase.lab',
        'bom_id',
        string='Fasi di Lavorazione',
        help='Fasi di lavorazione con assegnazione dei laboratori e costo',
        order="sequence",
    )


    @api.model
    def default_get(self, fields_list):
        res = super(MrpBom, self).default_get(fields_list)
        # Recupera tutte le fasi di lavorazione definite nel sistema
        phases = self.env['tech.fashion.phase'].search([])
        # Per ogni fase, prepara la linea da inserire in phase_ids
        phase_lines = []
        sequence = 0
        for phase in phases:
            phase_lines.append((0, 0, {
                'phase_id': phase.id,
                'time':1,
                'sequence': sequence,
            }))
            sequence = sequence+1
        res['phase_ids'] = phase_lines
        return res

    @api.depends('product_tmpl_id', 'bom_line_ids', 'operation_ids', 'update_list_price', 'profit_margin')
    def _compute_variant_costs(self):
        for bom in self:
            if not bom.product_tmpl_id:
                bom.variant_costs = "Nessun prodotto associato."
                bom.all_lists = "Nessun prodotto associato."
                continue

            # Ottieni tutte le varianti del prodotto
            variants = bom.product_tmpl_id.product_variant_ids

            # Calcola il costo per ogni variante
            costs = []
            listini = []
            for variant in variants:
                total_cost = 0.0
                list_price = 0.0
                component_price = 0.0
                phase_price = 0.0

                # Filtra le linee della BOM applicabili alla variante
                for line in bom.bom_line_ids:
                    # Se la linea ha attributi specifici, verifica se almeno uno corrisponde alla variante
                    if line.bom_product_template_attribute_value_ids:
                        # Ottieni gli attributi della variante
                        variant_attributes = variant.product_template_attribute_value_ids
                        # Verifica se almeno un attributo della linea è presente nella variante
                        if any(
                            attr in variant_attributes
                            for attr in line.bom_product_template_attribute_value_ids
                        ):
                            total_cost += line.product_id.standard_price * line.product_qty
                            component_price += line.product_id.standard_price * line.product_qty
                    # Se la linea è generica (senza attributi specifici), applica a tutte
                    else:
                        total_cost += line.product_id.standard_price * line.product_qty
                        component_price += line.product_id.standard_price * line.product_qty

                # Calcola il costo delle operazioni
                for operation in bom.operation_ids:
                    total_cost += operation.time_cycle * operation.workcenter_id.costs_hour

                # Calcola il costo delle fasi
                for phase in bom.phase_ids:
                    if phase.variant_ids and variant.id in phase.variant_ids.ids:
                        phase_price += phase.tot_cost
                        total_cost += phase.tot_cost
                    else:
                        if not phase.variant_ids:
                            phase_price += phase.tot_cost
                            total_cost += phase.tot_cost
                
                # Aggiorna il campo standard_price della variante
                variant.standard_price = total_cost

                # Aggiorna il prezzo di vendita se la checkbox è attiva
                if bom.update_list_price and bom.profit_margin:
                    # Calcola il prezzo di vendita in base al margine di profitto
                    list_price = total_cost * bom.profit_margin
                    # Aggiorna il campo price_extra degli attributi della variante
                    for attr_value in variant.product_template_attribute_value_ids:
                        attr_value.price_extra = list_price
                    # Imposto il supplemento ad ogni variante pari al costo + margine
                    #variant.price_extra = list_price
                    
                    costs.append(f"<b>{variant.display_name}</b>: {total_cost:.2f}€ (Comp: {component_price:.2f}€ - Lab: {phase_price:.2f})")
                    listini.append(f"<b>{variant.display_name}</b>: {list_price:.2f}€")

                else:
                    # Calcola il prezzo di vendita senza margine
                    list_price = total_cost
                    # Aggiorna il campo price_extra degli attributi della variante
                    # for attr_value in variant.product_template_attribute_value_ids:
                    #     attr_value.price_extra = list_price
                    # Imposto il supplemento ad ogni variante pari al costo
                    #variant.price_extra = list_price
                    
                    costs.append(f"<b>{variant.display_name}</b>: {total_cost:.2f}€ (Comp: {component_price:.2f}€ - Lab: {phase_price:.2f})")
                    listini.append(f"<b>{variant.display_name}</b>: {list_price:.2f}€")

                

            # Formatta i costi come HTML
            bom.variant_costs = "<br/>".join(costs)
            bom.all_lists = "<br/>".join(listini)

