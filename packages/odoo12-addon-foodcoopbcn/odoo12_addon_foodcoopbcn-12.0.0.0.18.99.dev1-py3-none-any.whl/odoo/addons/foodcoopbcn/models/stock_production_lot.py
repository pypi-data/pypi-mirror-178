from odoo import models, api
import datetime


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.multi
    def write(self, vals):
        alert_dates_calc = {}
        ret = super().write(vals)
        for lot in self:
            if 'removal_date' in vals and lot.product_id.categ_id.alert_before_removal_time:
                duration = lot.product_id.categ_id.alert_before_removal_time
                if lot.removal_date:
                    lot.alert_date = lot.removal_date - datetime.timedelta(duration)
                else:
                    lot.alert_date = False
        return ret


