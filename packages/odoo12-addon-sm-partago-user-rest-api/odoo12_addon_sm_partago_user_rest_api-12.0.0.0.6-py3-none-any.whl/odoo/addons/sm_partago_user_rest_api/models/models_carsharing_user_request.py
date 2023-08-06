from odoo import models

class carsharing_user_request(models.Model):
    _name = 'sm_partago_user.carsharing_user_request'
    _inherit = ["sm_partago_user.carsharing_user_request", "external.id.mixin"]