from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from ..models import DBSession
from ..models.user import User
from ..models.entry import Entry

@view_config(route_name='home', renderer='pyramid_blogr:templates/index.mako')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = Entry.get_paginator(request, page)
    return {'paginator': paginator}

@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = User.by_name(username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)