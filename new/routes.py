from flask import render_template, flash, redirect, url_for, request
from new import newapp, db
from new.forms import NewItemForm, NewNameForm, NewLocationForm, TransferItem
from new.models import ItemName, Item, Location, itemLocation, transferLog
from werkzeug.urls import url_parse
from datetime import datetime, timezone
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired




@newapp.route('/')
@newapp.route('/index')
def index():
    all_item = Item.query.filter_by().count()
    item_name = { item.name: Item.query.filter_by(name=item.name).count() for item in ItemName.query.filter_by().all() }
    item_loc = { item.name: itemLocation.query.filter_by(loc_id=item.id).count() for item in Location.query.filter_by().all() }
    locations = { _location.name: _location.id for _location in Location.query }
    return render_template('index.html', title='Home', Locations=Location, Item=Item, itemLocation=itemLocation, ItemName=ItemName)


@newapp.route('/new_item', methods=['GET', 'POST'])
def new_item():
    add_new = NewItemForm()
    if add_new.validate_on_submit():
        for i in range(add_new.quantity.data):
            new_asset = Item(name=add_new.item_name.data.name, status=add_new.status.data, description=add_new.description.data)
            db.session.add(new_asset)
            db.session.commit()
            new_asset_loc = itemLocation(item_id=new_asset.id, loc_id=add_new.location.data.id)
            db.session.add(new_asset_loc)
            db.session.commit()
        flash('Successfully Added new item!!')
        return redirect(url_for('index'))

# Below code block is used for creating items strictly with serial number
#
        # serial_check = Item.query.filter_by(serial=add_new.serial_number.data).first()
        # if serial_check is None:
        #     new_item = Item(name=add_new.item_name.data.name, serial=add_new.serial_number.data, status=add_new.status.data, description=add_new.description.data)
        #     db.session.add(new_item)
        #     db.session.commit()
        #     new_item_loc = itemLocation(item_id=new_item.id, loc_id=add_new.location.data.id)
        #     db.session.add(new_item_loc)
        #     db.session.commit()
        #     flash('Successfully Added new item!!')
        #     return redirect(url_for('index'))
        # else:
        #     flash(f'Item with serial {add_new.serial_number.data} is already existed')
        #     return redirect(url_for('new_item'))
#
# End code block

    return render_template('addnew.html', title='Add new item', add_new=add_new)


@newapp.route('/new_name', methods=['GET', 'POST'])
def new_name():
    new_name = NewNameForm()
    if new_name.validate_on_submit():
        name = ItemName.query.filter_by(name=new_name.name.data).first()
        if name is None:
            name = ItemName(name=new_name.name.data)
            db.session.add(name)
            db.session.commit()
            flash(f'{name.name} is added!')
            return redirect(url_for('index'))
        else:
            flash(f'{new_name.name.data} item name is already existed, please choose another name!')
            return redirect(url_for('new_name'))
    return render_template('new_name.html', title='Add new item name', new_name=new_name)


@newapp.route('/new_location', methods=['GET', 'POST'])
def new_location():
    new_loc = NewLocationForm()
    if new_loc.validate_on_submit():
        loc = Location.query.filter_by(name=new_loc.name.data).first()
        if loc is None:
            loc = Location(name=new_loc.name.data, description=new_loc.description.data)
            db.session.add(loc)
            db.session.commit()
            flash(f'{loc.name} is added successfully!!')
            return redirect(url_for('index'))
        else:
            flash(f'{new_loc.name.data} location name is already existed, please choose another name!!')
            return redirect(url_for('new_location'))
    return render_template('new_loc.html', title='Add new location', new_loc=new_loc)


@newapp.route('/transfer', methods=['GET', 'POST'])
def transfer_item():
    transfer = TransferItem()
    if transfer.validate_on_submit():
        _to_transfer = Item.query.filter_by(name=transfer.item_name.data.name)
        i = 0
        for item in _to_transfer:
            if item.loc() != transfer.transfer_to.data.name:
                _to_move = itemLocation.query.filter_by(item_id=item.id).first()
                transfer_log = transferLog(item_id=item.id, transfer_from=itemLocation.query.filter_by(item_id=item.id).first().loc_id, transfer_to=transfer.transfer_to.data.id, date=datetime.utcnow(), description=transfer.note.data)
                _to_move.loc_id = transfer.transfer_to.data.id
                db.session.add(transfer_log)
                i += 1
                if i >= transfer.quantity.data:
                    break
        db.session.commit()
        flash(f'Moved {transfer.quantity.data} asset to {transfer.transfer_to.data.name}')
        return redirect(url_for('index'))

# Below code block is used for transferring items strictly with serial number
#
        # item_to_transfer = Item.query.filter_by(serial=transfer.item_serial.data).first()
        # if item_to_transfer is not None:
        #     item_new_loc = itemLocation.query.filter_by(item_id=item_to_transfer.id).first()
        #     item_new_loc.loc_id = transfer.transfer_to.data.id
        #     transfer_log = transferLog(item_id=item_to_transfer.id, transfer_from=itemLocation.query.filter_by(item_id=item_to_transfer.id).first().loc_id, transfer_to=item_new_loc.loc_id, date=datetime.utcnow(), description=transfer.note.data)
        #     db.session.add(transfer_log)
        #     db.session.commit()
        #     flash(f'Moved item with serial {item_to_transfer.serial} to {transfer.transfer_to.data.name}')
        #     return redirect(url_for('index'))
        # else:
        #     flash('No item with mentioned serial number')
        #     return redirect(url_for('transfer_item'))
#
# End code block

    return render_template('transfer.html', title='Transfer item', transfer=transfer, Locations=Location, Item=Item, itemLocation=itemLocation, ItemName=ItemName)


@newapp.route('/transfer_log')
def transfer_log():
    log = transferLog.query

    return render_template('transfer_log.html', title='Transfer history', log=log, datetime=datetime, timezone=timezone, float=float)
