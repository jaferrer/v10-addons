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

from odoo import models, fields, api, _


class eq_product_template(models.Model):
    _inherit = 'product.template'


    #Überschreibt Constraint aus product.template, sodass dieser immer wahr ist.

    _sql_constraints = [
        ('default_code_unique', 'check(1=1)', "This Product No. is already in use!"),
    ]


class eq_product_product(models.Model):
    _inherit = 'product.product'


    #Überschreibt Constraint aus product.template, sodass dieser immer wahr ist.

    _sql_constraints = [
        ('default_code_unique', 'check(1=1)', "This Product No. is already in use!"),
    ]