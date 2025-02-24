{
    'name': 'TECH 3.0 4Fashion',
    'version': '1.0',
    'summary': 'Aggiunge le funzionalità 4 Fashion ad Odoo 18',
    'description': 'Aggiunge funzionalità per calcolare automaticamente il costo delle varianti di prodotto, delle etichette lavaggio,composizione, fasi lavorazione, etc',
    'author': 'TECH 3.0 Srl',
    'depends': ['base', 'mrp', 'product', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/phase_views.xml',
        'views/composition_label_views.xml',
        'views/washing_label_views.xml',
        'views/bom_views.xml',
        'views/product_views.xml',

        'reports/bom_structure_report.xml',


        'data/phase_data.xml',
    ],
    
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}