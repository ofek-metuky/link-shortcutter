import re
import typing

from link_shortcutter import config
from link_shortcutter.models import LinkItem
from pymongo import mongo_client


def _get_mongo_client():
    return mongo_client.MongoClient(config.mongo_url)


class DbWrapper:
    def __init__(self):
        self._client = _get_mongo_client()

    def __enter__(self):
        if self._client is None:
            self._client = _get_mongo_client()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
        self._client = None

    @property
    def _db(self):
        return self._client.get_database(config.db_name)

    @property
    def _links_collection(self):
        return self._db.get_collection(config.links_collection_name)

    def query_links(self, **query) -> typing.Iterable[LinkItem]:
        results = self._links_collection.find(query)
        for result in results:
            link_item = LinkItem(**result)
            yield link_item

    def get_links(self, short_name: typing.Union[str, re.Pattern]) -> typing.Iterable[str]:
        for link_item in self.query_links(short_name=short_name):
            yield from link_item.links

    def get_similar_links(self, short_name: str) -> typing.Iterable[str]:
        yield from self.get_links(re.compile(f".*{short_name}.*", re.IGNORECASE))

    def get_all_links(self):
        yield from self.query_links()

    def add_link(self, link_item: LinkItem):
        self._links_collection.insert_one(document=link_item.dict())

    def update_link(self, link_item: LinkItem):
        self._links_collection.update(spec=dict(short_name=link_item.short_name),
                                      document=link_item.dict())

    def delete_link(self, short_name):
        self._links_collection.delete_one(filter=dict(short_name=short_name))
