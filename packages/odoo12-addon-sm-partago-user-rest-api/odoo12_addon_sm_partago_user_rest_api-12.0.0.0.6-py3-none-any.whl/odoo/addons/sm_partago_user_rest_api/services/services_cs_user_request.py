import logging

from werkzeug.exceptions import BadRequest, NotFound

from odoo import _
from odoo.fields import Date

from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component

from . import schemas
from odoo.addons.sm_maintenance.models.models_api_services_utils import api_services_utils
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

_logger = logging.getLogger(__name__)

class CSUserRequestService(Component):
  _inherit = "emc.rest.service"
  _name = "sm_partago_user.carsharing_user_request.services"
  _usage = "cs-user-request"
  _description = """
    Carsharing User Request Service
  """

  def get(self, _id):
    record = self.env["sm_partago_user.carsharing_user_request"].search(
      [("id", "=", _id)]
    )
    if record:
      return self._to_dict(record)
    else:
      raise wrapJsonException(
        NotFound(_("No record for id %s") % _id)
      )

  def create(self, **params):  # pylint: disable=method-required-super
    params = self._prepare_create(params)
    record = self.env["sm_partago_user.carsharing_user_request"].create(params)
    return self._to_dict(record)

  def update(self, _id, **params):
    params = self._prepare_create(params)
    record = self.env["sm_partago_user.carsharing_user_request"].search(
      [("_api_external_id", "=", _id)]
    )
    if not record:
      raise wrapJsonException(
        NotFound(_("No record for id %s") % _id)
      )
    record.write(params)
    return self._to_dict(record)

  def validate(self, _id, **params):
    record = self.env["sm_partago_user.carsharing_user_request"].search(
      [("_api_external_id", "=", _id)]
    )
    if not record:
      raise wrapJsonException(
        NotFound(_("No record for id %s") % _id)
      )
    return self._to_dict(record)

  """Prepare a writable dictionary of values"""
  def _prepare_create(self, params):
    utils = api_services_utils.get_instance()
    attributes = {
      "name",
      "type",
      "data_partner_firstname",
      "data_partner_lastname",
      "data_partner_vat",
      "data_partner_email",
      "data_partner_mobile",
      "data_partner_phone",
      "data_partner_gender",
      "data_partner_birthdate_date",
      "data_partner_street",
      "data_partner_zip",
      "data_partner_city",
      "data_partner_iban",
      "data_partner_driving_license_expiration_date",
      "data_partner_image_dni",
      "data_partner_image_driving_license",
      "data_partner_image_address_certificate",
    }
    create_dict = utils.generate_create_dictionary(params, attributes)
    try:
      state = params['data_partner_state']
    except:
      state = False
    if state:
      create_dict['data_partner_state_id'] = sm_utils.get_state_id_from_code(self,params['data_partner_state'])
    return create_dict

  def _to_dict(self, record):
    record.ensure_one()
    utils = api_services_utils.get_instance()
    attributes = {
      "name",
      "type",
      "data_partner_firstname",
      "data_partner_lastname",
      "data_partner_vat",
      "data_partner_email",
      "data_partner_mobile",
      "data_partner_phone",
      "data_partner_gender",
      "data_partner_birthdate_date",
      "data_partner_street",
      "data_partner_zip",
      "data_partner_city",
      "data_partner_state_id",
      "data_partner_iban",
      "data_partner_driving_license_expiration_date",
      "data_partner_image_dni",
      "data_partner_image_driving_license",
      "data_partner_image_address_certificate"
    }
    return utils.generate_get_dictionary(record, attributes)

  def _validator_get(self):
    return schemas.S_CS_USER_REQUEST_GET

  def _validator_return_get(self):
    return schemas.S_CS_USER_REQUEST_RETURN_GET

  def _validator_create(self):
    return schemas.S_CS_USER_REQUEST_CREATE

  def _validator_return_create(self):
    return schemas.S_CS_USER_REQUEST_RETURN_GET

  def _validator_update(self):
    return schemas.S_CS_USER_REQUEST_UPDATE

  def _validator_return_update(self):
    return schemas.S_CS_USER_REQUEST_RETURN_GET

  def _validator_validate(self):
    return schemas.S_CS_USER_REQUEST_VALIDATE

  def _validator_return_validate(self):
    return schemas.S_CS_USER_REQUEST_RETURN_GET