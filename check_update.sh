#!/bin/sh
curl -L https://packages.sogo.nu/sources/ 2>/dev/null |grep 'href="SOPE-' |sed -e 's,.*>SOPE-,,;s,\.tar.*,,' |grep '^[0-9.]*$' |sort -V |tail -n 1
