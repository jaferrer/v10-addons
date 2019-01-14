# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # product_putaway_ids = fields.One2many(
    #     comodel_name='stock.product.putaway.strategy',
    #     inverse_name='product_product_id',
    #     string="Product stock locations")
    product_putaway_ids = fields.One2many(
        comodel_name='stock.product.putaway.strategy',
        related='product_tmpl_id.product_putaway_ids',
        string="Product stock locations")