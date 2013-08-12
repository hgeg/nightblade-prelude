#!/bin/bash
if [ -f database.db ]; then
      rm database.db
fi
python manage.py syncdb < yes
python manage.py shell --plain < pyinit
