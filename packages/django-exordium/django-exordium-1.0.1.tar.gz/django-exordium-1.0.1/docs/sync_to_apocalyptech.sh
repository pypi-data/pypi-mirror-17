#!/bin/bash
# vim: set expandtab tabstop=4 shiftwidth=4:

rm -rf _build/* && make html && rsync -av _build/html/ pez@apocalyptech.com:/var/www/sites/apocalyptech.com/exordium

