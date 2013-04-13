.. _getting-started:

User Roles
==========

Terminator has six different user roles with increasing permissions (each role
inherits previous role permissions):

- *Anonymous user*: those users that are not authenticated.
- *Authenticated user*: users authenticated but without any permission on any
  glossary.
- Terminologist: 
- Lexicographer: 
- Glossary owner: 
- Server administrator: 


How Terminator Handles Terminology
==================================

Terminator encloses all terminology in glossaries. Terminology is managed in a
concept-centric way, allowing several terms for each concept, even for the same
language.



Export
======

Export to TBX
-------------

Terminator is capable of exporting to a subset of the ISO 30042 TermBase
eXchange (TBX) standard. See :ref:`tbx-conformance` for more details.




Import
======

Import from TBX
---------------

Terminator is capable of importing from a subset of the ISO 30042 TermBase
eXchange (TBX) standard. See :ref:`tbx-conformance` for more details.




.. warning:: Terminator assumes that some elements that are used in the TBX
   file, for example the languages, are already created in Terminator. If
   those elements don't exist in Terminator then the import will fail showing
   an error message.

.. warning:: Terminator assumes that some required elements are present in the
   TBX file, thus if those elements are not present then the import process
   will fail showing an error message. See :ref:`tbx-conformance` for more
   details on the required elements.

.. note:: If any other element, besides the supported by Terminator ones, is
   present in the TBX file Terminator won't import those, but the importing
   process won't fail. See :ref:`tbx-conformance` for more details on which are
   the supported elements.



Search for Terminology
======================



