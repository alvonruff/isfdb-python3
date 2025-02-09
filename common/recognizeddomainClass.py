#
#     (C) COPYRIGHT 2023   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 203 $
#     Date: $Date: 2018-09-12 17:38:34 -0400 (Wed, 12 Sep 2018) $

import cgi
from isfdb import *
from library import XMLescape, XMLunescape
from SQLparsing import SQLGetRecognizedDomainByID


class RecognizedDomain():
        def __init__(self):
                self.used_domain_id = 0
                self.used_domain_name = 0
                self.used_explicit_link_required = 0
                self.used_explicit_link_required_display = 0
                self.used_linking_allowed = 0
                self.used_linking_allowed_display = 0
                self.used_required_segment = 0
                self.used_site_name = 0
                self.used_site_url = 0

                self.domain_id = ''
                self.domain_name = ''
                self.explicit_link_required = 0
                self.explicit_link_required_display = 'No'
                self.linking_allowed = 0
                self.linking_allowed_display = 'No'
                self.required_segment = ''
                self.site_name = ''
                self.site_url = ''

                self.error = ''

        def load(self, record_id):
                if not record_id:
                        self.error = 'No Recognized Domain ID specified.'
                        return
                self.domain_id = record_id
                self.used_domain_id = 1
                record = SQLGetRecognizedDomainByID(self.domain_id)
                if not record:
                        self.error = 'Specified Recognized Domain ID does not exist.'
                        return
                if record[DOMAIN_NAME]:
                        self.domain_name = record[DOMAIN_NAME]
                        self.used_domain_name = 1
                if record[DOMAIN_SITE_NAME]:
                        self.site_name = record[DOMAIN_SITE_NAME]
                        self.used_site_name = 1
                if record[DOMAIN_SITE_URL]:
                        self.site_url = record[DOMAIN_SITE_URL]
                        self.used_site_url = 1
                if record[DOMAIN_LINKING_ALLOWED] is not None:
                        self.linking_allowed = record[DOMAIN_LINKING_ALLOWED]
                        self.used_linking_allowed = 1
                        self.used_linking_allowed_display = 1
                        if self.linking_allowed:
                                self.linking_allowed_display = 'Yes'
                        else:
                                self.linking_allowed_display = 'No'
                if record[DOMAIN_REQUIRED_SEGMENT]:
                        self.required_segment = record[DOMAIN_REQUIRED_SEGMENT]
                        self.used_required_segment = 1
                if record[DOMAIN_EXPLICIT_LINK_REQUIRED] is not None:
                        self.explicit_link_required = record[DOMAIN_EXPLICIT_LINK_REQUIRED]
                        self.used_explicit_link_required = 1
                        self.used_explicit_link_required_display = 1
                        if self.explicit_link_required:
                                self.explicit_link_required_display = 'Yes'
                        else:
                                self.explicit_link_required_display = 'No'

        def cgi2obj(self):
                self.form = cgi.FieldStorage()
                if self.form.has_key('domain_id'):
                        self.domain_id = int(self.form['domain_id'].value)
                        self.used_domain_id = 1
                        if not SQLGetRecognizedDomainByID(self.domain_id):
                                self.error = 'This Recognized Domain ID is not on file'
                                return

                if self.form.has_key('domain_name'):
                        self.domain_name = XMLescape(self.form['domain_name'].value)
                        self.used_domain_name = 1
                else:
                        self.error = 'Recognized Domain Name is a required field'
                        return

                if self.form.has_key('site_name'):
                        self.site_name = XMLescape(self.form['site_name'].value)
                        self.used_site_name = 1
                else:
                        self.error = 'Web Site name is a required field'
                        return

                if self.form.has_key('site_url'):
                        self.site_url = XMLescape(self.form['site_url'].value)
                        self.used_site_url = 1
                else:
                        self.error = 'Web Site URL is a required field'
                        return

                if self.form.has_key('linking_allowed'):
                        self.linking_allowed_display = self._CheckYesNoValue(XMLescape(self.form['linking_allowed'].value),
                                                               'Linking Allowed')
                        if self.error:
                                return
                        if self.linking_allowed_display == 'Yes':
                                self.linking_allowed = '1'
                        else:
                                self.linking_allowed = '0'
                        self.used_linking_allowed = 1
                        self.used_linking_allowed_display = 1
                else:
                        self.error = 'Linking Allowed is a required field'
                        return

                if self.form.has_key('required_segment'):
                        self.required_segment = XMLescape(self.form['required_segment'].value)
                        self.used_required_segment = 1

                if self.form.has_key('explicit_link_required'):
                        self.explicit_link_required_display = self._CheckYesNoValue(XMLescape(self.form['explicit_link_required'].value),
                                                                      'Explicit Credit Page Link Required')
                        if self.error:
                                return
                        if self.used_explicit_link_required_display == 'Yes':
                                self.used_explicit_link_required = '1'
                        else:
                                self.used_explicit_link_required = '0'
                        self.used_explicit_link_required = 1
                        self.used_explicit_link_required_display = 1
                else:
                        self.error = 'Explicit Credit Page Link is a required field'
                        return

        def _CheckYesNoValue(self, value, field_name):
                if value not in ('Yes', 'No'):
                        self.error = 'Yes and No are the only valid values for field %s' % field_name
                        return
                return value
