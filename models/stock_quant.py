# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from psycopg2 import Error, OperationalError

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    largo = fields.Float(related='lot_id.largo', store=True, readonly=True)
    cantidad_en_metros = fields.Float('Cantidad en metros', compute='_cantidad_en_metros')
    costo_total_en_metros = fields.Float('Costo total en metros', compute='_costo_total_en_metros')

    # @api.one
    @api.depends('largo','quantity')
    def _cantidad_en_metros(self):
        logging.warning('Que es largo?')
        # logging.warning(self.largo)
        for self1 in self:
            logging.warning(self1.largo)
            if self1.largo:
                self1.cantidad_en_metros = self1.largo * self1.qty
            else:
                self1.cantidad_en_metros = 0

    # @api.one
    @api.depends('product_id','cantidad_en_metros')
    def _costo_total_en_metros(self):
        for self1 in self:
            if self1.cantidad_en_metros != 0:
                self1.costo_total_en_metros = self1.product_id.costo_por_metro * self1.cantidad_en_metros
            else:
                self1.costo_total_en_metros = 0

        
    