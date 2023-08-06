
from odoo import api, fields, models


class BeesdooProduct(models.Model):

    _inherit = "product.product"

    @api.multi
    def write(self, values):
        previous_standard_price = {}
        for product in self:
            previous_standard_price[product.id] = product.standard_price
        res = super().write(values)
        for product in self:
            if product.standard_price != previous_standard_price[product.id]:
                product.label_to_be_printed = True
        return res

