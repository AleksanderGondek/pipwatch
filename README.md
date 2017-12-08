Pipwatch
=======
[![CircleCI](https://circleci.com/gh/AleksanderGondek/pipwatch.svg?style=svg&circle-token=658a169be1fb9e68c7ef8e5ccce9ca0b2f629af9)](https://circleci.com/gh/AleksanderGondek/pipwatch)
![License](https://img.shields.io/badge/License-Apache%20License%202.0-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/Python-3.6-blue.svg?style=flat-square)


Easily manage and keep up to date all of your projects pip dependencies.

Requirements update flow
---
![Worker flow](/docs/workerFlow.png)

How changes to requirements are applied
---
After new versions of requirement packages are verified to work, their change may be applied in the following ways:
* Push [*Implemented*]– Just as the name indicates, the commit with changes made by pipwatch is simply pushed to master branch
* Github flavoured pull request [*To be implemented*] – Changes are going to be staged on fork of project repository and then a pull request is going to be submitted to selected github instance (may be public or enterprise). Pipwatch is going to sync fork and upstream repository automatically
* Gerrit patch [*To be implemented*] – Changes are going to be submitted as a `git-review` patchset to selected gerrit instance

**Note**: Currently no monitoring is performed to verify if github/gerrit changes are merged into repository, which can become a nuisance and lead to multiple submissions of same changes.


License
---

Copyright 2017 Aleksander Gondek

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
