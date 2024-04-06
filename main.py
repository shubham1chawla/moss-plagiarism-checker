#!./.venv/bin/python

import logging as log
from argparse import ArgumentParser
from src.checker import MossPlagiarismChecker

parser = ArgumentParser()
parser.add_argument('--students', '-S', type=str, help='Students CSV file path.', required=True)
parser.add_argument('--homeworks-dir', '-H', type=str, help='Directory containing all homeworks.', required=True)
parser.add_argument('--report-dir', '-R', type=str, help='Export directory for all the reports.', required=True)
parser.add_argument('--moss-userid', '-U', type=int, help='MOSS user id.', required=True)
parser.add_argument('--moss-tag', '-T', type=str, help='Report name given to MOSS report.', required=True)
args = parser.parse_args()

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)

    checker = MossPlagiarismChecker(args.students, args.homeworks_dir)
    checker.export_javascript_reports(args.report_dir)
    checker.perform_moss_plagiarism_test(args.report_dir, args.moss_userid, args.moss_tag)
