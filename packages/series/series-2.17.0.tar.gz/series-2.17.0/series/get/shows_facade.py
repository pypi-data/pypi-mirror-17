import re

from series.get.model.show import Show

from amino import Maybe
from series import canonicalize
from series.get.tvdb import Tvdb

from series.db_facade import DbFacade, exclusive, commit


class ShowsFacade(Tvdb, DbFacade):

    @property
    def main_type(self):
        return Show

    @exclusive
    def name_exists(self, name):
        return self.filter_by(canonical_name=canonicalize(name)).count() > 0

    def id_param(self, showid):
        return (dict(etvdb_id=showid) if self.use_etvdb else
                dict(rage_id=showid))

    @exclusive
    def add(self, name, show):
        data = dict(
            name=show.name,
            canonical_name=canonicalize(name)
        )
        data.update(**self.id_param(show.showid))
        if show.latest_episode is not None:
            data.update(latest_episode=show.latest_episode.number,
                        latest_season=show.latest_episode.season)
        self._db.add(Show(**data))

    @commit
    def update(self, id_, data):
        query = self.filter_by(id=id_)
        if query.count() > 0:
            show = query.first()
            for key, value in data.items():
                setattr(show, key, value)
            return show
        else:
            self.log.debug(
                'Tried to update nonexistent show with id {}'.format(id_)
            )

    @commit
    def delete_by_sid(self, showid):
        query = self.filter_by(**self.id_param(showid))
        if query.count() > 0:
            show = query.first()
            self._db.delete(show)
        else:
            self.log.debug(
                'Tried to delete nonexistent show with id {}'.format(showid)
            )

    @commit
    def delete(self, showid):
        query = self.filter_by(id=showid)
        if query.count() > 0:
            show = query.first()
            self._db.delete(show)
        else:
            self.log.debug(
                'Tried to delete nonexistent show with id {}'.format(showid)
            )

    @property  # type: ignore
    @exclusive
    def all(self):
        return self.filter_by().all()

    def filter_by_regex(self, regex):
        r = re.compile(regex)
        return filter(lambda s: r.search(s.canonical_name), self.all)

    @exclusive
    def find_by_name(self, name):
        return Maybe(self.filter_by(canonical_name=name).first())

__all__ = ['ShowsFacade']
