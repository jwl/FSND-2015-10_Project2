Project work for P2 of Udacity's FSND, October 2015 cohort.

Forked from [rdb-fullstack](https://github.com/udacity/fullstack-nanodegree-vm).



--------------------
### Table Schemas

##### players
This lists individual players registered in the system. This table gives NO indication what tourneys they are participating in, if any.

* `p_id` - the player's unique ID number
* `p_name` - the player's name, expressed as a string


##### tourneys
This lists tournaments

* `tourney_id` - unique ID for each tournament
* `tourney_desc` - descrition of tournament as a string

##### matches
All matches across all tournaments. Matches may be unplayed or in-progress. By default, on creation results should be set to 'unplayed'. If complete, there will either be a winner or a tie. Results stored as an integer, represented as follows:

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
