from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    alert_before_removal_time = fields.Integer(string='Days between alert and removal dates')
 
