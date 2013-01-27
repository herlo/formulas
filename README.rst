What are Formulas
=================

Formulas provide an better way to manage local configurations.

The idea was formed around a concept to extend the ability to manage a
local system with configuration management tools. The primary CM tool
supported is ansible, but it is possible to support other CM tools.

A Formula is idempotent, meaning that it can be applied and each time
the resulting configuration is the same. The value of this is that one
or more machines can use the same Formula and expect the same setup.

Consider the following example as a simple Formula::

  * Install the Apache Web Server (httpd)
  * Add a configuration to create a virtual host
  * Drop some basic web data, including configuration for a database
  * Install Mysql (mysql-server)
  * Start the httpd and mysql services
  * Sync the database

It may be clear that some of the steps above can be done by a simple
yum install or adding a simple script to the %post section in a
kickstart. In some cases, however, interactive responses are required,
like the username/password of the database, for example. In these cases
it may be better to have an interactive prompt at first boot.

Additionally, Formulas could be played back after the initial interactive
configuration. Thus providing automation to the process. Answer the questions
once, apply the same rules in several other situations quickly and easily.

Managing Formulas
=================

Simply put, many Formulas will be written. It would seem logical that Formulas
should be shared, but with a control structure of some sort. Therefore, a model
has been put forth to manage 'approved' Formulas, by which a trust can be formed
between the infrastructure provider and those applying Formulas. Formulas will
exist in a git repository which is tightly managed for writes by gitolite. This
will provide a level of assurance that any Formula being applied from the
'approved' set can be applied reliably each time.

Additionally, it would make sense that a read-only form of these git repositories
would exist to provide an easy mechanism for sharing. Because the goal is to
encourage more 'approved' Formulas, as well as provide a means for testing,
expanding and even maintaining a separate set of Formulas, a git forking model
has been adopted.

With the exception of the 'approved' repositories being managed in some form
of review and approval process, likely similar to the Fedora RPM approval
model, git repositories can be forked and modified much like how
they are on github. The fork and pull request model works well because the
control remains with the upstream repository. In this case, it proves valuable
because when any Formula is improved upon, it can be merged back into the
upstream repository at the maintainer's convenience or not at all.

Applying Formulas
=================

Formulas can be applied to any Linux system as long as it is a supported
configuration management system. This currently means that it '''must'''
be ansible, but more are likely to come.

To apply a Formula, it must exist on the local system in an archive. A Formula
is applied as follows::

  # formulas apply formula_one

Formulas can be downloaded from remote sources to the local system as part of the apply
command. Remote sources can be configured in the Formulas.conf. Multiple
sources can be searched in the order provided, thus allowing for searching
through 'approved' Formulas before others, for example. An example
configuration may look something like this::

  remote_sources:
    - git://github.com/herlo/formulas/
    - git://github.com/bob/formulas/
    - file:///var/lib/formulas/

In this way, if the 'formula_one' Formula existed in both the herlo and bob
repositories, the herlo 'formula_one' Formula would be downloaded and applied.
If the 'formula_two' were to be applied, the same search would occur, but it's
possible that the bob 'formula_two' formula would be the first one found since
the 'herlo' repository didn't have a 'formula_two'. Additionally, locations for
Formulas can be overridden by a config option::

  # formulas apply formula_one --remote_source=file:///var/lib/formulas,file://home/herlo/formulas

Eventually, the goal is to have Formulas available in 'FirstBoot'. In Fedora
18, FirstBoot was replaced by anaconda, probably called 'Stage III'. Because
anaconda Stage III now provides this functionality, it is much more flexible
than the old FirstBoot. This makes adding a GUI interface for formulas much
less complex. To that end, the list of 'approved' Formulas may easily be
available and/or configurable at FirstBoot. Having something like this makes
Formulas a 'killer' feature for Fedora 18 and beyond.


