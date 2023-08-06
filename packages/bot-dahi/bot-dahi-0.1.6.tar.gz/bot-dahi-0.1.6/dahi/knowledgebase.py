from bson import ObjectId
from dahi import getDB
from dahi.document import Document
from dahi.statement import Statement


class KnowledgeBase(object):

    def __init__(self, storageEngine, id):
        self.id = id
        self.docs = []
        self.db = storageEngine["docs"]

    def getAll(self):
        return (Document.generate(i) for i in self.db.find())

    def get(self, docID):
        data = self.db.findOne({"_id": ObjectId(docID)})
        return Document.generate(data)

    def insert(self, doc):
        self.db.insert(doc.toDB())

    def update(self, doc):
        self.db.update(
            {"_id": ObjectId(doc.id)},
            doc.toDB())

    def remove(self, doc=None, docID=None):
        if doc:
            docID = doc.id
        elif not docID:
            raise AttributeError("neither document itself or its id is given")
        self.db.remove({"_id": docID})

    def truncate(self):
        self.db.remove()

    def count(self):
        return self.db.count()
