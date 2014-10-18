##coursera-dl
A small script developed to help me download all videos from enrolled courses at coursera. I was a bit tired of manually downloading videos as they were released.

The implementation is split into two main modules: `coursera_session`, and `coursera-dl`. 

###dependencies
It's only dependency is the [requests](http://docs.python-requests.org/) module (version >= 2.0.0).

###coursera_session
The `coursera_session` module provides a class `CourseraSession`. The class is derived from `requests.Session` - it forges a log in, and from that point provides functions for scraping information about a course, and to download videos. This module is not dependent on the `coursera-dl` module, it may be used for any purpose.

###coursera-dl
This module implements a CLI using the `coursera_session` module. It maintains records of already downloaded videos and courses to monitor. It facilitates adding and removing of courses from the downloader, and updating registered courses. The CLI is as follows:

```
	python coursera-dl.py update [help | all | (course_id)...]`
	python coursera-dl.py courses add [help | (course_id)...]`
	python coursera-dl.py courses remove [help | all | (course_id)...]`
	python coursera-dl.py courses list`
```

####coursera-dl update
This function is used to download new videos for registered courses.

It accepts a list of course IDs, or the word `all`. Specifiying all
causes the downloader to update all registered courses. Otherwise, only
specified courses are updated. For example, updating all courses:

	`coursera-dl update all`

And to update only specific courses:

	`coursera-dl update algo-001 crypto-01`

####coursera-dl courses add
This function allows you to add courses to the list of maintained courses. 
Course IDs should be separated by a space. An example of a valid command for this function is:

	`coursera-dl courses add proglan-003 ml-008 mmds-01`

####coursera-dl courses remove
This function allows you to remove courses from the list of maintained courses. 
Course IDs should be separated by a space. In the case you wish to remove all courses 
(i.e, reset the state of the program), use `all` as the sole argument; for example:

	`coursera-dl courses remove all`

Another example of a valid command for this function is:

	`coursera-dl courses remove algo-001 crypto-01`

####coursera-dl courses list
This function will print a list of all registered courses. It's use is very simple:

	`coursera-dl courses list`