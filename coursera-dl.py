import sys
import pickle
import getpass
import coursera_session

courses_done = {}

try:
    with open(".save_data", "rb") as f:
        courses_done = pickle.loads(f.read())
except:
    pass


def save_courses_done():
    with open(".save_data", "wb") as f:
        f.write(pickle.dumps(courses_done))


def download_callback(chunk, byte_count, file_size, file_name):
    if byte_count == len(chunk):
        print(" [*] ", file_name)
    filled = (48 * byte_count) // file_size
    progress = '=' * filled + ' ' * (48 - filled)
    args = (progress, float(byte_count)/(2**20), byte_count * 100. / file_size)
    status = " [*]%s| %.3f mb  [%3.2f%%]" % args
    print(status + chr(8)*(len(status)+1), end='')
    sys.stdout.flush()


def update(args):
    if not args or args[0] in ['help', '/?']:
        print(""" [H] This function is used to download new videos for registered courses.

It accepts a list of course IDs, or the word `all`. Specifiying all
causes the downloader to update all registered courses. Otherwise, only
specified courses are updated.""")
    else:
        if 'all' in args:
            args = courses_done.keys()
        email = input("Enter your email address: ")
        password = getpass.getpass("Enter your password: ")
        session = coursera_session.CourseraSession()
        session.log_in(email, password)

        for course_id in args:
            try:
                print("\n [****] Updating course", course_id)
                if course_id not in courses_done:
                    courses_done[course_id] = set()

                video_ids = session.scrape_video_ids(course_id)
                if not video_ids:
                    print(" [*] There are no videos to download for `%s`." % (course_id))
                else:
                    print(" [*]", len(video_ids), "videos to download")
                    print(" [*]")

                while video_ids:
                    video_id = video_ids.pop(0)
                    if video_id in courses_done[course_id]:
                        continue
                    session.download_video(course_id, video_id, callback=download_callback)
                    courses_done[course_id].add(video_id)
                    save_courses_done()
                    print("\n [*]")
            except:
                msg = "An error occured while downloading videos for `%s`. Try updating again later."
                print(msg % (course_id,))


def add_courses(args):
    if not args or args[0] in ['help', '/?']:
        print(""" [H] This function allows you to add courses to the list of maintained courses. 
Course IDs should be separated by a space. An example of a valid command for this function is:

    `coursera-dl courses add proglan-003 ml-008 mmds-01`""")
    else:
        for arg in args:
            if arg in courses_done:
                print(" [E] The course '%s' is already registered." % (arg,))
            else:
                courses_done[arg] = set()
        save_courses_done()


def remove_courses(args):
    if not args or args[0] in ['help', '/?']:
        print(""" [H] This function allows you to remove courses from the list of maintained courses. 
Course IDs should be separated by a space. In the case you wish to remove all courses 
(i.e, reset the state of the program), use `all` as the sole argument; for example:

        `coursera-dl courses remove all`

Another example of a valid command for this function is:

        `coursera-dl courses remove algo-001 crypto-01`""")
    elif 'all' in args:
        courses_done.clear()
        save_courses_done()
    else:
        for arg in args:
            if arg in courses_done:
                del courses_done[arg]
            else:
                print(" [E] The course '%s' is not currently registered." % (arg,))
        save_courses_done()


def print_course_list():
    for course in courses_done:
        print(" [*]", course)


def print_arg_error():
    print(" [E] Invalid parameters. Run with parameter 'help' to learn how to use this tool.")


def print_help():
    print("""The downloader""")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_help()

    elif len(sys.argv) == 2 and sys.argv[1] in ['help', '/?']:
        print_help()

    elif sys.argv[1] == 'courses':
        if len(sys.argv) == 2:
            print_arg_error()
        elif sys.argv[2] == 'add':
            add_courses(sys.argv[3:])
        elif sys.argv[2] == 'remove':
            remove_courses(sys.argv[3:])
        elif sys.argv[2] == 'list':
            print_course_list()
        else:
            print_arg_error()

    elif sys.argv[1] == 'update':
        update(sys.argv[2:])

    else:
        print_arg_error()