import json

import requests
from werkzeug import urls
import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ResConfigZaloChat(models.TransientModel):
    _inherit = 'res.config.settings'


    deta_project_key = fields.Char('Deta Project Key', config_parameter='deta.project_key')
    using_deta = fields.Boolean('Using Deta', config_parameter='deta.using')