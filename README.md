## latestchanges

This is a very simple tool to check what are the latest changed files on a directory. This tool works on Linux and Windows system where it has been tested successfully, and since it is very OS independent, it should work just fine on Unix, as long as it runs the right version of python.

### Technology

latestchanges uses the following frameworks/libraries for the specified purposes:

* argparse: for parsing command line arguments
* colorama: for providing colored output

### Installation

To install latestchanges, just run the following command on your server machine:

```
$> pip install latestchanges
```

or

```
$> pipenv install latestchanges
```


### Running

latestchanges can be run as a command line tool:

```
$> lc $HOME
```

And it can also be used as a library:

```
import latestchanges as lc

found_files = lc.get_latest_files(source_dir='/home/user')
for f in found_files:
    print('Found file: {}'.format(f.file_name))

```


### Developers

Currently, this project is maintained and developed by:

* thilux (Thiago Santana)

Contributions are expected and more than welcome. If you have ideas to enhance the solution, please raise and issue and specify your request. The same is required if you simply want to report bugs. If you want to contribute with code, fork the project and submit a pull request and it will be surely reviewed and happily accepted.

### License

Copyright 2018 Thiago Santana (thilux).

Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements. See the NOTICE file distributed with this work for additional information regarding copyright ownership. The ASF licenses this file to you under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.