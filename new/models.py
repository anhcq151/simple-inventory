from datetime import datetime
from new import db
from hashlib import md5



class ItemName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    item = db.relationship('Item', backref='Item list', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), db.ForeignKey('item_name.name'))
    serial = db.Column(db.String(64), index=True, unique=True)
    status = db.Column(db.String(32), index=True)
    description = db.Column(db.String(256), index=True)
    import_date = db.Column(db.DateTime, default=datetime.utcnow)
    transfer_log_item = db.relationship('transferLog', foreign_keys='transferLog.item_id', backref='Transfer History', lazy='dynamic')
    change_log_item = db.relationship('itemChangeLog', foreign_keys='itemChangeLog.item_id', backref='Change History', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}\nSerial: {self.serial}\nStatus: {self.status}'

    def loc(self):
        _item_loc_id = itemLocation.query.filter_by(item_id=self.id).first()
        _item_loc_name = Location.query.filter_by(id=_item_loc_id.loc_id).first()
        return _item_loc_name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(256), index=True)
    item_loc = db.relationship('itemLocation', backref='Items in this location', lazy='dynamic')
    transfer_log_from = db.relationship('transferLog', foreign_keys='transferLog.transfer_from', backref='Transfer From History', lazy='dynamic')
    transfer_log_to = db.relationship('transferLog', foreign_keys='transferLog.transfer_to', backref='Transfer To History', lazy='dynamic')

    def __repr__(self):
        return self.name


class itemLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))


class transferLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    transfer_from = db.Column(db.Integer, db.ForeignKey('location.id'))
    transfer_to = db.Column(db.Integer, db.ForeignKey('location.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.String(256), index=True)

    def item_name(self):
        return Item.query.filter_by(id=self.item_id).first().name

    def item_loc(self):
        _loc_id_from = itemLocation.query.filter_by(loc_id=self.transfer_from).first()
        _loc_id_to = itemLocation.query.filter_by(loc_id=self.transfer_to).first()
        return Location.query.filter_by(id=_loc_id_from.loc_id).first().name, Location.query.filter_by(id=_loc_id_to.loc_id).first().name


class itemChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    attrib_name = db.Column(db.String(32))
    old_value = db.Column(db.String(64))
    new_value = db.Column(db.String(64))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)