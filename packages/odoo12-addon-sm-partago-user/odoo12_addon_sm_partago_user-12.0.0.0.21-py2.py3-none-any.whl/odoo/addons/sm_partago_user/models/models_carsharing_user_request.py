# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

# -*- coding: utf-8 -*-
class carsharing_user_request(models.Model):
  _name = 'sm_partago_user.carsharing_user_request'
  _inherit = ['mail.thread']
  _description = "CS User request"
  _order = "create_date desc"

  # FIELDS: GENERAL
  name = fields.Char(string=_("Name"))
  type = fields.Selection([
    ('elprat_request', _("El Prat")),
  ], default='elprat_request', string=_("Provision type"), required=True)
  # FIELDS: MEMBER
  force_partner_creation = fields.Boolean(string=_("Force partner creation"))
  member_computation_type = fields.Selection([
    ('not_computed', _("Not computed")),
    ('partner_found', _("Partner found")),
    ('partner_new', _("Partner new")),
  ],default='not_computed', string=_("Partner computation type"), required=True)
  cs_user_status = fields.Selection([
    ('only_exists_on_db','Person created on APP (nothing more)'),
    ('requested_access', 'Access request sent'),
    ('active', 'Active'),
    ('blocked_banned', 'Manually Blocked'),
    ('no_access', 'No access')
  ],
  string=_("Carsharing user status"),
  compute="_get_cs_user_status",
  store=False)
  cs_user_type = fields.Selection([
    ('none','None'),
    ('user', 'Regular user'),
    ('promo', 'Promo user'),
    ('maintenance', 'Maintenance user'),
    ('organisation', 'Organisation user')
  ],
  string=_("Carsharing user type"),
  compute="_get_cs_user_type",
  store=False)
  related_member_id = fields.Many2one('res.partner', string=_("Related partner"))

  # FIELDS: STATUS INDICATORS
  completed_date = fields.Date(string=_("Completed Date"))
  completion_status = fields.Selection([
    ('not_executed', 'Not executed'),
    ('error', 'Error'),
    ('completed', 'Completed')
  ], default='not_executed')
  workflow_status = fields.Selection([
    ('new', 'New'),
    ('member_computed','Member computed'),
    ('computed', 'Computed'),
    ('completed', 'Completed'),
    ('cancelled','Cancelled')
  ], default='new')

  # FIELDS: PARTNER CSDATA_IBAN
  data_partner_firstname = fields.Char(string=_("Firstname"))
  data_partner_lastname = fields.Char(string=_("Lastname"))
  data_partner_vat = fields.Char(string=_("VAT"))
  data_partner_email = fields.Char(string=_("Email"))
  data_partner_mobile = fields.Char(string=_("Mobile"))
  data_partner_phone = fields.Char(string=_("Phone"))
  data_partner_gender = fields.Selection(
    [("male", "Male"), ("female", "Female"), ("other", "Other")],
    string=_("Gender"),
  )
  data_partner_birthdate_date = fields.Date(string=_("Birthdate"))
  data_partner_street = fields.Char(string=_("Street"))
  data_partner_zip = fields.Char(string=_("ZIP"))
  data_partner_state_id = fields.Many2one('res.country.state', string=_("State"))
  data_partner_city = fields.Char(string=_("City"))
  data_partner_iban = fields.Char(string=_("IBAN"))
  data_partner_driving_license_expiration_date = fields.Char(string=_("Driving license expiration date"))
  data_partner_image_dni = fields.Char(string=_("DNI image"))
  data_partner_image_driving_license = fields.Char(string=_("Driving license image"))
  data_partner_image_address_certificate = fields.Char(string=_("Address certificate"))

  # FIELDS: COMPLETION
  cs_registration_request_ids = fields.One2many(
    comodel_name='sm_partago_user.carsharing_registration_request',
    inverse_name='related_carsharing_user_request_id',
    string=_("CS registration requests"))

  tariffs_ids = fields.One2many(
    comodel_name='smp.sm_carsharing_tariff',
    inverse_name='related_carsharing_user_request_id',
    string=_("CS tariffs"))

  # COMPUTED FIELDS
  @api.depends('related_member_id')
  def _get_cs_user_type(self):
    for record in self:
      if record.related_member_id:
        record.cs_user_type = record.related_member_id.cs_user_type

  @api.depends('related_member_id')
  def _get_cs_user_status(self):
    for record in self:
      if record.related_member_id:
        record.cs_user_status = record.related_member_id.cs_state

  # WORKFLOW ACTIONS:
  def _set_workflow_status_to(self,workflow_status):
    self.write({
      'workflow_status': workflow_status
    })

  # RESET WORKFLOW ACTION
  @api.multi
  def reset_progressbar_action(self):
    self.write({
      'member_computation_type': 'not_computed',
      'completion_status': 'not_executed',
      'workflow_status': 'new',
      'completed_date': False
    })

  # MEMBER COMPUTE WORKFLOW ACTION
  @api.multi
  def compute_member_progressbar_action(self):
    resources = sm_resources.getInstance()
    if self.workflow_status == 'new':
      error = self._compute_member()
      if error:
        return resources.get_successful_action_message(self,error, self._name)
      self._set_workflow_status_to('member_computed')
    else:
      return resources.get_successful_action_message(self,_('Cannot execute. Status must be "New"'), self._name)

  # returns error
  def _compute_member(self):
    # only enter if no related_member defined. Otherwise advance state.
    if not self.related_member_id:
      # Forcing creation. Must not exists a partner with same email.
      if self.force_partner_creation:
        if self._find_existing_partner_with_same_email():
          return _("Force partner creation not possible. It exists already a partner with same email.")
        else:
          if not self._validate_partner_creation():
            self._create_cs_user_partner_and_link_it_to_request()
            return False
      # Not forced. Find existing.
      if self._valid_fields_for_partner_existing():
        existing_partner = self._find_existing_partner()
        if existing_partner:
          self.write({
            'related_member_id': existing_partner.id,
            'member_computation_type': 'partner_found'
          })
          return False
      # Not existing. Try create one.
        else:
          if not self._validate_partner_creation():
            self._create_cs_user_partner_and_link_it_to_request()
            return False
      else:
        return _("Need at least VAT and Email for member computation")
    # partner already defined setup member_computation_type
    else:
      self.write({
        'member_computation_type': 'partner_found'
      })
    return False

  def _validate_fields_for_partner_creation(self):
    if not self._valid_fields_for_partner_creation():
      return _("No related partner found. Need all contact fields for creating a partner.")
    if not sm_utils.validate_iban(self,self.data_partner_iban):
      return _("No related partner found. Need valid iban for creating a partner.")
    return False

  def _valid_fields_for_partner_existing(self):
    if(
      not self.data_partner_vat or
      not self.data_partner_email
    ):
      return False
    return True

  def _valid_fields_for_partner_creation(self):
    if(
      not self.data_partner_firstname or
      not self.data_partner_lastname or
      not self.data_partner_vat or
      not self.data_partner_email or
      not self.data_partner_mobile or
      not self.data_partner_phone or
      not self.data_partner_birthdate_date or
      not self.data_partner_street or
      not self.data_partner_zip or
      not self.data_partner_state_id or
      not self.data_partner_city or
      not self.data_partner_iban or
      not self.data_partner_driving_license_expiration_date or
      not self.data_partner_image_dni or
      not self.data_partner_image_driving_license
    ):
      return False
    return True

  def _find_existing_partner(self):
    q = str(self.data_partner_vat).replace("-", "").replace(" ", "").upper()
    rel_member_q = self.env['res.partner'].sudo().search([('vat', '=', q)])
    if rel_member_q.exists():
      for rmember in rel_member_q:
        if rmember.email == self.data_partner_email:
          return rmember
      return rel_member_q[0]
    return False

  def _create_cs_user_partner_and_link_it_to_request(self):
    creation_partner = self._create_cs_user_partner()
    self.write({
      'related_member_id': creation_partner.id,
      'member_computation_type': 'partner_new'
    })

  def _create_cs_user_partner(self):
    partner_creation_data = {
      'firstname' : self.data_partner_firstname,
      'lastname' : self.data_partner_lastname,
      'vat' : self.data_partner_vat,
      'email' : self.data_partner_email,
      'mobile' : self.data_partner_mobile,
      'phone' : self.data_partner_phone,
      'gender' : self.data_partner_gender,
      'birthdate_date' : self.data_partner_birthdate_date,
      'street' : self.data_partner_street,
      'zip' : self.data_partner_zip,
      'state_id' : self.data_partner_state_id.id,
      'city' : self.data_partner_city,
      'driving_license_expiration_date' : self.data_partner_driving_license_expiration_date,
      'image_dni' : self.data_partner_image_dni,
      'image_driving_license' : self.data_partner_image_driving_license
    }
    partner = self.env['res.partner'].create(partner_creation_data)
    partner_bank_creation_data = {
      "acc_number": self.data_partner_iban,
      "acc_type": 'iban',
      "partner_id": partner.id,
    }
    partner_bank = self.env['res.partner.bank'].create(partner_bank_creation_data)
    self.write({
      'related_member_id': partner.id
    })
    return partner

  # COMPUTE WORKFLOW ACTION
  @api.multi
  def compute_progressbar_action(self):
    resources = sm_resources.getInstance()
    if self.workflow_status == 'member_computed':
      error = self._compute()
      if error:
        return resources.get_successful_action_message(self,error, self._name)
      self._set_workflow_status_to('computed')
    else:
      return resources.get_successful_action_message(self,_('Cannot execute. Status must be "Member computed"'), self._name)

  # return error
  def _compute(self):
    if self.type == 'elprat_request':
      return self._compute_elprat()
    return _("Request type must be defined.")

  def _compute_elprat(self):
    company = self.env.user.company_id
    # validation
    if not self._valid_cs_user_type():
      return _('Can only compute request if member "Carsharing user type" is "None" or "Regular user"')
    if not self._valid_cs_user_status():
      return _('Can not compute request if member "Carsharing user status" if "Manually Blocked"')
    # Get carsharing groups and carsharing status
    self.related_member_id.set_carsharing_groups()
    # Recompute carsharing status
    self.related_member_id.recompute_cs_registration_info()
    # Add related member to follower
    self.message_subscribe([self.related_member_id.id])
    # Create tariffs
    tariffs = self._create_tariffs_elprat()
    # Check if member has access to general SM.
    if self._has_member_general_membership():
      if self.cs_user_status != 'active':
        # Member with general access and not completed -> Resend registration (registration to SM-general)
        registration_request = self.env['sm_partago_user.carsharing_registration_request'].create({
          'related_member_id': self.related_member_id.id,
          'group_index': company.sm_user_person_group,
          'ba_behaviour': 'update_ba',
          'ba_credits': 1.0E12,
          'related_carsharing_user_request_id': self.id
        })
    else:
      # Member without access -> Resend registration if must (registration to GT)
      registration_request = self.env['sm_partago_user.carsharing_registration_request'].create({
        'related_member_id': self.related_member_id.id,
        # TODO: verify this is the group giving access to cars on elPrat
        'group_index': 'fleet_elprat',
        'ba_behaviour': 'update_ba',
        'ba_credits': 1.0E12,
        'related_carsharing_user_request_id': self.id
      })

  def _valid_cs_user_type(self):
    if self.cs_user_type == 'none' or self.cs_user_type == 'user':
      return True
    return False

  def _valid_cs_user_status(self):
    if self.cs_user_status != 'blocked_banned':
      return True
    return False

  def _has_member_general_membership(self):
    company = self.env.user.company_id
    for membership in self.related_member_id.cs_member_group_ids:
      if membership.related_group_id.name == company.sm_user_person_group:
        return True
    return False

  def _create_tariffs_elprat(self):
    tariff_carconfig_refs = [
      "-NEaGmPikt94k4-tVeMf",
      "-NEaH13UfkepEulYY8MF",
      "-NEaHDv7AALG-9aoqdlo",
      "-NEaGUDMAHpRbKICmhUh",
      "-NEaFhhNSV6PTDz0Sf0q",
      "-NEaG86OLlRidau4UnG4",
      "-NEaoXkb_m9L71oKk_h7",
      "-NEaHS7c6RngxaNL054-"
    ]
    related_tariffs = []
    for carconfig_ref in tariff_carconfig_refs:
      db_carconfig_ids = self.env['smp.sm_car_config'].search([('name','=',carconfig_ref)])
      if db_carconfig_ids.exists():
        tariff = sm_utils.get_create_existing_model(
          self.env['smp.sm_carsharing_tariff'],
          [
            ('tariff_type', '=', 'rel_car'),
            ('related_carconfig_id','=',db_carconfig_ids[0].id),
            ('related_member_id','=',self.related_member_id.id)
          ],
          {
            'name': 'El Prat: Reduced for '+carconfig_ref,
            'reason': 'El Prat registration',
            'date': str(datetime.now()),
            'date_active': str(datetime.now()),
            # TODO: verify which tariff model to use
            'tariff_model_id': 8,
            'related_carconfig_id': db_carconfig_ids[0].id,
            # TODO: Adjust depending on tariff model
            'description': "<p>4€/hora 40€/dia</p>",
            'tariff_type': 'rel_car',
            'related_carsharing_user_request_id': self.id
          }
        )
        if tariff.related_carsharing_user_request_id:
          if tariff.related_carsharing_user_request_id.id == self.id:
            related_tariffs.append(tariff)
    return related_tariffs

  # COMPLETE WORKFLOW ACTION
  @api.multi
  def complete_progressbar_action(self):
    resources = sm_resources.getInstance()
    if self.workflow_status == 'computed':
      # Completion data
      completion_data = {
        'completed_date': str(datetime.now()),
        'completion_status': 'completed',
        'workflow_status': 'completed'
      }
      # Apply Tariffs
      if self.tariffs_ids:
        for tariff in self.tariffs_ids:
          tariff.write({
            'related_member_id': self.related_member_id.id
          })
      # Compute registration requests
      if self.cs_registration_request_ids:
        for registration_request in self.cs_registration_request_ids:
          registration_request.compute_request()
          if registration_request.completed_behaviour == 'error':
            completion_data['completion_status'] = 'error'
      # Write completion data
      self.write(completion_data)
      # Send email to contact
      if completion_data['completion_status'] != 'error':
        # Notify contact El Prat went ok
        sm_utils.send_email_from_template(self, 'elprat_ok_mail_template_id')
      # We could notify admin if we're not manually completing
      # else:
      #   # Notify admin registration failed.
      #   sm_utils.send_email_from_template(self, 'elprat_notok_mail_template_id')
    else:
      return resources.get_successful_action_message(self,_('Cannot execute. Status must be "Computed"'), self._name)

  @api.multi
  def cancell_progressbar_action(self):
    resources = sm_resources.getInstance()
    if self.workflow_status != 'computed' and self.state != 'completed':
      self._set_workflow_status_to('cancelled')
    else:
      return resources.get_successful_action_message(self,_('Cannot execute. Status must not be "Computed" or "Cancelled"'), self._name)