# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monkeyble', 'monkeyble.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['monkeyble = monkeyble.cli.monkeyble_cli:main']}

setup_kwargs = {
    'name': 'monkeyble',
    'version': '1.1.1',
    'description': 'End-to-end testing framework for Ansible',
    'long_description': '<p align="center">\n    <img src="docs/images/monkeyble_logo.png">\n</p>\n\n<h3 align="center">End-to-end testing framework for Ansible</h3>\n\n<p align="center">\n<a href="https://hewlettpackard.github.io/monkeyble"><img alt="Doc" src="https://img.shields.io/badge/read-documentation-1abc9c?style=flat-square"></a>\n<a href="https://makeapullrequest.com"><img alt="PR" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>\n</p>\n\n# Monkeyble\n\nMonkeyble is a callback plugin for Ansible that allow to execute end-to-end tests on Ansible playbooks with a \nPythonic testing approach. 🧐\n\nMonkeyble allows, at task level, to:\n\n- 🐵 Check that a module has been called with expected argument values\n- 🙊 Check that a module returned the expected result dictionary\n- 🙈 Check the task state (changed, skipped, failed)\n- 🙉 Mock a module and return a defined dictionary as result\n\nMonkeyble is designed to be executed by a CI/CD in order to detect regressions when updating an Ansible code base. 🚀 \n\n## Quick tour\n\nComplete documentation available [here](https://hewlettpackard.github.io/monkeyble).\n\nAnsible resources are models of desired-state. Ansible modules have their own unit tests and guarantee you of their correct functioning.\nAs such, it\'s not necessary to test that services are started, packages are installed, or other such things. \nAnsible is the system that will ensure these things are declaratively true.\n\nThat being said, an Ansible playbook is commonly a bunch of data manipulation before calling a module that will perform a particular action.\nFor example, we get data from an API endpoint, or from the result of a module, we register a variable, then use a filter transform the data like combining two dictionary, \ntransforming into a list, changing the type, extract a specific value, etc... to finally call another module in a new task with the transformed data..\n\nGiven a defined list of variable as input we want to be sure that a particular task: \n\n- is well called with the expected instantiated arguments\n- produced this exact result\n- has been skipped, changed or has failed\n\n### Check input\n\nMonkeyble allows to check each instantiated argument value when the task is called:\n\n```yml\n  - task: "my_task_name"\n    test_input:\n      - assert_equal:\n          arg_name: module_argument\n          expected: "my_value"\n```\n\nMonkeyble support multiple test methods:\n\n- assert_equal\n- assert_not_equal\n- assert_in\n- assert_not_in\n- assert_true\n- assert_false\n- assert_is_none\n- assert_is_not_none\n- assert_list_equal\n- assert_dict_equal\n\n### Check output\n\nMonkeyble allows to check the output result dictionary of a task\n\n```yml\n  - task: "my_task_name"\n    test_output:\n      - assert_dict_equal:\n          dict_key: "result.key.name"\n          expected: \n            key1: "my_value"\n            key2: "my_other_value"\n```\n\nSame methods as the `test_input` are supported.\n\n### Task states\n\nMonkeyble allow to check the states of a task\n\n```yml\n  - task: "my_task_name"\n    should_be_skipped: false\n    should_be_changed: true\n    should_failed: false\n```\n\n### Monkey patching\n\nMonkey patching is a technique that allows you to intercept what a function would normally do, substituting its full execution with a return value of your own specification. \nIn the case of Ansible, the function is actually a module and the returned value is the "result" dictionary.\n\nConsider a scenario where you are working with public cloud API or infrastructure module. \nIn the context of testing, you do not want to create a real instance of an object in the cloud like a VM or a container orchestrator.\nBut you still need eventually the returned dictionary so the playbook can be executed entirely.\n\nMonkeyble allows to mock a task and return a specific value:\n```yml\n- task: "my_task_name"\n  mock:\n    config:\n      monkeyble_module:\n        consider_changed: true\n        result_dict:\n          my_key: "mock value"\n```\n\n### Cli \n\nMonkeyble comes with a CLI that allow to execute all tests from a single command and return a summary of test executions.\n```bash\nmonkeyble test\n\nPlaybook   | Scenario        | Test passed\n-----------+-----------------+-------------\n play1.yml | validate_test_1 | ✅\n play1.yml | validate_test_2 | ✅\n play2.yml | validate_this   | ✅\n play2.yml | validate_that   | ✅\n \n 🐵 Monkeyble test result - Tests passed: 4 of 4 tests\n```\n\n## Do I need Monkeyble?\n\nThe common testing strategy when using Ansible is to deploy to a staging environment that simulates the production.\nWhen a role or a playbook is updated, we usually run an integration test battery against staging again before pushing in production.\n\nBut when our playbooks are exposed in an [Ansible Controller/AWX](https://www.ansible.com/products/controller) (ex Tower)\nor available as a service in a catalog like [Squest](https://github.com/HewlettPackard/squest), we need to be sure that we don\'t have any regressions \nwhen updating the code base, especially when modifying a role used by multiple playbooks. This is where Monkeyble is helpful. Placed in a CI/CD it will \nbe in charge of validating that the legacy code is always working as expected.\n\nMonkeyble is a tool that can help you to enhance the quality of your Ansible code base and can be coupled \nwith [official best practices](https://docs.ansible.com/ansible/latest/reference_appendices/test_strategies.html).\n\n## Contribute\n\nFeel free to fill an issue containing feature request(s), or (even better) to send a Pull request, we would be happy to collaborate with you.\n\n> If you like the project, star it ⭐, it motivates us a lot 🙂\n',
    'author': 'Nicolas Marcq',
    'author_email': 'nicolas.marcq@hpe.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hewlettpackard.github.io/monkeyble/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
