import os
import re
import json
import traceback
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import base64

from django.http import QueryDict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.urls import reverse, resolve
from django.conf.urls import url, include

import s3fs
import gcsfs

from users.decorators import log_activity
from dashboard.lib import log_app_activity

from enrichsdk.utils import SafeEncoder
from enrichapp.spec import validate_spec as default_validate_spec, fill_action_gaps
from enrichsdk.lib import get_credentials_by_name
from enrichsdk.utils import SafeEncoder
from enrichsdk.datasets import Doodle

logger= logging.getLogger('app')


###############################################
# Main class
###############################################
class AppBase():
    """
    A shareable view across apps
    """

    def __init__(self):
        self.name = "singlepageapp"
        self.verbose_name = "Single Page App"
        self.category = "singlepageapp"
        self.templates = {
            'index': f'enrichapp/singlepageapp/index.html',
            'helper': f'enrichapp/singlepageapp/helper.html',
        }

    def __str__(self):
        return f"[{self.name}] {self.verbose_name}"

    def get_template(self, spec, name):
        return spec.get('templates',{}).get(name, self.templates[name])

    def get_model(self, spec, name):

        from enrichapp.dashboard.globalapp import lib as globallib

        if (('models' in spec) and (name in spec['models'])):
            return spec['models'][name]

        raise Exception("Not implemented")

    def get_form(self, spec, name):

        from enrichapp.dashboard.globalapp import lib as globallib

        if (('forms' in spec) and (name in spec['forms'])):
            return spec['forms'][name]

        raise Exception("Not implemented")        

    def validate_spec(self, spec):

        fill_action_gaps(spec, context={ })

        errors = default_validate_spec(spec)
        if len(errors) > 0:
            return len(errors) == 0, errors

        return len(errors) == 0, errors

    def check_prerequisites(self, request, spec):

        valid, errors = self.validate_spec(spec)
        if not valid:
            error = "Invalid specification"
            messages.error(request, error)
            msg = "Errors: " + json.dumps(errors, indent=4, cls=SafeEncoder)
            msg += "Spec:\n" + json.dumps(spec,  indent=4, cls=SafeEncoder)

            logger.error(error,
                         extra={
                             'transform': 'Dashboard',
                             'data': msg
                         })
            return valid, HttpResponseRedirect(reverse('dashboard:application_index'))

        return valid, None

    def get_urlpatterns(self):
        urlpatterns = [
            url('^[/]?$', self.index, name="index"),
        ]

        return urlpatterns


    def get_fs_handle(self, cred):
        """
        Get s3/gcs filesystem handle..
        """
        cred = get_credentials_by_name(cred)
        nature = cred['nature']
        if nature not in ['s3', 'gcs']:
            raise Exception(f"Unknown credentials: {nature}")

        if nature == 's3':
            config_kwargs={
                'signature_version': 's3v4'
            }

            if 'region' in cred:
                config_kwargs['region_name'] = cred['region']

            fshandle = s3fs.S3FileSystem(
                key    = cred['access_key'],
                secret = cred['secret_key'],
                config_kwargs=config_kwargs,
                use_listings_cache=False
            )
        else:
            fshandle = gcsfs.GCSFileSystem(
                token=cred['keyfile']
            )

        return fshandle

    def get_data(self, request, spec):

        try:
            data = {
                "test": "This is test data"
            }

        except:
            logger.exception(f"Error in accessing {spec['name']} results")

        return data

    @log_activity("app_index", nature="application")
    def index(self, request, spec):

        r = resolve(request.path)

        valid, redirect = self.check_prerequisites(request, spec)
        if not valid:
            return redirect

        usecase = spec['usecase']

        template = self.get_template(spec, 'index')
        helper = self.get_template(spec, 'helper')

        try: 
            data = self.get_data(request, spec)
        except:
            logger.exception("Unable to read data")
            messages.error(request, "Unable to read data. See log")
            return HttpResponseRedirect(reverse('dashboard:application_index'))

        return render(request,
                      template,
                      {
                          'app': self,
                          'spec': spec,
                          'usecase': usecase,
                          'basenamespace': r.namespace,
                          'data': data,
                          'helper': helper
                      })

    
    def get_router(self):

        from ninja import Router, Query, Schema

        router = Router()

        # Nothing to do...
        return router
