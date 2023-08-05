# -*- coding: utf-8 -*-
"""
    package.py

"""
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Or, Bool, Id

__metaclass__ = PoolMeta
__all__ = ['Package']


class Package:
    __name__ = 'stock.package'

    tracking_number = fields.Function(
        fields.Many2One('shipment.tracking', 'Tracking Number'),
        'get_tracking_number', searcher="search_tracking_number"
    )

    weight = fields.Function(
        fields.Float(
            "Weight", digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits'],
        ),
        'get_weight'
    )
    weight_uom = fields.Function(
        fields.Many2One('product.uom', 'Weight UOM'),
        'get_weight_uom'
    )
    weight_digits = fields.Function(
        fields.Integer('Weight Digits'), 'on_change_with_weight_digits'
    )

    computed_weight = fields.Function(
        fields.Float(
            "Computed Weight", digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits'],
        ),
        'get_computed_weight'
    )

    override_weight = fields.Float(
        "Override Weight", digits=(16, Eval('weight_digits', 2)),
        depends=['weight_digits'],
    )

    available_box_types = fields.Function(
        fields.One2Many("carrier.box_type", None, "Available Box Types"),
        getter="on_change_with_available_box_types"
    )
    box_type = fields.Many2One(
        'carrier.box_type', 'Box Types', domain=[
            ('id', 'in', Eval('available_box_types'))
        ], depends=["available_box_types"]
    )

    length = fields.Float('Length')
    width = fields.Float('Width')
    height = fields.Float('Height')
    distance_unit = fields.Many2One(
        'product.uom', 'Distance Unit', states={
            'required': Or(Bool(Eval('length')), Bool(
                Eval('width')), Bool(Eval('height')))
        },
        domain=[
            ('category', '=', Id('product', 'uom_cat_length'))
        ], depends=['length', 'width', 'height']
    )

    @fields.depends("_parent_shipment", "_parent_shipment.carrier")
    def on_change_with_available_box_types(self, name=None):
        if self.shipment.carrier:
            return map(int, self.shipment.carrier.box_types)
        return []

    def _process_raw_label(self, data, **kwargs):
        "Downstream modules can use this method to process label image"
        return data

    def get_tracking_number(self, name):
        """
        Return first tracking number for this package
        """
        Tracking = Pool().get('shipment.tracking')

        tracking_numbers = Tracking.search([
            ('origin', '=', '%s,%s' % (self.__name__, self.id)),
        ], limit=1)

        return tracking_numbers and tracking_numbers[0].id or None

    @classmethod
    def search_tracking_number(cls, name, clause):
        Tracking = Pool().get('shipment.tracking')

        tracking_numbers = Tracking.search([
            ('origin', 'like', 'stock.package,%'),
            ('tracking_number', ) + tuple(clause[1:])
        ])
        return [
            ('id', 'in', map(lambda x: x.origin.id, tracking_numbers))
        ]

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2

    def get_weight_uom(self, name):
        """
        Returns weight uom for the package from shipment
        """
        return self.shipment.weight_uom.id

    def get_weight(self, name):
        """
        Returns package weight if weight is not overriden
        otherwise returns overriden weight
        """
        return self.override_weight or self.get_computed_weight()

    def get_computed_weight(self, name=None):
        """
        Returns sum of weight associated with each move line
        """
        return sum(map(
            lambda move: move.get_weight(self.weight_uom, silent=True),
            self.moves
        ))

    @staticmethod
    def default_type():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id(
            'shipping', 'shipment_package_type'
        )

    @staticmethod
    def default_distance_unit():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id(
            'product', 'uom_inch'
        )
