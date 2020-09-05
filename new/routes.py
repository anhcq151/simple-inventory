from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import inspect
from new import newapp, db
from new.forms import *
from new.models import ItemName, Item, Location, itemLocation, transferLog, itemChangeLog
from werkzeug.urls import url_parse
from datetime import datetime, timezone
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired




@newapp.route('/')
@newapp.route('/index')
def index():

    return render_template('index.html', title='Home', Locations=Location, Item=Item, itemLocation=itemLocation, ItemName=ItemName)


@newapp.route('/<asset_name>')
def asset_per_name(asset_name):
    assets = Item.query.filter_by(name=asset_name)

    return render_template('assets_per_name.html', title='Assets list', asset_name=asset_name, assets=assets)


@newapp.route('/asset/<asset_id>')
def asset_view(asset_id):
    selected_item = Item.query.get(asset_id)
    transfer_log = transferLog.query.filter_by(item_id=asset_id)
    change_log = itemChangeLog.query.filter_by(item_id=asset_id)

    return render_template('asset_view.html', title='Asset View', selected_item=selected_item, transfer_log=transfer_log, change_log=change_log, datetime=datetime, timezone=timezone, float=float)


@newapp.route('/asset/<asset_id>/edit', methods=['GET', 'POST'])
def asset_change(asset_id):
    selected_item = Item.query.get(asset_id)
    edit_form = EditItem(
        serial=selected_item.serial, 
        status=selected_item.status, 
        location=selected_item.loc(), 
        description=selected_item.description
    )
    if edit_form.validate_on_submit():
        if edit_form.serial.data == selected_item.serial:
            pass

        elif edit_form.serial.data != selected_item.serial and Item.query.filter_by(serial=edit_form.serial.data).first().id != selected_item.id:
            flash('Serial Number is already existed')

            return redirect(url_for('asset_change', asset_id=asset_id))

        else:
            change_log_serial = itemChangeLog(item_id=asset_id)
            change_log_serial.attrib_name = 'Serial Number'
            change_log_serial.old_value = selected_item.serial
            selected_item.serial = edit_form.serial.data
            change_log_serial.new_value = selected_item.serial
            db.session.add(change_log_serial)

        if edit_form.status.data != selected_item.status:
            change_log_status = itemChangeLog(item_id=asset_id)
            change_log_status.attrib_name = 'Status'
            change_log_status.old_value = selected_item.status
            selected_item.status = edit_form.status.data 
            change_log_status.new_value = selected_item.status
            db.session.add(change_log_status)

        if edit_form.location.data != selected_item.loc():
            _move = itemLocation.query.filter_by(item_id=asset_id).first()
            transfer_log = transferLog(
                    item_id=asset_id, 
                    transfer_from=selected_item.loc().id, 
                    transfer_to=edit_form.location.data.id, 
                    date=datetime.utcnow(), 
                    description=edit_form.transfer_note.data
                )
            _move.loc_id = edit_form.location.data.id
            db.session.add(transfer_log)

        if edit_form.description.data != selected_item.description:
            change_log_description = itemChangeLog(item_id=asset_id)
            change_log_description.attrib_name = 'Description'
            change_log_description.old_value = selected_item.description
            selected_item.description = edit_form.description.data
            change_log_description.new_value = selected_item.description
            db.session.add(change_log_description)
        
        db.session.commit()
        flash('Successfully updated item information!')
        
        return redirect(url_for('asset_view', asset_id=asset_id))

    return render_template('asset_edit.html', title='Edit Item', selected_item=selected_item, edit_form=edit_form, datetime=datetime, timezone=timezone, float=float)


@newapp.route('/new_item', methods=['GET', 'POST'])
def new_item():
    add_new = NewItemForm()
    if add_new.validate_on_submit():
        for i in range(add_new.quantity.data):
            new_asset = Item(
                name=add_new.item_name.data.name, 
                status=add_new.status.data, 
                description=add_new.description.data
            )
            db.session.add(new_asset)
            db.session.commit()
            new_asset_loc = itemLocation(
                item_id=new_asset.id, 
                loc_id=add_new.location.data.id
            )
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
            loc = Location(
                name=new_loc.name.data, 
                description=new_loc.description.data
            )
            db.session.add(loc)
            db.session.commit()
            flash(f'{loc.name} is added successfully!!')

            return redirect(url_for('index'))
        else:
            flash(f'{new_loc.name.data} location name is already existed, please choose another name!!')

            return redirect(url_for('new_location'))

    return render_template('new_loc.html', title='Add new location', new_loc=new_loc)


@newapp.route('/transfer_log')
def transfer_log():
    log = transferLog.query

    return render_template('transfer_log.html', title='Transfer history', log=log, datetime=datetime, timezone=timezone, float=float)
