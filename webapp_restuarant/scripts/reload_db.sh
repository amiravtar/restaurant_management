#!/bin/bash

#run from resturant app with scripts/reaload_db.sh
find . -path '*/migrations/__init__.py' -exec truncate -s 0 {} + -o -path '*/migrations/*' -delete
#rm db.sqlite3
