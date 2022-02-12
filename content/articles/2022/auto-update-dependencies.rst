Automatically updating dependencies with dependabot
###################################################

:date: 2022-02-12
:tags: dependencies, github-actions
:has_code: true

Outdated packages can open your application up to security issues. Moreover,
newer versions will often have performance improvements, bug fixes and generally
fewer problems. Keeping them up to date over multiple codebases can be quite
painful, but it's possible to bring this effort down to close to zero with a bit
of up-front effort.

This post applies only if you're hosting your code on GitHub. If not, there are
managed options for dependency upgrades, such as `Snyk`_. It's very expensive,
but does a lot of other things too. If you *are* on GitHub, this is a free or
cheap alternative.

First, a few pre-requisites. You'll need to ensure "Allow auto-merge" is
enabled in your repository settings. You should also configure dependabot
security alerts in the "Security" tab. These alerts happen outside of the
dependabot schedule we'll set up later, and will ensure you get critical security
updates as quickly as possible. You'll also need to make sure GitHub Actions
is enabled for your repository.

Next, you'll need to create a new file for the dependabot configuration:

``.github/dependabot.yml``

.. code-block:: yaml

    version: 2
    updates:
      - package-ecosystem: "github-actions"
        assignees:
          - "<your_github_username>"
        directory: "/"
        reviewers:
          - "<your_github_username>"
        schedule:
          day: "monday"
          interval: "weekly"
          time: "09:00"
          timezone: "Europe/Amsterdam"
      - package-ecosystem: "pip"
        allow:
          - dependency-type: all
        assignees:
          - "<your_github_username>"
        directory: "/"
        reviewers:
          - "<your_github_username>"
        schedule:
          interval: "daily"
          time: "09:00"
          timezone: "Europe/Amsterdam"


The confiration is quite straightforward. Note there are two ``package-ecosystem``
sections defined. One of these is for pip, which will also work for pipenv and poetry.
The other will keep any GitHub actions you use up to date. We'll be using one of
these soon, so it seemed good to add it. You can set the schedule however makes sense
for your workflow. You don't need to set assignees and reviewers, but I like to add
them so they show up in my GitHub notifications and I can make sure I don't miss
anything. Not every update will be able to be merged automatically, so it's good
to know about them.

One other important thing here is the ``allow`` section. Here I've set
``dependency-type`` to ``all``, which means that subdependencies will also be updated.
Without this, only explicitly defined dependencies will be updated.

Other `configuration options`_ are availble.

Adding this file is enough for dependabot to submit pull requests on your repo with
package updates. We need to do a bit more to get them merging automatically. For this,
we need GitHub Actions.

.. warning::
    You should only have your dependencies merge automatically if you have an
    exhaustive CI set up. Otherwise, you may be vulnerable to `obnoxious developers`_
    and supply chain attacks. Supply chain attacks may still get through your CI
    however, so you should judge the level of risk you're willing to tolerate.

We'll create a new file, ``.github/workflows/dependabot-automerge.yml``.

.. code-block:: yaml

    name: Dependabot auto-merge
    on: pull_request_target

    permissions:
      pull-requests: write
      contents: write

    jobs:
      dependabot-auto-merge:
        runs-on: ubuntu-latest
        if: ${{ github.actor == 'dependabot[bot]' }}
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        steps:
          - name: Dependabot metadata
            id: metadata
            uses: dependabot/fetch-metadata@v1.1.1
            with:
              github-token: "${{ secrets.GITHUB_TOKEN }}"
          - name: Approve PR
            run: gh pr review --approve "$PR_URL"
          - name: Merge PR
            if: ${{ steps.metadata.outputs.update-type != 'version-update:semver-major' }}
            run: gh pr merge --auto --squash "$PR_URL"

Exactly what you put in this file will depend on your workflow. For example, if
your pull requests do not require reviews, you can omit that section. Are you
feeling risk-averse? Remove the auto-merge, or use it only for patch versions.
The opposite? Remove the conditional and auto-merge everything.

This example will approve every dependabot pull request, and merge any non-major
semver versions automatically so long as all required checks pass.
For major versions, I like to review them to make sure nothing will break.
If the project isn't using semantic versioning, it's a little difficult to know
what happens here, however. My assumption is that it'll do its best to figure it out
and assume it's a major version. But it may be that if it doesn't look like it's using
semver, it will not count as a major update and will be merged automatically.
If anyone does know the answer to this, I would `love to hear it`_. Luckily, most
packages use something similarto semantic versioning these days so I haven't yet had any
problems. I'll update this post if I notice any.

I hope this saves you some time you could be using for something more fun.

.. _Snyk: https://snyk.io/
.. _configuration options: https://docs.github.com/en/code-security/supply-chain-security/keeping-your-dependencies-updated-automatically/configuration-options-for-dependency-updates
.. _obnoxious developers: https://www.theregister.com/2022/01/10/npm_fakerjs_colorsjs/
.. _love to hear it: mailto:tom@carrick.eu
