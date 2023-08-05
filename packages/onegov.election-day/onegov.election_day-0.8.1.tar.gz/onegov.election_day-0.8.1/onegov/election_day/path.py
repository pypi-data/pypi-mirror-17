from onegov.core.i18n import SiteLocale
from onegov.ballot import Election, ElectionCollection
from onegov.ballot import Ballot, BallotCollection
from onegov.ballot import Vote, VoteCollection
from onegov.election_day import ElectionDayApp
from onegov.election_day.models import Archive, Principal
from onegov.user import Auth


@ElectionDayApp.path(model=Auth, path='/auth')
def get_auth(request, to='/'):
    return Auth.from_request(request, to)


@ElectionDayApp.path(model=Principal, path='/')
def get_principal(app):
    return app.principal


@ElectionDayApp.path(model=ElectionCollection, path='/manage/elections')
def get_manage_elections(app, page=0):
    return ElectionCollection(app.session(), page=page)


@ElectionDayApp.path(model=VoteCollection, path='/manage/votes')
def get_manage_votes(app, page=0):
    return VoteCollection(app.session(), page=page)


@ElectionDayApp.path(model=Election, path='/election/{id}')
def get_election(app, id):
    return ElectionCollection(app.session()).by_id(id)


@ElectionDayApp.path(model=Vote, path='/vote/{id}')
def get_vote(app, id):
    return VoteCollection(app.session()).by_id(id)


@ElectionDayApp.path(model=Ballot, path='/ballot/{id}')
def get_ballot(app, id):
    return BallotCollection(app.session()).by_id(id)


@ElectionDayApp.path(model=Archive, path='/archive/{date}')
def get_archive_by_year(app, date):
    return Archive(app.session(), date)


@ElectionDayApp.path(model=SiteLocale, path='/locale/{locale}')
def get_locale(request, app, locale, to=None):
    to = to or request.link(app.principal)
    return SiteLocale.for_path(app, locale, to)
