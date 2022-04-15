.. _getting-started:

User Roles
==========

Terminator has six different user roles with increasing permissions (each role
inherits previous role permissions):

- *Anonymous user*: users that are not authenticated.
- *Authenticated user*: users authenticated but without any permission on any
  glossary.
- Terminologist: users that can add and manage terms.
- Lexicographer: users that can proofread terms.
- Glossary owner: users that have all permissions on a specific glossary.
- Server administrator: users with all permissions.

How Terminator Handles Terminology
==================================

Terminator encloses all terminology in glossaries. Terminology is managed in a
concept-centric way, allowing several terms for each concept, even for the same
language.

Export
======

Export to TBX
-------------

Terminator can export to a subset of the ISO 30042 TermBase eXchange (TBX) standard. See :ref:`tbx-conformance` for more details.

Import
======

Import from TBX
---------------

Terminator can import from a subset of the ISO 30042 TermBase
eXchange (TBX) standard. See :ref:`tbx-conformance` for details.

.. warning:: Some elements in the TBX file, for example the languages, must already be created in Terminator prior to the import, otherwise the import will fail and display an error message.

.. warning:: Some required elements must be present in the TBX file. And, Terminator will not import any other elements (beside the supported elements) available in the TBX file See :ref:`tbx-conformance` for details on the required and supported elements.

Search for Terminology
======================

