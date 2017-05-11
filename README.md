# Log Analysis

This is a project that shows the data analysis of news publication platform based on the user logs using postgreSQL database.

### Instructions to run the code


1. Clone this repository.
2. Next, download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the logAnalysis folder inside the vagrant directory.
3. To use the Vagrant virtual machine, navigate to the LogAnalysis/vagrant directory in the terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh (logs into the virtual machine).
4. Once you have executed the vagrant ssh command, you will want to cd /vagrant/logAnalysis to change directory to the synced folders in order to run the project
5. once you're in the logAnalysis folder in the VM do the following:
```sh
$ psql -d news -f newsdata.sql
$ Ctrl + D to exit psql
$ python logAnalysis.py
```