import os
import argparse
from timeit import default_timer as timer

DIST_NAME = "find_in_file"
BLOCK_SIZE_MULTIPLIER = 500  # read block size multiplier
ARGS = {}


def parse_args():
    arg_parser = argparse.ArgumentParser(DIST_NAME, formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('search_term', type=str)
    arg_parser.add_argument('filename', type=str)
    ARGS.update(vars(arg_parser.parse_args()))
    ARGS["block_size"] = os.statvfs(os.path.expanduser(ARGS["filename"]))[0]  # Get file system default block size (f_bsize)
    ARGS["read_size"] = ARGS["block_size"] * BLOCK_SIZE_MULTIPLIER


def find_last_line(end, fd):
    fd.seek(end)
    block_number = 1
    last_line_pos = -1
    blocks = ""
    position = end
    # print(position)

    while position != 0:
        position = max(0, position - ARGS["read_size"])
        # print(position)
        fd.seek(position, 0)
        blocks = fd.read(ARGS["read_size"]) + blocks

        last_line_pos = blocks.rfind("\n", 0, len(blocks))
        if last_line_pos != -1:
            break

        block_number += 1

    if last_line_pos > 0:
        position += last_line_pos + 1

    fd.seek(position, 0)

    # print(position, last_line_pos, len(blocks))

    return fd.readline(len(ARGS["search_term"])), position


def binary_find(start, end, fd):
    # Did not find / empty file
    if start == end:
        # print("Not Found1")
        return ""

    first_line, pos_first = find_last_line(start, fd)
    last_line, pos_last = find_last_line(end, fd)
    # print("************************************************************************************************")
    # print(f"{first_line} *** {last_line}")
    # print("************************************************************************************************")
    if first_line >= ARGS["search_term"]:
        # print("First line bigger")
        fd.seek(pos_first, 0)
        return fd.readline()

    if last_line < ARGS["search_term"]:
        # print("Not Found")
        return ""

    mid = (end + start) // 2
    mid_line, pos_mid = find_last_line(mid, fd)

    if mid_line > ARGS["search_term"]:
        if mid_line == last_line:  # first < so it means that last line is the first <=
            fd.seek(pos_last, 0)
            return fd.readline()

        # print(f"LEFT {mid_line} {mid}")
        return binary_find(start, mid, fd)

    elif mid_line < ARGS["search_term"]:
        if mid_line == first_line:  # first < so it means that last line is the first <=
            fd.seek(pos_last, 0)
            return fd.readline()

        # print(f"RIGHT, {mid_line} {mid}")
        return binary_find(mid, end, fd)

    # Equals
    else:
        # print("Equals")
        fd.seek(pos_mid, 0)
        return fd.readline()


def main():
    parse_args()

    # print(ARGS)
    # return
    start = timer()
    with open(os.path.expanduser(ARGS["filename"]), mode="r") as fd:
        fd.seek(0, 2)
        end = fd.tell()
        # print(f"File size: {end} bits")
        result = binary_find(0, end, fd)

    end = timer()
    print(result)
    print(f"finished {end - start} seconds")

