#!/bin/bash

flask db init
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - ${FLASK_APP}:newapp