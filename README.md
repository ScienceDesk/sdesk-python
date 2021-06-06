# ScienceDesk Python helpers

This module provides Python code to help you interact with and extend the
ScienceDesk platform.

## Modules

- api: helpers to interact with the ScienceDesk API
- proc: helpers to write ScienceDesk algorithms


## Documentation
You can check the current documentation at [Read The Docs](https://sciencedesk-helper-library.readthedocs.io)


## Release Management (for contribuitors)
### Release candidates
 * Set proper version on files `pyproject.toml` and `sdesk/__init__.py` following `<X>.<Y>.<Z>+RC<V>` (i.e 0.2.4+RC0)
 * Commit and push to development branch
 * The package will be published at https://pypi.debonzi.dev
    * Install it with ` pip install -i https://pypi.debonzi.dev/simple/ sdesk-0.2.4+rc.0` (use the proper package version)

 ### Oficial Releases
 * Set proper version on files `pyproject.toml` and `sdesk/__init__.py` following `<X>.<Y>.<Z>` (i.e 0.2.4)
 * Commit to `development` branch
 * Merge `development` into `master` branch
 * Tag with the same package version
    * For instance ` git tag 0.2.4`
 * push `development` `master` and tag to origin
    * For instance `git push origin master develoment 0.2.4` 
 * The package will be published at https://pypi.org/