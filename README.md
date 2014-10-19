#coursera-dl
A small script developed to help me download all videos from enrolled courses at coursera. I was a bit tired of manually downloading videos as they were released.

The implementation is split into two main modules: `coursera-dl`, and `coursera_session`. 

##Dependencies
It's only dependency is the [requests](http://docs.python-requests.org/) module (version >= 2.0.0).

##File Structure
The script creats a directory for each course. The names of the directories are the names of the courses. The videos are then saved in the appropriate directory.

The script maintains state by pickling a python object to a file `.save_data`. Deleting this file will reset the state of the script; it will forget what it has and has not downloaded. Deleting this file will cause updates to download everything from the beginning - even if it already exists; be careful with this file!

##Notes
- The script can only download videos from courses you are enrolled in. Do not add courses that you are **not** enrolled in.
- The script will only download videos from active courses. It does not yet support *previews* and *archived* courses. Support for these modes will be added in the future.

##To-Do
- Support for downloading videos from *previews of courses* and *archived courses*.
- Support for other resources (pdfs, subtitles, code snippets, etc)
- Add `auto` mode to the `coursera add` function. This mode will automatically add all enrolled courses given account credentials

##About: **coursera-dl** module
This module implements a CLI using the `coursera_session` module. It maintains records of already downloaded videos and courses to monitor. It facilitates adding and removing of courses from the downloader, and updating added courses. The CLI is as follows:

```
  coursera-dl.py update [help | all | (course_id)...]
  coursera-dl.py courses add [help | (course_id)...]
  coursera-dl.py courses remove [help | all | (course_id)...]
  coursera-dl.py courses list
```

###coursera-dl update
This function is used to download new videos for added courses.

It accepts a list of course IDs, or the word `all`. Specifiying `all`
causes the downloader to update all added courses. Otherwise, only
specified courses are updated. For example, updating all courses:

`coursera-dl update all`

And to update only specific courses:

`coursera-dl update algo-001 crypto-01`

Courses will be updated in the order they are specified.

###coursera-dl courses add
This function allows you to add courses to the list of maintained courses. 
Course IDs should be separated by a space. An example of a valid command for this function is:

`coursera-dl courses add proglang-003 ml-008 mmds-01`

###coursera-dl courses remove
This function allows you to remove courses from the list of maintained courses. 
Course IDs should be separated by a space. In the case you wish to remove all courses 
(i.e, reset the state of the program), use `all` as the sole argument; for example:

`coursera-dl courses remove all`

Another example of a valid command for this function is:

`coursera-dl courses remove algo-001 crypto-01`

###coursera-dl courses list
This function will print a list of all added courses. It's use is very simple:

`coursera-dl courses list`


##About: **coursera_session** module
The `coursera_session` module provides a class `CourseraSession`. The class is derived from `requests.Session` - it forges a log in, and from that point provides functions for scraping information about a course, and to download videos. This module is not dependent on the `coursera-dl` module, it may be used for any purpose.

As of now, the `CourseraSession` class provides the following functions:

###log_in
Takes as arguments:

- **email** : string
- **password** : string

and forges a log in. After calling this function the session will emulate that of a logged in browser. The `email` and `password` are not stored anywhere during this function.

###download_video
Takes as arguments:

- **course_id** : string
- **video_id** : integer or string
- **chunk_size** : integer
- **directory** : string or None
- **callback** : function(bytearray, int, int, string)

and downloads a video of id `video_id` associated with a `course_id`. This function uses chunked transfer encoding (via Requests streams) to download the file; the `chunk_size` argument specifies the size of chunks to use. The `directory` argument specifies a directory to save the video; if this is None, the function will determine the name of the course, and use that as a directory. The `callback` function is called with the arguments (`chunk`, `byte_count`, `file_size`, `file_name`) whenever a chunk is saved.

###scrape_video_ids
Takes as arguments:

- **course_id** : string

and scrapes a list of video ids for all available videos for the course `course_id`.

###get_video_url
Takes as arguments:

- **course_id** : string
- **video_id** : int

and returns the url for the video described by `course_id` and `video_id`.

###get_course_name
Takes as arguments:

- **course_id** : string

and gets the name of the course of id `course_id`.