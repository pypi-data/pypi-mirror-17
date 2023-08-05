# -*- coding: utf-8 -*-
from decimal import Decimal

from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.exceptions import UserError

__metaclass__ = PoolMeta
__all__ = ['Sale']


class Sale:
    __name__ = "sale.sale"

    def _get_carrier_context(self):
        "Pass sale in the context"
        context = super(Sale, self)._get_carrier_context()

        if self.carrier.carrier_cost_method != 'pricelist':
            return context

        context = context.copy()
        context['sale'] = self.id
        return context

    def on_change_lines(self):
        """Pass a flag in context which indicates the get_sale_price method
        of pricelist carrier not to calculate cost on each line change
        """
        with Transaction().set_context({'ignore_carrier_computation': True}):
            return super(Sale, self).on_change_lines()

    def update_pricelist_shipment_cost(self):
        "Add a shipping line to sale for pricelist costmethod"
        Sale = Pool().get('sale.sale')
        Currency = Pool().get('currency.currency')

        if not self.carrier or self.carrier.carrier_cost_method != 'pricelist':
            return

        with Transaction().set_context(self._get_carrier_context()):
            shipment_cost = self.carrier.get_sale_price()
        if not shipment_cost[0]:
            return

        shipment_cost = Currency.compute(
            Currency(shipment_cost[1]), shipment_cost[0], self.currency
        )
        Sale.write([self], {
            'lines': [
                ('create', [{
                    'type': 'line',
                    'product': self.carrier.carrier_product.id,
                    'description': self.carrier.carrier_product.name,
                    'quantity': 1,  # XXX
                    'unit': self.carrier.carrier_product.sale_uom.id,
                    'unit_price': Decimal(shipment_cost),
                    'shipment_cost': Decimal(shipment_cost),
                    'amount': Decimal(shipment_cost),
                    'taxes': [],
                    'sequence': 9999,  # XXX
                }]),
                ('delete', [
                    line for line in self.lines if line.shipment_cost
                ]),
            ]
        })

    def get_pricelist_shipping_cost(self):
        """
        Return pricelist shipping cost
        """
        Product = Pool().get('product.product')
        Carrier = Pool().get('carrier')
        Company = Pool().get('company.company')

        carrier, = Carrier.search([('carrier_cost_method', '=', 'pricelist')])

        total = Decimal('0')

        company = Transaction().context.get('company')
        if not company:
            raise UserError("Company not in context.")

        default_currency = Company(company).currency

        try:
            context = {
                'customer': self.party.id,
                'price_list': carrier.price_list.id,
                'currency': self.currency.id,
            }
        except:
            if Transaction().context.get('ignore_carrier_computation'):
                # If carrier computation is ignored just return the
                # default values
                return Decimal('0'), default_currency.id

        with Transaction().set_context(**context):
            for line in self.lines:
                if not line.product:
                    continue
                total += \
                    Product.get_sale_price([line.product])[line.product.id] * \
                    Decimal(line.quantity)

        return total, self.currency.id

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        # TODO: Fix this method and remove return
        return super(Sale, self).get_shipping_rate(
            carrier, carrier_service, silent
        )
        Currency = Pool().get('currency.currency')

        cost, currency_id = self.get_pricelist_shipping_cost()

        if carrier.carrier_cost_method == 'pricelist':
            rate_dict = {
                'carrier_service': carrier_service,
                'cost': cost,
                'cost_currency': Currency(currency_id),
                'carrier': carrier,
                'display_name': carrier.rec_name
            }
            return [rate_dict]

        return []
