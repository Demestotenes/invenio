## This file is part of Invenio.
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011 CERN.
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

"""Invenio Submission Web Interface config file."""

__revision__ = "$Id$"

import re

## test:
test = "FALSE"

## CC all action confirmation mails to administrator? (0 == NO; 1 == YES)
CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN = 0

## During submission, warn user if she is going to leave the
## submission by following some link on the page?
## Does not work with Opera and Konqueror.
## This requires all submission functions to set Javascript variable
## 'user_must_confirm_before_leaving_page' to 'false' before
## programmatically submitting a form , or else users will be asked
## confirmation after each submission step.
## (0 == NO; 1 == YES)
CFG_WEBSUBMIT_CHECK_USER_LEAVES_SUBMISSION = 0

## List of keywords/format parameters that should not write by default
## corresponding files in submission directory (`curdir').  Some other
## filenames not included here are reserved too, such as those
## containing non-alphanumeric chars (excepted underscores '_'), for
## eg all names containing a dot ('bibdocactions.log',
## 'performed_actions.log', etc.)
CFG_RESERVED_SUBMISSION_FILENAMES = ['SuE',
                                     'files',
                                     'lastuploadedfile',
                                     'curdir',
                                     'function_log',
                                     'SN',
                                     'ln']

## Prefix for video uploads, Garbage Collector
CFG_WEBSUBMIT_TMP_VIDEO_PREFIX = "video_upload_"
