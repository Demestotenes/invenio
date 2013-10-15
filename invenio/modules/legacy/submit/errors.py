## This file is part of Invenio.
## Copyright (C) 2013 CERN.
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

"""
    invenio.modules.submit.errors
    ---
    Exceptions for Invenio Submit module.
"""


# WebSubmitAdmin exceptions
class InvenioWebSubmitAdminWarningIOError(Exception):
    pass


class InvenioWebSubmitAdminWarningNoUpdate(Exception):
    """Exception used when a no update was made as a result of an action"""
    pass


class InvenioWebSubmitAdminWarningDeleteFailed(Exception):
    pass


class InvenioWebSubmitAdminWarningInsertFailed(Exception):
    pass


class InvenioWebSubmitAdminWarningTooManyRows(Exception):
    pass


class InvenioWebSubmitAdminWarningNoRowsFound(Exception):
    pass


class InvenioWebSubmitAdminWarningReferentialIntegrityViolation(Exception):
    pass


# WebSubmit exceptions
class InvenioWebSubmitWarning(Exception):
    """A generic warning for WebSubmit."""
    def __init__(self, message):
        """Initialisation."""
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)


class InvenioWebSubmitFunctionError(Exception):
    """This exception should only ever be raised by WebSubmit functions.
       It will be caught and handled by the WebSubmit core itself.
       It is used to signal to WebSubmit core that one of the functions
       encountered a FATAL ERROR situation that should all further execution
       of the submission.
       The exception will carry an error message in its "value" string. This
       message will probably be displayed on the user's browser in an Invenio
       "error" box, and may be logged for the admin to examine.

       Again: If this exception is raised by a WebSubmit function, an error
              message will displayed and the submission ends in failure.

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - an error string to display to the user.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitFunctionStop(Exception):
    """This exception should only ever be raised by WebSubmit functions.
       It will be caught and handled by the WebSubmit core itself.
       It is used to signal to WebSubmit core that one of the functions
       encountered a situation that should prevent the functions that follow
       it from being executed, and that WebSubmit core should display some sort
       of message to the user. This message will be stored in the "value"
       attribute of the object.

       ***
       NOTE: In the current WebSubmit, this "value" is ususally a JavaScript
             string that redirects the user's browser back to the Web form
             phase of the submission. The use of JavaScript, however is going
             to be removed in the future, so the mechanism may change.
       ***

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to display to the user.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitFunctionWarning(Exception):
    """This exception should be raised by a WebSubmit function
       when unexpected behaviour is encountered during the execution
       of the function. The unexpected behaviour should not have been
       so serious that execution had to be halted, but since the
       function was unable to perform its task, the event must be
       logged.
       Logging of the exception will be performed by WebSubmit.

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to write to the log.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitFileStamperError(Exception):
    """This exception should be raised by websubmit_file_stamper when an
       error is encoutered that prevents a file from being stamped.
       When caught, this exception should be used to stop processing with a
       failure signal.

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to write to the log.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitIconCreatorError(Exception):
    """This exception should be raised by websubmit_icon_creator when an
       error is encoutered that prevents an icon from being created.
       When caught, this exception should be used to stop processing with a
       failure signal.

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to write to the log.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitFileMetadataRuntimeError(Exception):
    """This exception should be raised by websubmit_file_metadata plugins when an
       error is encoutered that prevents a extracting/updating a file.
       When caught, this exception should be used to stop processing with a
       failure signal.

       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to write to the log.
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)
