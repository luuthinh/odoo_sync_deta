# -*- coding:utf-8 -*-

from deta import Deta
from dotty_dict import dotty
from datetime import datetime, date
import uuid
import logging

from odoo import models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SyncDetaMixin(models.AbstractModel):
    _name = 'sync.deta.mixin'

    deta_key = fields.Char(string="Deta Key", readonly=True)
    deta_last_sync = fields.Datetime(string="Deta Last Sync", readonly=True)
    deta_status = fields.Boolean(string="Deta Status", readonly=True)

    # override
    def get_deta_base(self):
        return ''
    
    # Override
    def get_deta_mapping(self):
        return {'id': 'odoo_id'}
    
    def create_key(self):
        return uuid.uuid4().hex    

    def get_deta(self):
        project_key = self.env['ir.config_parameter'].sudo().get_param('deta.project_key', False)
        if not project_key:
            raise UserError('Please config project key.')
        
        base = self.get_deta_base()
        if not base:
            raise UserError('Please override function get_deta_base().')
        
        return Deta(project_key).Base(base)     
      
    def _prepare_sync_deta(self):
        res = dotty()
        mapping = self.get_deta_mapping()

        for k in mapping.keys():
            k_split = k.split('.')
            k_len = len(k_split)
            if k_len == 1:
                if isinstance(self[k], datetime) or isinstance(self[k], date):
                    res[k] = self[k].isoformat()
                else:
                    res[k] = self[k] or None
                continue

            temp = self[k_split[0]]         
            num = 1
            while(temp and num < k_len):
                try:
                    temp = temp[k_split[num]]
                    if not temp:
                        res[k] = None
                        break
                except:
                    break
                num += 1
            if isinstance(self[k], datetime) or isinstance(self[k], date):
                temp = temp.isoformat()
            res[k] = temp or None

        res = res.to_dict()
        set_name = set([(k.split('.')[0], v) for k,v in mapping.items()])
        for k in set_name:
            res[k[1]] = res.pop(k[0])
        return res

    def deta_sync(self):
        self.write({'deta_status': False})
        try:
            deta_base = self.get_deta()
            data_sync = self._prepare_sync_deta()
            new_deta_key = False
            if not self.deta_key:
                new_deta_key = self.create_key()
                data_sync.update({
                    'key': new_deta_key,
                })
                deta_base.put(data_sync)
            else:
                deta_base.update(data_sync, self.deta_key)

            vals = {
                'deta_last_sync': datetime.now(),
                'deta_status': True
            }
            if new_deta_key:
                vals.update({
                    'deta_key': new_deta_key
                })
            self.write(vals)

        except Exception as e:
            _logger.info("Sync deta error %s : %s - %s" % (e, self._name, self.display_name))



