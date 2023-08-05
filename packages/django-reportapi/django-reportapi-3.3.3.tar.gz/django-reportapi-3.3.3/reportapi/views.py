# -*- coding: utf-8 -*-
#
#   Copyright 2014-2015 Grigoriy Kramarenko <root@rosix.ru>
#
#   This file is part of ReportAPI.
#
#   ReportAPI is free software: you can redistribute it and/or
#   modify it under the terms of the GNU Affero General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   ReportAPI is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public
#   License along with ReportAPI. If not, see
#   <http://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals
import logging

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from quickapi.http import tojson

from reportapi.conf import (REPORTAPI_VIEW_PRIORITY,
    REPORTAPI_DOWNLOAD_PRIORITY, REPORTAPI_LOGGING as LOGGING)
from reportapi.models import Document
from reportapi.sites import site

DOCS_PER_PAGE = 25

def _default_context(request):
    ctx = {}
    ctx['sections'] = site.get_sections(request)
    docs = Document.objects.permitted(request).all()
    ctx['docs'] = docs[:DOCS_PER_PAGE]
    return ctx


@login_required
def index(request):
    ctx = _default_context(request)
    return render(request, 'reportapi/index.html', ctx)

@login_required
def report_list(request, section):
    ctx = _default_context(request)
    if not section in site.sections:
        if LOGGING:
            logger = logging.getLogger('reportapi.views.report_list')
            logger.warning(force_text(_('Section (%s) not found.') % section))

        return render(request, 'reportapi/404.html', ctx)

    ctx['section'] = site.sections[section]

    docs = Document.objects.permitted(request).all()
    docs = docs.filter(register__section=section)
    ctx['docs'] = docs[:DOCS_PER_PAGE]

    ctx['reports'] = site.sections[section].get_reports(request)

    return render(request, 'reportapi/report_list.html', ctx)

@login_required
def documents(request, section=None, name=None):
    """
    Returns inner html with founded documents
    """
    ctx = _default_context(request)

    docs = Document.objects.permitted(request).all()

    if section:
        ctx['section'] = site.sections.get(section, None)
        if not ctx['section'] or not ctx['section'].has_permission(request):
            if LOGGING:
                logger = logging.getLogger('reportapi.views.documents')
                logger.error(force_text(_('Section (%s) not found or not allowed.') % section))

            return render(request, 'reportapi/404.html', ctx)
        docs = docs.filter(register__section=section)

    if section and name:
        report, register = site.get_report_and_register(request, section, name)
        if not report or not register:
            if LOGGING:
                logger = logging.getLogger('reportapi.views.documents')
                logger.error(force_text(_('Report or register not found for section (%s).') % section))

            return render(request, 'reportapi/404.html', ctx)
        ctx['report'] = report
        docs = docs.filter(register__name=name)

    ctx['docs'] = docs[:DOCS_PER_PAGE]

    return render(request, 'reportapi/index.html', ctx)

@login_required
def report(request, section, name):
    ctx = _default_context(request)
    report, register = site.get_report_and_register(request, section, name)
    if not report or not register:
        if LOGGING:
            logger = logging.getLogger('reportapi.views.report')
            logger.error(force_text(
                _('Report or register not found for section (%(section)s) and name (%(name)s).')
                % {'section': section, 'name': name}
            ))
        return render(request, 'reportapi/404.html', ctx)

    ctx['report_as_json'] = tojson(report.get_scheme(request) or dict())
    ctx['report']  = report
    ctx['filters_list'] = report.filters_list(request)
    ctx['section'] = site.sections[section]

    return render(request, 'reportapi/report.html', ctx)

@login_required
def view_document(request, pk, format=None):
    ctx = _default_context(request)
    try:
        doc = Document.objects.permitted(request).get(pk=pk)
    except Exception as e:
        if LOGGING:
            logger = logging.getLogger('reportapi.views.view_document')
            logger.error(force_text(_('Document (%s) not found or not allowed.') % pk))

        ctx['remove_nav'] = True
        return render(request, 'reportapi/404.html', ctx)
    if doc.error:
        return HttpResponse(doc.error)

    if not format:
        for p in REPORTAPI_VIEW_PRIORITY:
            if getattr(doc, 'has_view_%s' % p, False):
                url = getattr(doc, '%s_url' % p, None)
                if url:
                    return HttpResponseRedirect(url)

    elif format in ('html', 'pdf'):
        if getattr(doc, 'has_view_%s' % format, False):
            url = getattr(doc, '%s_url' % format, None)
            if url:
                return HttpResponseRedirect(url)

    ctx['remove_nav'] = True

    return render(request, 'reportapi/404.html', ctx)

@login_required
def download_document(request, pk, format=None):
    ctx = _default_context(request)
    try:
        doc = Document.objects.permitted(request).get(pk=pk)
    except Exception as e:
        if LOGGING:
            logger = logging.getLogger('reportapi.views.download_document')
            logger.error(force_text(_('Document (%s) not found or not allowed.') % pk))

        ctx['remove_nav'] = True
        return render(request, 'reportapi/404.html', ctx)
    if doc.error:
        return HttpResponse(doc.error)

    if not format:
        for p in REPORTAPI_DOWNLOAD_PRIORITY:
            if getattr(doc, 'has_download_%s' % p, False):
                url = getattr(doc, '%s_url' % p, None)
                if url:
                    return HttpResponseRedirect(url)

    elif format in ('pdf', 'odf', 'xml'):
        if getattr(doc, 'has_download_%s' % format, False):
            url = getattr(doc, '%s_url' % format, None)
            if url:
                return HttpResponseRedirect(url)

    ctx['remove_nav'] = True

    return render(request, 'reportapi/404.html', ctx)

