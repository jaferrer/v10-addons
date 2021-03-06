# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from datetime import datetime

class EqStockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def assign_picking(self):
        # Overrided base assign_picking function
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']
        for move in self:
            recompute = False
            
            picking = Picking.search([
                ('group_id', '=', move.group_id.id),
                ('location_id', '=', move.location_id.id),
                ('location_dest_id', '=', move.location_dest_id.id),
                ('picking_type_id', '=', move.picking_type_id.id),
                ('printed', '=', False),
                ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])])

            # Create separate stock picking only if picking_policy is not 'one'
            if picking and move.sale_line_id.order_id.picking_policy != 'one':
                # It is necessary because min date is 'datetime' and eq delivery date is 'date'
                for rec in picking:
                    min_date = datetime.strptime(rec.min_date, '%Y-%m-%d %H:%M:%S').date()
                    eq_delivery_date = datetime.strptime(move.sale_line_id.eq_delivery_date, '%Y-%m-%d').date()
                    if min_date == eq_delivery_date:
                        picking = rec
                        break
                    picking = False
                    
            if not picking:
                recompute = True
                picking = Picking.create(move._get_new_picking_values())
                    
            move.write({'picking_id': picking.id})

            # If this method is called in batch by a write on a one2many and
            # at some point had to create a picking, some next iterations could
            # try to find back the created picking. As we look for it by searching
            # on some computed fields, we have to force a recompute, else the
            # record won't be found.
            if recompute:
                move.recompute()
            
            # With this part, message for the origin of the transfer is created on Delivery Order
            if move.picking_id and move.picking_id.group_id:
                picking = move.picking_id
                order = self.env['sale.order'].sudo().search([('procurement_group_id', '=', picking.group_id.id)])
                picking.message_post_with_view(
                    'mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True
    
    def _get_new_picking_values(self):
        # Overrided base _get_new_picking_values function
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited. """

        # Set min_date only if picking_policy is not 'one', else use the standard date setting
        if self.sale_line_id.order_id.picking_policy != 'one':
            min_date = self.sale_line_id.eq_delivery_date
        else:
            min_date = False

        # Added min_date, set from eq_delivery_date of the corresponding sale_line_id
        return {
            'origin': self.origin,
            'company_id': self.company_id.id,
            'move_type': self.group_id and self.group_id.move_type or 'direct',
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'min_date': min_date
        }
