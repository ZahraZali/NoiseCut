# OwlPy development environment and contribution guide

## Language

OwlPy is written in the Python programming language (version >=3.6).

## Deployment

OwlPy uses Setuptools for its installation script. See `setup.py` and
`setup.cfg` in the project root directory.

## Testing

`pytest` is used for testing. To run all tests, run

```sh
pytest  # or pytest-3
```

Running the tests requires both [ObsPy](https://obspy.org) and
[Pyrocko](https://pyrocko.org) to be installed.

## CI

Drone CI tests are run on any commits pushed to the repository. By default,
flake8 is run, tests are run, test coverage is measured and docs are built.

## Versioning and releases

Git is used for version control. Use development branches for new features.
Master branch should always point to a stable version.

The OwlPy project adheres to [Semantic Versioning](https://semver.org).

Notable changes must be documented in the file `CHANGELOG.md`. The format of
the change log is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

### Commit message conventions

* Fllow the usual convention 1 line summary, blank line, description.
* Start with lower case.
* Colon-prepend affected component.
* Try to use imperative form.
* Examples:
  - `docs: add section about weighting`
  - `polarization: correct typo in component names`
  - `rotation from array: fix issues with misaligned traces`

### Branching policy

* Use topic branches to develop new features.
* Open a pull request when ready to start discussions.
* When a topic is complete, all tests pass and it is rebased to current `main`:
  merge with `--ff-only` and don't forget to update `CHANGELOG.md`.
* The `main` branch should always point to a stable version.

### Rebase small changes before pushing

Try to rebase little changes on top of `main` (or any other development branch)
before pushing, it makes the history much better readable. Here is a safe way
to do so:

```sh
# we are on feature branch
git fetch origin    # important, otherwise we rebase to outdated
git rebase origin/main
```

If during push it refuses to upload ('not fast forward...') then repeat the
procedure, because someone else has pushed between your fetch and push.

When using `git pull` or `git merge` always add `--ff-only` to avoid accidental
merge commits.

**Tip:** use `rebase -i ...` to simplify/fixup/beautify your changeset.

## Code style

OwlPy source code must follow the PEP8 coding standards. It must pass the
code style check provided by the `flake8` tool.

Additionally,

* use i/n convention for indices and counts
  - e.g. `for istation in range(nstations):`
* do not abbreviate words unless this would result in ridiculously long names
* use British English, e.g.
  - 'modelling' rather than 'modeling'
  - 'analyser' rather than 'analyzer'
  - 'optimiser' rather than 'optimizer'
* log and exception messages:
  - capital beginning
  - final period
  - Progress actions should end with `...`, e.g. `Generating report's archive...`
  - e.g. `raise ProblemDataNotAvailable('No problem data available (%s).' % dirname)`
  - in-text names must be quoted; not needed after colons
* docstrings:
  - Docs are built with Sphinx, use rst syntax.
  - Follow the usual convention 1 line summary, blank line, description.
  - Triple-quotes above and below docstring. New line after opening 
    triple-quotes.

### Use pre-commit

The repository comes with a [pre-commit](https://pre-commit.com/) config to
check the code with flake8 before commiting.

Install the git-hook with:
```sh
pre-commit install
```

## Documentation

OwlPy's documentation is built using the `Sphinx` tool. See the `docs`
in the project's root directory. Build with `make html` in `docs`.

*Text style rules:*

* titles: only capitalize first word
* use British English
