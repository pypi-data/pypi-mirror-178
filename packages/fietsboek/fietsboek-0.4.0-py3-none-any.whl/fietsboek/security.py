"""Module implementing the user authentication."""
from pyramid.security import Allowed, Denied
from pyramid.authentication import SessionAuthenticationHelper
from pyramid.authorization import ACLHelper, Everyone, Authenticated
from pyramid.traversal import DefaultRootFactory

from sqlalchemy import select

from . import models


ADMIN_PERMISSIONS = {'admin'}


class SecurityPolicy:
    """Implementation of the Pyramid security policy."""
    def __init__(self):
        self.helper = SessionAuthenticationHelper()

    def identity(self, request):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.identity`"""
        userid = self.helper.authenticated_userid(request)
        if userid is None:
            return None

        query = select(models.User).filter_by(id=int(userid))
        return request.dbsession.execute(query).scalar_one_or_none()

    def authenticated_userid(self, request):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.authenticated_userid`"""
        identity = self.identity(request)
        if identity is None:
            return None
        return str(identity.id)

    def permits(self, request, context, permission):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.permits`"""
        identity = self.identity(request)
        # If the context is not there, we are on a static site that does not use ACL
        if isinstance(context, DefaultRootFactory):
            if identity is None:
                return Denied('User is not signed in.')
            if permission not in ADMIN_PERMISSIONS:
                return Allowed('User is signed in.')
            if identity.is_admin:
                return Allowed('User is an administrator.')
            return Denied('User is not an administrator.')

        # If the context is there, use ACL
        principals = [Everyone]
        if identity is not None:
            principals.append(Authenticated)
            principals.extend(identity.principals())

        if 'secret' in request.GET:
            principals.append(f'secret:{request.GET["secret"]}')

        return ACLHelper().permits(context, principals, permission)

    def remember(self, request, userid, **kw):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.remember`"""
        return self.helper.remember(request, userid, **kw)

    def forget(self, request, **kw):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.forget`"""
        return self.helper.forget(request, **kw)
