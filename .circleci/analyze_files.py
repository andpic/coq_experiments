#!/usr/bin/python3
#
# analyze_files.py - Compile and analyze all the Coq files in the project.

import os, sys, subprocess


def _find_all_coq_files(folder_path):
    """ Find all the Coq files in folder_path and its sub-folders. """

    coq_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".v"):
                coq_files.append(os.path.join(root, file))
    return coq_files

def _write_to_log(a_string, log_file):
    """ Write a string to the log """

    log_file.flush()
    print(a_string, file=log_file)
    log_file.flush()


def _coqchk_file_identifier(file_name):
    """ Workaround for differences between Linux and Windows """

    if os.name == 'nt':
        return file_name + ".vo"
    else:
        return file_name


def _analyze_single_file(file_path, detailed_log_path):
    """ Process and analyze the input file """
    
    folder_path = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    initial_folder_path = os.getcwd()
    os.chdir(folder_path)

    return_codes = []

    with open(detailed_log_path, "a+") as detailed_log:
        _write_to_log("=== Processing " + file_name, detailed_log)

        # Compile file
        file_identifier_coqc = file_name + ".v"
        _write_to_log("Calling coqc " + file_identifier_coqc, detailed_log)
        return_codes.append(
            subprocess.call(["coqc", file_identifier_coqc], 
                stdout=detailed_log,                 
                stderr=detailed_log))

        # Check proofs
        file_identifier_coqckh = _coqchk_file_identifier(file_name)
        _write_to_log("Calling coqchk " + file_identifier_coqckh, detailed_log)
        return_codes.append(
            subprocess.call(["coqchk", file_identifier_coqckh],
                stdout=detailed_log, 
                stderr=detailed_log))

    os.chdir(initial_folder_path)
    return all(code == 0 for code in return_codes)


def main(folder_path, detailed_log_path):
    all_files = _find_all_coq_files(folder_path)
    detailed_log_path = os.path.realpath(detailed_log_path)

    check_passed = []
    for file in all_files:
        print("Analyzing " + file + "... ", end = '')
        passed = _analyze_single_file(file, detailed_log_path)
        check_passed.append(passed)

        if passed:
            print("PASSED")
        else:
            print("FAILED")

    if all(code == True for code in check_passed):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])