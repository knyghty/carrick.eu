Faster dependabot updates with groups
#####################################

:date: 2024-07-09
:tags: dependencies, github-actions
:has_code: true

Back in 2022, I wrote about `automatically updating dependencies with dependabot`_.
However, this can be quite tedious. If you have a lot of dependencies, or even
if you don't, you'll likely get spammed with many pull requests on your scheduled
update time. This can be quite annoying, especially if you have a lot of repositories.

Every time you merge one of these pull requests, if you're strict about only merging
branches when they're up to date with the base branch, you'll have to update the next
pull request, wait for all your CI checks to pass, burning through your GitHub actions
minutes (or other CI credits), and warming the planet a little. And then, the next PR.
And the next. And the next.

Now, you can just YOLO merge without updating the branch if you're happy to take the risk.
And it doesn't take much time to update the branch, you can spread this out over a day in
those few minutes between tasks, or when pretending to pay attention in a meeting,
but you don't need to do any of this anymore.

Last year, GitHub released a grouping feature for dependabot.
You can now group your dependencies in the dependabot configuration like so:

``.github/dependabot.yml``

.. code-block:: yaml

    version: 2
    - package-ecosystem: "pip"
      directory: "/"
      groups:
        all:
          patterns:
            - "*"
      schedule:
        day: "monday"
        interval: "weekly"
        time: "09:00"
        timezone: "Europe/Amsterdam"

I simplified the configuration a bit from last time, but the important thing is the
``groups`` key. This allows you to group your dependencies by a pattern. In this case,
I'm grouping all dependencies with the pattern ``*``. This will group all dependencies
together, so you'll only get one pull request for all your dependencies, rather than
one for each. You can have multiple groups, so you can group your dependencies however
you like, although I don't personally find much utility in this.

A huge time saver, and a huge annoyance saver.


.. _automatically updating dependencies with dependabot: {filename}../2022/auto-update-dependencies.rst
