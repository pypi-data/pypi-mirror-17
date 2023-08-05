=========
Changelog
=========

Version 0.2.1
=============

- BUGFIX: use the multiprocessing variant of timeout
- BUGFIX: don't count error list to the linecount

Version 0.2.0
=============

- refactor
- refactor tests
- add timout decorator
- cleanup some coverage
- add coverage
- add RunCode class + tests
- refactor
- new methode for ReturnObject + tests
- add Emitter class with tests
- add example usage
- remove example/.cache
- no more .cache in example
- use a named pipe to emit an error when a forbidden function is called in the c code
- Refactor RunCode
- store if the code is run in use_stdin mode or not in the PopenReturnObject
- use the capturer module to capture stdout in the emit tests
- reorganize example
- Split argument cmd in Command(ldpreload, filename) to be more flexible with the emittet text later
- simplify RunCode
- reorganize
- Restructure ReturnObjects, RunCode and add Make
- refactor inteface of Make
- pylint version 1.6.3 used
- Bugfix: Check befor apply __eq__
- add a msgtype and a MsgType enum to the emit function
- add descriptors for Boolean and Text
- use MsgType in Make class
- add gitlab-ci and codecov support
- Correct badges
- rename enum field
- add pep8 checke to gitlab-ci
- apply pep8 to all files
- install cuebung_helper for pep8 test
- remove pytest-pep8 from combined test
- restructure gitlab-ci configs
- use mocking instead of capturer
- pep8
- add pylint to gitlab-ci
- Check the file encoding
- deactivate pylint test for the moment
- add ce_ignore
- implement the validation
- use the validation in the example
- improved readability of the tests
- Solve naming conflict TimeoutError -> MyTimeoutError
- Move Config and Command to helper.py
- pylint conform
- Merge branch 'master' into 'master'
- Merge branch 'patch-1' into 'master'
- test ReferenceReturnObject
- Merge branch 'master' of gitlab.com:cuebung/cuebung_helper_functions
- correct the test
- unify the emit data from Make object

Version 0.1.0
=============

- Feature A added
- FIX: nasty bug #1729 fixed
- add your changes here!
