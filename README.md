Project work for P2 of Udacity's FSND, October 2015 cohort.

Forked from [rdb-fullstack](https://github.com/udacity/fullstack-nanodegree-vm).

--------------------
### Project Structure
```
.
├── README.md
└── vagrant
    ├── catalog
    │   └── README.txt
    ├── CREATE
    ├── forum
    │   ├── forumdb.py
    │   ├── forum.py
    │   └── forum.sql
    ├── pg_config.sh
    ├── tournament
    │   ├── tournament.py
    │   ├── tournament.sql
    │   └── tournament_test.py
    └── Vagrantfile
```


--------------------
### HOWTO setup
1. Setup and launch VM
2. Populate database
3. Run test suite

#### Setup and launch VM
This project is based around the [rdb-fullstack](https://github.com/udacity/fullstack-nanodegree-vm) starter project and is meant to be used with Vagrant and Virtualbox. Please reference the [Vagrant](https://docs.vagrantup.com/v2/installation/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) documentation on how to install each.

Once Vagrant and VirtualBox are setup on your system:

* navigate to the `vagrant` directory of the project
* start up your VM with vagrant and connect to it:
	* `vagrant up`
	* `vagrant ssh`
* once connected, change directory to the vagrant shared directory:
	* `cd /vagrant`
* change directory to the `tournament` directory
* Note: Once complete, use `exit` to disconnect from the VM and `vagrant halt` to shutdown the VM.

#### Populate database
* execute `tournament.sql` to create the database and initialize the tables
	* `psql -f tournament.sql`
* if necessary, re-execute the above command to drop the database and re-initialize it.

#### Run test suite
* execute the test suite `tournament_test.py` to verify functionality of project
	* `python tournament_test.py`
	* 8 tests should be executed and a success message should be printed

--------------------
### Table Schema Reference

##### players
This lists individual players registered in the system. This table gives NO indication what tourneys they are participating in, if any.

* `p_id` - the player's unique ID number
* `p_name` - the player's name, expressed as a string


##### tourneys
This lists tournaments

* `tourney_id` - unique ID for each tournament
* `tourney_desc` - descrition of tournament as a string

##### matches
All matches across all tournaments. Matches may be unplayed or in-progress. For the purposes of this project, all matches entered into the table will be matches that are already played to completion with a clear winner. However, there exists support for tracking unplayed and in-progress matches. `m_results` is an integer indicating the state of the match or the winner, as outlined below:

* `-2`: unplayed
* `-1`: in-progress
* `0`: tie
* `1`: player 1 is the winner
* `2`: player 2 is the winner

* `match_id` - unique identifier for the match expressed as an integer
* `t_id` - reference to the tournament this match belongs to
* `p1` - player ID number for the first player
* `p2` - player Id number for the second player
* `m_results` - Integer representation of results as outlined in above list
