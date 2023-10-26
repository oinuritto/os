import os
import sys
import random


def parent_process(num_children):
    pid = os.getpid()
    children = []

    for _ in range(num_children):
        start_child(children, pid)

    for _ in children:
        child_pid, status = os.wait()
        exit_code = int(status / 256)
        print(f"Parent[{pid}]: Child with PID {child_pid} terminated. Exit Status {exit_code}.")
        if exit_code != 0:
            start_child(children, pid)


def start_child(children, pid):
    child_pid = os.fork()
    if child_pid == 0:
        sleep_time = random.randint(5, 10)
        child_args = ['child.py', str(sleep_time)]

        # пришлось использовать chmod +x child.py, иначе Permission denied
        os.execve('child.py', child_args, os.environ)
    else:
        children.append(child_pid)
        print(f"Parent[{pid}]: I ran children process with PID {child_pid}.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parent.py <number_of_children>")
        sys.exit(1)

    num_children = int(sys.argv[1])
    parent_process(num_children)
