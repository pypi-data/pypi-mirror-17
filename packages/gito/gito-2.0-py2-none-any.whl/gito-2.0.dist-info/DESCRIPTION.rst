# gito

## (Easy TODO`s)
### Command line python library to view TODO`s from all the files under a directory with deadline displays and wunderlist uploads.
#
#
## Installing Gito is Simple, Here we go..
### Installing pip
```sh
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
```
### Installing Gito
```sh
$ pip install gito
```
## Configuration
Configuration Location - `~/.gito` (or) `C:\\Users\\user\\.gito`
#### Initialize Configuration
The configuration file can be created using gito cli.
```
$ gito --initconfig
```
#### Configuration usage
```yaml
wl_access_token: YOUR_WUNDERLIST_ACCESS_TOKEN
```
`Note: Please Obtain the access token for your wunderlist account by visiting`
[wloauth](http://wloauth.herokuapp.com)
## Usage Example
#### gito cli

```
$ gito
usage: gito [-h] [--wsync] [--display] [--initconfig]

Gito - Command Line Utility to Print TODO`s in source files & upload to
wunderlist

optional arguments:
  -h, --help    show this help message and exit
  --wsync       Sync the TODO`s to wunderlist
  --display     Display all the TODO`s
  --initconfig  Init Gito Configuration file under home

```
#### Displaying todos (example)
```
$ gito --display
TODO`s:

/Users/xyz/project/main.py
        1. [NO-DUE] Plan for new functionality
        2. [NO-DUE] Refactor the code

/Users/xyz/project/test.py
        1. [NO-DUE] Test xyz functionality

```
#### Uploading todos to wunderlist (example)
```
$ gito --display
Uploading tasks to Wunderlist:
Syncing task -  Plan for new functionality
[DONE]
Syncing task -  Refactor the code
[DONE]
Text xyz functionality
{DONE}
```
## Gito features & Rules
#### TODO Format
```bash
// TODO: Your todo here
```
`(or)`
```python
# TODO: Your todo Here
```
`Note: Only single line comments are supported.`
#### Due Date
Gito allows mentioning due dates in todo which will be identified and parsed. These dates are used to display the due status and also for setting as due date in wunderlist.
###### Date Format
```bash
// TODO: 05-06-2020
```
`(or)`
```bash
# TODO: 05-06-2020
```
###### Due status
  1. `[OVERDUE]` - Behind the date
  2. `[ONDUE]` - On the date
  3. `[NORMAL]` - Having more than `5` days
  4. `[CRITICAL]` - Having less than `5` days

#### Wunderlist upload
Inorder to upload to wunderlist, the access token must be specified in the configuration file (see `Configuration`).
On upload a list with the directory name will created and every todo will be created as a task in the list. Due status are excluded in wunderlist upload.

## Releases
###### v0.9 (Beta) - Initial Release. Includes display, upload functionality.
###### v1.2
###### v2.0 (Stable) - Added support for excluding gitignore files.


#### Thanks for checking out this library. Feel free to create issues regarding bugs or features and contribute to the project by forking `dev` branch and submitting a pull request.
#### Fork it before you Spoon it.
### Contributors:
##### [raghu](http://twitter.com/raghu12133)


