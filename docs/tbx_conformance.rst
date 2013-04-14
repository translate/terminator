.. _tbx-conformance:

TBX Conformance
===============

ISO 30042 TermBase eXchange (TBX) is the `LISA OSCAR standard
<http://www.gala-global.org/lisa-oscar-standards>`_ for terminology exchange.
Terminator has partial support for the features in this format.


.. _tbx_conformance#references:

References
++++++++++

* `Standard home page <http://www.gala-global.org/lisa-oscar-standards>`_
* `Specification
  <http://www.gala-global.org/oscarStandards/tbx/tbx_oscar.pdf>`_
* `ISO 30042
  <http://www.iso.org/iso/iso_catalogue/catalogue_tc/catalogue_detail.htm?csnumber=45797>`_
  -- TBX is an approved ISO standard
* `Additional TBX resources <http://www.tbxconvert.gevterm.net/>`_

You might also be interested in reading about `TBX-Basic
<http://www.gala-global.org/oscarStandards/tbx/tbx-basic.html>`_ -- a simpler,
reduced version of TBX with most of the useful features included.

Also you might want to use `TBXChecker
<http://sourceforge.net/projects/tbxutil/>`_ in order to check that TBX files
are valid. Check the `TBXChecker explanation
<http://www.tbxconvert.gevterm.net/tbx_checker_explanation.html>`_.


.. _tbx_conformance#terminator_tbx_specification:

Terminator TBX specification
++++++++++++++++++++++++++++

The original Terminator TBX support is derived from the Galician Free Software
Translation Group `Proxecto Trasno <http://www.trasno.net/>`_ needs on
terminology for helping on its translation works.

TBX stores the terminology data by grouping it in concepts. Within each concept
the data is stored using a three leve structure:

* concept level,
* language level and
* translation level (also called term level).

In concept level only goes data data specific to the concept but that doesn't
belong to any particular language. In language level it goes data that is
specific to a given language but not tied to a particular term. Language level
is under concept level. Finally in term level goes all data specific to a given
term. This level is under language level.

Below you can see a diagram that depicts the level structure and the data that
goes in each level.

.. image:: /_static/TBX_termEntry_structure.png

Next you can see a list of the items and the tag chosen for representing each
item, telling the level where the tag goes:

* **Glossary name:** the glossary name is the TBX file title, which is
  represented using the label `<title>`. It goes on the file header.

* **Glossary description:** Terminator exports the glossary description inside a
  `<p>` tag enclosed in the `<sourceDesc>` tag. It goes on the file header.

* **Concept:** the `<termEntry>` tag from TBX standard represents a concept.
  The `<termEntry>` tag encloses the concept level.

  * **Concept identifier:** the `<termEntry>` tag has an attribute named `"id"`.

    .. code-block:: xml

      <termEntry id="cid-11">

    .. note:: When exporting Terminator uses the format `"cid-NNNN"` for concept
       ids where `NNNN` is replaced by an unique number. `cid` is short for
       *concept identifier*.


* **Concept subject field:** the TBX standard defines the `<descrip>` tag with
  `"subjectField"` value in its `"type"` attribute to represent the concept
  subject field. It goes in concept level. Example of how TBX says to do this:

    .. code-block:: xml

      <descrip type="subjectField">subject field name</descrip>

  Despite this, Terminator handles the subject field as another concept in the
  same glossary. So when exporting it uses a `<descripGrp>` tag which wraps a
  `<descrip>` tag like in the above example, but also a `<ref>` tag pointing at
  the subject field concept. It goes in concept level.

    .. code-block:: xml

      <descripGrp>
          <descrip type="subjectField">firewall</descrip>
          <ref type="crossReference" target="cid-2342"></ref>
      </descripGrp>

  .. note:: The lack of a way in TBX standard to refer to another concept within
     the same glossary as subject field to make self-contained glossaries is a
     real problem.

  .. warning:: Terminator doesn't export the subject field exactly how the TBX
     specification tells to do.


* **Related concepts:** the TBX standard suggest the use of the `<ref>` tag with
  `type="crossReference"` having a `"target"` attribute whose value is the id of
  the related concept. The text between the opening and closing `<ref>` tags is
  one of the related concept translations (the first english recommended one,
  for example). It goes on concept level.

  .. code-block:: xml

    <ref type="crossReference" target="cid­23">some text...</ref>


* **Broader concept:** TBX defines the use of the tag `<descrip>` with the value
  `"broaderConceptGeneric"` in its `"type"` attribute and a text between its
  opening and closing tags. Also it allows the use of the `"target"` attribute
  to refer to the broader concept. It goes on concept level.

  .. code-block:: xml

    <descrip type="broaderConceptGeneric" target="cid­23">broader concept name</descrip>


* **Language:** in TBX the `<langSet>` tag represents a language, but no
  language list is stored inside the TBX file. So if there is a `<langSet>` tag
  for a given language somewhere inside the TBX file, then this particular
  language is defined in that TBX file. Inside each concept only can exist one
  `<langSet>` per language, but a given language can have a `<langSet>` in each
  `<termEntry>`. It is essential that at least one `<langSet>` tag is present in
  every `<termEntry>` tag. The `<langSet>` tag encloses the language level. It
  goes on concept level.

  * **Language code:** the `<langSet>` tag has an attribute named `"xml:lang"`
    which stores some `ISO 639 code
    <http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ value.

    .. code-block:: xml

      <langSet xml:lang="gl">

    .. note:: Language codes like `en-US` (`IETF language tag
       <http://en.wikipedia.org/wiki/IETF_language_tag>`_) can be used. You just
       have to add to Terminator languages which use that codes. This is so
       because Terminator actually doesn't check the format of the language
       code, but it is recommended to use `ISO 639 language codes
       <http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.


* **Definition:** to save the definitions it should be used the `<descrip>` tag
  with the value `"definition"` in its "type" attribute. It goes on the language
  level.

  * **Definition text:** the definition text goes between the opening and
    closing `<descrip>` tags.

    .. code-block:: xml

      <!-- This can be the definition for "nickname". -->
      <descrip type="definition">alternate name for a person...</descrip>


  * **Definition source:** Optionally Terminator allows to provide a source for
    the definition. When a definition has a source it is exported using a
    `<descripGrp>` tag that wraps the `<descrip>` tag for the definition, and a
    `<xref>` tag with with `"xSource"` in its `"type"` attribute and an URL on
    its `"target"` attribute pointing at the source in an external location and
    a descriptive text between the opening and closing `<xref>` tags.

    .. code-block:: xml

      <!-- This can be the definition for the "tab" GUI element. -->
      <descripGrp>
        <descrip type="definition">Definition for tab...</descrip>
        <xref type="xSource" target="http://en.wikipedia.org/wiki/Tab_(GUI)">English Wikipedia page.</xref>
      </descripGrp>

    .. note:: Note that when a definition has a source Terminator exports it in
       a different way in order to attach the source data to the definition.


* **Link to external reference:** according to TBX standard the tag that defines
  external links to outside the current file is the `<xref>` tag. This tag has a
  `"type"` attribute indicating the link type, a `"target"` attribute holding
  the link address and a short description text between the opening and closing
  tags. It goes on language level.

  * **Link type:** the `<xref>` tag has an attribute named `"type"` that defines
    the link type. This attribute can have the values `"xGraphic"` if it is an
    image, `"externalCrossReference"` if it is a link to an external resource
    (for example a link to Wikipedia). Another used value is `"xSource"` but not
    for this kind of links to external references, but for pointing at the
    source for another data, e.g. a definition.

  * **Link address:** the `<xref>` tag has an attribute named `"target"` which
    holds the link address.

  * **Link description:** the link description goes between the opening and
    closing `<xref>` tags.

  .. code-block:: xml

    <!-- Links to external references. One language can have several. -->
    <xref type="xGraphic" target="sports/cricket/bat.jpg">cricket bat</xref>
    <xref type="externalCrossReference" target="http://en.wikipedia.org/wiki/Firewall_(computing)">Firewall</xref>


* **Translation:** the TBX standard defines two different tags to enclose the
  translation level: `<tig>` and `<ntig>`. Terminator only uses the `<tig>` tag.
  The `<tig>` tag encloses the translation level. It goes on language level.

  .. warning:: Terminator doesn't support the `<ntig>` tag.

     The `<tig>` tag already provides all the required features, and the
     `<ntig>` has a lot of unnecessary features that make the TBX file
     structure much more complex making its size grow unnecessarily and making
     difficult to a person read the file using a text editor. Also the TBX-Basic
     standard only uses the `<tig>` tag.


  * **Translation identifier:** the `<tig>` tag has an attribute named `"id"`
    where Terminator puts the translation unique identifier.

    .. code-block:: xml

      <tig id="tid­-59">...</tig>

    .. note:: When exporting Terminator uses the format `"tid-NNNN"` for
       translation ids where `NNNN` is replaced by an unique number. `tid` is
       short for *translation identifier*.


* **Translation text:** the translation text goes between the opening and
  closing of the `<term>` tag that goes on the translation level (under the
  `<tig>` tag).

  .. code-block:: xml

    <term>nickname</term>


* **Part of speech:** for storing the part of speech TBX suggests the use of
  the `<termNote>` tag indicating in the `"type"` attribute the value
  `"partOfSpeech"`. The TBX standard doesn't define a part of speech values list
  (like `"noun"`, `"verb"`,...), but the TBX-Basic standard (a simplified subset
  of TBX) defines a short list of part of speech values which Terminator uses.
  Other values can be added in order to complete that list if necessary. It goes
  on translation level.
  
  .. code-block:: xml

    <termNote type="partOfSpeech">noun</termNote>


* **Grammatical gender:** TBX specifies that the grammatical gender should be
  specified using the `<termNote>` tag indicating the value
  `"grammaticalGender"` in the `"type"` attribute. TBX doesn't define a gender
  list so Terminator uses the ones defined in TBX-Basic: `"masculine"`,
  `"feminine"`, `"neuter"`. It goes on the translation level.
  
  .. code-block:: xml

    <termNote type="grammaticalGender">masculine</termNote>


* **Grammatical number:** TBX says that for saving the grammatical number it
  should be used a `<termNote>` tag with the value `"grammaticalNumber"` in its
  `"type"` attribute. For the grammatical number Terminator uses the list
  defined in TBX-Basic. The grammatical should only be put when not putting it
  could lead to misunderstanding, thus when it is `"singular"` the grammatical
  number is not exported. It goes on the translation level.
  
  .. code-block:: xml

    <termNote type="grammaticalNumber">plural</termNote>


* **Acronym:** to indicate that a translation is an acronym Terminator uses the
  `<termNote>` tag with the `"termType"` value on its attribute `"type"` and the
  text `"acronym"` between its opening and closing tags. It goes on the
  translation level.
  
  .. code-block:: xml

    <termNote type="termType">acronym</termNote>


* **Abbreviation:** to indicate that a translation is an abbreviation Terminator
  uses the `<termNote>` tag with the `"termType"` value on its `"type"`
  attribute and the text `"abbreviation"` between its opening and closing tags.
  It goes on the translation level.
  
  .. code-block:: xml

    <termNote type="termType">abbreviation</termNote>


* **Translation explaining note:** for the notes TBX defines the use of the
  `<termNote>` tag with the value `"usageNote"` on its `"type"` attribute with
  the explanatory note text between its opening and closing tags. It goes on the
  translation level.
  
  .. code-block:: xml

    <termNote type="usageNote">Don't abuse of this translation...</termNote>


* **Example of use:** for the examples of use created ad hoc (not the ones that
  can be referenced on an external source) Terminator uses the `<descrip>`
  tag with the value `"context"` on its `"type"` attribute and the example text
  between its opening and closing tags. It goes on the translation level.
  
  .. code-block:: xml

    <descrip type="context">put example text here</descrip>

  .. note:: Terminator doesn't use for this `<descrip type="sampleSentence">`
     since it doesn't appear both in TBX and in TBX-Basic, and neither will use
     `<descrip type="example">` since in this tag it is not mandatory to include
     the translation text in the example.


* **Link to real use example:** it is used for references to corpus (translation
  databases, like `open-tran.eu <http://open-tran.eu/>`_). TBX says that such
  references should be indicated using the `<xref>` tag with the value
  `"corpusTrace"` value on its `"type"` attribute. It goes on the translation
  level.
  
  .. code-block:: xml

    <xref type="corpusTrace" target="http://en.gl.open-tran.eu/suggest/window">Window on open-tran.eu</xref>


* **Completion status:** Terminator uses the `<termNote>` tag with the value
  `"processStatus"` value in its `"type"` attribute and the text
  `"provisionallyProcessed"` between its opening and closing tags to indicate
  that not all the translation information is yet finished or approved, or that
  some of the data still needs to be added. In case all the data is complete
  then this tag shouldn't appear, despite TBX defines both the values
  `"unprocessed"` and `"finalized"`. It goes on the translation level.
  
  .. code-block:: xml

    <termNote type="processStatus">provisionallyProcessed</termNote>


* **Administrative status:** to indicate the administrative status of the
  translation Terminator uses the way TBX specifies and not how TBX-Basic
  does since Terminator uses a superset of TBX-Basic. TBX specifies the use of
  the `<termNote>` tag with the value `"administrativeStatus"` on its `"type"`
  attribute and the text that indicates the status between its opening and
  closing tags. TBX defines a list of several states but Terminator only uses
  three of them:

  * `"preferredTerm­admn­sts"` to indicate that this is a recommended translation,
  * `"admittedTerm­admn­sts"` to indicate that it is a valid translation but that
    be prefer not to use it since there is another one that is recommended,
  * `"deprecatedTerm­admn­sts"` to indicate that this translation is forbidden
    (for not being a valid translation for a given language for some reasons:
    false friend,...).
  
  It goes on the translation level.
  
  .. code-block:: xml

    <termNote type="administrativeStatus">preferredTerm­admn­sts</termNote>


* **Administrative status reason:** TBX doesn't define any way to save the
  reason why a translation has a given administrative status. Due to that it was
  decided to use the `<note>` tag for specifying the reason. Since this tag is
  also used for saving notes it is necessary to use the `<termNoteGrp>` to group
  it together with the administrative status tag. Maybe some languages are not
  going to use that, but in galician it is very very important. Note that the
  reason is not specified if the administrative status is
  `"preferredTerm­admn­sts"`. It goes on the translation level.
  
  .. code-block:: xml

    <termNoteGrp>
      <termNote type="administrativeStatus">deprecatedTerm­admn­sts</termNote>
      <note>Reason: galicism</note>
    </termNoteGrp>

  .. warning:: This is a feature not supported by TBX.


.. _tbx_conformance#example_of_terminator_supported_tbx:

Example of Terminator supported TBX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE martif SYSTEM 'TBXcoreStructV02.dtd'>
    <martif type='TBX' xml:lang='en'>
        <martifHeader>
            <fileDesc>
                <titleStmt>
                    <title>Localization glossary</title>
                </titleStmt>
                <sourceDesc>
                    <p>Test glossary with concepts from software localization...</p>
                </sourceDesc>
            </fileDesc>
            <encodingDesc>
                <p type='XCSURI'>http://www.lisa.org/fileadmin/standards/tbx/TBXXCSV02.xcs</p>
            </encodingDesc>
        </martifHeader>
        <text>
            <body>

                <termEntry id="cid-23">
                    <descripGrp>
                        <descrip type="subjectField">computer science</descrip><!-- Enclosed text in english since it is the glossary 
    language (see martif opening tag) -->
                        <ref type="crossReference" target="cid-2342"></ref><!-- Reference to the subject field concept -->
                    </descripGrp>
                    <ref type="crossReference" target="cid-12">microprocessor</ref><!-- Enclosed text in english since it is the 
    glossary language (see martif opening tag) -->
                    <ref type="crossReference" target="cid-16">keyboard</ref><!-- Enclosed text in english since it is the glossary 
    language (see martif opening tag) -->
                    <descrip type="broaderConceptGeneric" target="cid-7">hardware</descrip><!-- Enclosed text in english since it is 
    the glossary language (see martif opening tag) -->

                    <langSet xml:lang="en">
                        <descrip type="definition">A computer is a programmable machine that receives input, stores and manipulates 
    data, and provides output in a useful format.</descrip>
                        <xref type="xGraphic" target="http://en.wikipedia.org/wiki/File:HPLaptopzv6000series.jpg">computer image</xref>
                        <xref type="externalCrossReference" target="http://en.wikipedia.org/wiki/Computer">English Wikipedia computer
    page</xref><!-- Multiple external references links -->

                        <tig id="tid-59">
                            <term>computer</term>
                        </tig>
                        <tig>
                            <term>PC</term>
                            <termNote type="termType">acronym</termNote><!-- "PC" is an acronym of "Personal Computer" -->
                            <termNote type="administrativeStatus">admittedTerm-admn-sts</termNote>
                            <termNote type="usageNote">Do not abuse of using this translation.</termNote>
                        </tig>
                        <tig>
                            <term>comp.</term>
                            <termNote type="termType">abbreviation</termNote><!-- "comp." is an abbreviation of "computer" -->
                            <termNote type="administrativeStatus">admittedTerm-admn-sts</termNote>
                        </tig>
                    </langSet>

                    <langSet xml:lang="es">
                        <descrip type="definition">Máquina  electrónica que recibe y procesa datos para convertirlos en
    información útil</descrip><!-- Definition without source for spanish -->

                        <tig>
                            <term>sistema</term>
                            <termNote type="administrativeStatus">admittedTerm-admn-sts</termNote>
                        </tig>
                        <tig>
                            <term>equipo</term>
                            <termNote type="administrativeStatus">deprecatedTerm-admn-sts</termNote>
                            <termNote type="processStatus">provisionallyProcessed</termNote>
                        </tig>
                        <tig>
                            <term>ordenador</term>
                            <termNote type="partOfSpeech">noun</termNote>
                            <termNote type="grammaticalGender">masculine</termNote>
                            <termNote type="grammaticalNumber">singular</termNote>
                            <termNote type="administrativeStatus">preferredTerm-admn-sts</termNote>
                            <descrip type="context">El ordenador personal ha supuesto la generalización de la
    informática.</descrip><!-- Example phrase -->
                            <xref type="corpusTrace" target="http://es.en.open-tran.eu/suggest/ordenador">ordenador en
    open-tran.eu</xref><!-- Enclosed text in spanish -->
                        </tig>
                        <tig>
                            <term>computador</term>
                            <termNote type="administrativeStatus">deprecatedTerm-admn-sts</termNote>
                        </tig>
                        <tig>
                            <term>computadora</term>
                            <termNote type="administrativeStatus">deprecatedTerm-admn-sts</termNote>
                        </tig>
                    </langSet>

                    <langSet xml:lang="fr">
                        <descripGrp><!-- Using descripGrp tags for enclosing the definition and its source -->
                            <descrip type="definition">Un ordinateur est une machine dotée d'une unité de traitement lui permettant 
    d'exécuter des programmes enregistrés. C'est un ensemble de circuits électroniques permettant de manipuler des données sous forme 
    binaire, ou bits. Cette machine permet de traiter automatiquement les données, ou informations, selon des séquences d'instructions 
    prédéfinies appelées aussi programmes.
                            Elle interagit avec l'environnement grâce à des périphériques comme le moniteur, le clavier, la souris, 
    l'imprimante, le modem, le lecteur de CD (liste non-exhaustive). Les ordinateurs peuvent être classés selon plusieurs critères 
    (domaine d'application, taille ou architecture).</descrip>
                            <xref type="xSource" target="http://fr.wikipedia.org/wiki/Ordinateur">Wikipedia: ordinateur</xref>
                        </descripGrp>

                        <tig>
                            <term>ordinateur</term>
                        </tig>
                    </langSet>
                </termEntry>

                <termEntry id="cid-27"><!-- Another concept -->
                    <descrip type="subjectField">computer science</descrip>

                    <langSet xml:lang="en">
                        <descrip type="definition">A technical standard is an established norm or requirement. It is usually a formal 
    document that establishes uniform engineering or technical criteria, methods, processes and practices. In contrast, a custom, 
    convention, company product, corporate standard, etc. which becomes generally accepted and dominant is often called a de facto
    standard.</descrip>

                        <tig>
                            <term>standard</term>
                            <termNote type="partOfSpeech">noun</termNote>
                            <termNote type="administrativeStatus">preferredTerm-admn-sts</termNote>
                        </tig>
                    </langSet>

                    <langSet xml:lang="gl">
                        <descrip type="definition">Norma que mediante documentos técnicos fixa a especificación de determinado
    tema.</descrip>

                        <tig>
                            <term>estándar</term>
                            <termNote type="administrativeStatus">preferredTerm-admn-sts</termNote>
                        </tig>

                        <tig>
                            <term>standard</term>
                            <termGrp><!-- Example of administrative status along with its reason -->
                                <termNote type="administrativeStatus">deprecatedTerm­admn­sts</termNote>
                                <note>Razón: anglicismo</note><!-- The translation of the enclosed text is: "Reason: anglicism" -->
                            </termGrp>
                        </tig>
                    </langSet>
                </termEntry>

            </body>
        </text>
    </martif>



