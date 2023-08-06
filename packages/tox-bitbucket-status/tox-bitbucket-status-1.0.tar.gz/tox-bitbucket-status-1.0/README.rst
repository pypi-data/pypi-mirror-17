tox-bitbucket-status
====================

Tox_ plugin that pushes status reports back to BitBucket_.

Installation::

  $ pip install hg+https://bitbucket.org/hpk42/tox@hook/report-status#egg=tox
  $ pip install tox-bitbucket-status

(You need to install the custom tox version for now, until the next version of tox is released).

Usage:

You need to ensure the following environment variables are set in your environment::

  CI
  CI_NAME
  CI_COMMIT_ID
  CI_BUILD_URL
  BB_USERNAME (will default to $BB_REPO_OWNER if not set)
  BB_PASSWORD
  BB_REPO_OWNER
  BB_REPO_SLUG

Then, your commits will get a build status after they are pushed to BitBucket.

Just like the ones `in this repository <https://bitbucket.org/schinckel/tox-bitbucket-status/commits/all>`_.

Codeship_
~~~~~~~~~

The ``CI_*`` variables are all set by Codeship, but you will need to seth the ``BB_*`` variables yourself.

Jenkins_
~~~~~~~~

If you are using Jenkins and the Mercurial plugin, then some of the environment will be detected from the environment variables that are set::

  CI → True
  CI_NAME → 'Jenkins'
  CI_BUILD_URL → $BUILD_URL
  CI_COMMIT_ID → $MERCURIAL_REVISION

  BB_REPO_OWNER : extracted from $MERCURIAL_REPOSITORY_URL
  BB_REPO_SLUG : extracted from $MERCURIAL_REPOSITORY_URL

At this point, the extraction of the owner/slug from the repo url only does sanity checking for mercurial repos (ie, that they are from bitbucket). Pull requests to support git repo urls will be accepted.

.. _Tox: https://testrun.org/tox/latest/
.. _BitBucket: https://bitbucket.org/
.. _Jenkins: http://jenkinsci.org/
.. _Codeship: https://www.codeship.com/
