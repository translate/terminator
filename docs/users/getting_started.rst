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

.. warning:: There are required elements in a TBX file and Terminator will not import any unsupported elements. See :ref:`tbx-conformance` for details about required and supported TBX file elements. Prior to the import, some elements that are part of the TBX file must already be created in Terminator, for example, the languages. Otherwise, the import will fail and display an error message. 

Search for Terminology
======================

