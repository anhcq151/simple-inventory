from new import newapp, db
from new.models import Item, Location, itemLocation, transferLog, ItemName

@newapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'Item': Item, 'Location': Location, 'itemLocation': itemLocation, 'transferLog': transferLog, 'ItemName': ItemName}