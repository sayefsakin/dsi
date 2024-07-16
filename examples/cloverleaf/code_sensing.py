#!/usr/bin/env python3

import argparse
import sys
import glob
import re

def recursive_match(re_list, search_file_list, cur_dir):
    """ The data is parsed from all of the files in the current directory """
    occurance = dict()
    for code_files in glob.iglob('**', root_dir=cur_dir, recursive=True):
        for f_type in search_file_list:
            if re.search(f_type + '$', code_files):
                with open(cur_dir + "/" + code_files, 'r') as cf:
                    line_number = 1
                    for line in cf:
                        for each_re in re_list:
                            line_match = re.compile(r"\s*[#]" + each_re + r"\s+(\w+)[\t\s]+(.*)\s*(\r\n|\r|\n)").match(line)
                            if line_match is not None:
                                c_line = "#" + each_re + " " + line_match.group(1)
                                second_part = line_match.group(2)
                                if second_part is not None and len(second_part) > 0:
                                    c_line = c_line + " " + line_match.group(2)
                                c_line = c_line.rstrip()
                                occurance[c_line] = occurance.get(c_line, dict())
                                # occurance[line]["first"] = line_match.group(1)
                                # occurance[line]["second"] = line_match.group(2)
                                occurance[c_line][code_files] = occurance[c_line].get(code_files, list())
                                occurance[c_line][code_files].append(line_number)
                        line_number = line_number + 1
    print("matching done")
    return occurance    

def main():
    """ A testname argument is required """
    parser = argparse.ArgumentParser()
    parser.add_argument('--testname', help='the test name')
    parser.add_argument('--gitdir', help='the git directory')
    args = parser.parse_args()
    # testname = "temp_test"
    testname = args.testname
    git_repo = args.gitdir
    if testname is None or git_repo is None:
        parser.print_help()
        sys.exit(0)

    re_list = ["pragma", "define"]
    search_file_list = [r"\.c", r"\.cc"]
    recursive_match(re_list, search_file_list, git_repo)

if __name__ == '__main__':
    main()

