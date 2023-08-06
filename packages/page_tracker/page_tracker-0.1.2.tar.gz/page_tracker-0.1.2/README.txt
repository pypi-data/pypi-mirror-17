===========
Page Tracker
===========

Tracks a page and sends out email alerts if something changes in the tracked page 
	test.py
    #!/usr/bin/env python

    import page_tracker
	page_tracker.track_page()

=============
configuration
=============
A config.JSON file has to be setup like so in the same directory as the file calling the track_page function like so
{
	"gmail_id": <any gmail user id from which email alerts will be sent>,
	"gmail_password": <password of the id used to send out alerts>,
	"send_alert_to" : <any email id to which alerts will be sent >,
	"link_to_monitor": <link to monitor>,
	"time_interval": <time interval in seconds , takes integer values only >
}
