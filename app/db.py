import couchdb

from app.common import constants


class CouchDB:
    def __init__(self, database_name):
        self.server = couchdb.Server(constants.COUCHDB_URL)
        self.server.resource.credentials = (constants.COUCHDB_USERNAME,
                                            constants.COUCHDB_PASSWORD)
        self.db = self.server[database_name]

    def create_document(self, data):
        doc_id, doc_rev = self.db.save(data)
        return doc_id, doc_rev

    def find(self, selector):
        result = self.db.find(selector)
        return list(result)

    def update_document(self, doc_id, data):
        if not isinstance(data, dict):
            data = data.dict()
        doc = self.get_document(doc_id)
        if doc:
            data['_id'] = doc_id
            data['_rev'] = doc['_rev']
            self.db.save(data)
            return True
        return False

    def get_document(self, doc_id):
        try:
            return self.db[doc_id]
        except couchdb.ResourceNotFound:
            return None