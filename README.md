# Use & Abuse of Personal Information
==================================================

Virtually every time that you sign up for an account or for information across the Internet, you are required to share a little piece of yourself with the unseen second party.  This repository contains the raw data, initial data processing scripts, and experimental design for an 18-month small-scale experiment that seeks to answer the question of how those second parties use-and-abuse your personal information.  The results come from a series of collection tools (email, voicemails, texts) created to track the results of one-time interactions of 300 fake identities with 185 distinct organizations.  Although sheer numbers appear large (16450 emails, 3482 phonecalls, 949 voicemails, 774 texts) at first glance, the true intent here is to establish a normative baseline for the design of a larger scale experiment that will more conclusively answer these questions with ~100k identities and ~1k phone lines.  The analysis also includes an initial attempt to quantitatively score privacy policies and user agreements according to a rubric that questions how well consumers' information is protected, though correlations are weak at best, inviting additional consideration.  The preliminary results for the "Use and Abuse of Personal Information" (U&A) project were presented at Blackhat USA 2021.

In support of broader experimentation and hopefully accountability in how personal information is shared across the Internet, we are sharing our raw data, analysis scripts, and some supporting documentation.  As with any experiment of this complexity, there are a wide variety of lessons learned, many of which have small or large impacts on the data analysis.  Likewise, some aspects of the data (passwords, personal info of team members, etc) have intentionally been scrubbed, and all accounts have been disabled prior to posting here.  We recommend reading the documentation to learn more about these caveats. 

-------------------

.. contents:: **Table of Contents**

Highlights

##########

Email and Phone server Database: raw collections and processing scripts for Zadarma phone/texts and RainLoop email server

Initial Research and Project Setup: original project plans, task descriptions, and goals

Political Timeline Analysis: attempts to correlate observed traffic to political and social events

Privacy Policy Analysis: raw and processed (quantitative rubric) results for 188 distinct privacy policies / terms of service

Additional docs: just that...


Documentation
#############

..... to be added once Blackhat releases  ......

Blackhat USA 2021 whitepaper

Blackhat USA 2021 presentation


Contributing
############

If you find any errors, feel free to open an issue; those issues will be integrated into our future experimental design for the large-scale trial.  If you provide adequate contact information, we will incorporate your feedback and potentially offer opportunities to participate if we are able to crowd source the future analysis.


Citing this Repository
######################

This repository contains implementations of both custom and third-party open source algorithms (e.g. sentiment analysis, email parsers, fake name and facial image generators, etc.) and therefore, whenever those algorithms are used, their respective works **must** be cited.  We have attempted to include all relevant citations for their works in the attached whitepaper.  

Since this repository isn't the *official* code for any publication, you take responsibility for the *correctness* of the implementations (although we've made every effort to ensure that the code is well tested).  Nevertheless, if you find this code useful for your research, please consider referencing it in your work so that others are aware.
This repository isn't citable (since that requires `archiving and creating a DOI <https://guides.github.com/activities/citable-code/>`_), so a simple footnote would be the best way to reference this repository.

.. code:: latex
    \footnote{Code is available at \textit{github.com/humeESL/Use-and-Abuse-PII}}

If your work specifically revolves around tracking propagation of personal information across the Internet, consider citing our whitepaper (Blackhat 2021) or upcoming conference paper(s) delving deeper into the analysis.

.. code:: latex
    @article{humeUseAbusePII,
            author = {A. {Michaels} and K. B. {George} and L. {Anderson} and J. {Harrison} and J. {Lyons} and L. {Maunder} and P. {O'Donnell} and B. {Vanek} and H. {Bui} and C. {Dunnavant} and P. {Hancock} and M. {Jackson} and C. {Mathewes} and S. {Ramboyong} and A. {Schliefer} and B. {Timana-Gomez} },
            doi = {},
            issn = {},
            journal = {Blackhat {USA} },
            month = {August},
            number = {},
            pages = {},
            title = {Use \& Abuse of Personal Information},
            volume = {},
            year = {2021}
    }
  

Authors

#######

.. list-table::
    :widths: 30, 60, 10
    :align: center
    * - **Alan J. Michaels**
      - Professor and Director, Electronic Systems Lab
      - ajm@vt.edu
    * - **Kiernan B. George**
      - M.S. ECE Graduate
      - kbg98@vt.edu

Numerous others have generously contributed to this work -- see `CONTRIBUTORS.rst <CONTRIBUTORS.rst>`_ for more details.

.. |br| raw:: html
    <br /># use_and_abuse_pii
