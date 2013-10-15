## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebSubmit Admin configuration parameters."""

__revision__ = \
    "$Id$"

# pylint: disable=C0301

from invenio.config import CFG_SITE_URL

WEBSUBMITADMINURL = "%s/admin/websubmit/websubmitadmin.py" % (CFG_SITE_URL,)
WEBSUBMITADMINURL_OLD = "%s/admin/websubmit" % (CFG_SITE_URL,)

## List of the names of functions for which the parameters are files that can be edited.
## In particular, this applies to the record creation functions that make use of bibconvert.
FUNCTIONS_WITH_FILE_PARAMS = ["Make_Record", "Make_Modify_Record"]
