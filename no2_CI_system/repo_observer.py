import argparse
import os
import subprocess
import helpers
import time
import socket

def poll():
    # use parser for command-line parsing in Python
    # see more at https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    # We must also give the observer the dispatcher's address,
    # so the observer may send it messages. 
    parser.add_argument("--dispatcher-server", 
            help="dispatcher has to respect the syntax: host:port, "\
                    "by default it uses localhoast:8888",
            default="localhost:8888", action="store_true")

    parser.add_argument("repo", metavar="repository", type=str,
            help="path to the repository this will observe")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")

    while True:
        try:
            # call the bash script that will update the repo and check for changes.
            # If there's a change, it will drop a .commit_id file with the latest commit
            # in the current working directory
            subprocess.check_output(["./update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception("could not update and check repository. Reason: %s" % e.output)

        if os.path.isfile(".commit_id"):
            # great, we have a change! Let's execute the tests
            # First, check the status of the dispatcher server to see
            # if we can send the tests

            try:
                response = helpers.communicate(dispatcher_host, int(dispatcher_port), "status")

            except socket.error as e:
                raise Exception("Could not communicate with dispatcher server: %s" %e)

            if response == "OK":
                # Dispatcher is present, let's send it a test
                commit = ""
                with open(".commit_id", "r") as f:
                    commit = f.readline() # read the newest commit that is stored in '.commit_id' file
                # send the commit ID to the dispatcher
                response  = helpers.communicate(dispatcher_host, int(dispatcher_port),
                        "dispatcher: %s" % commit)

                if response != "OK":
                    raise Exception("Could not dispatcher the test %s" % response)
                print("dispatched!")
            else:
                # Something wrong happened to the dispatcher
                raise Exception("Could not dispatch the test: %s" % response)
        
        time.sleep(5)

if __name__ == "__main__":
    poll()

