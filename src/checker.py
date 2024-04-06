import logging as log
import os
import pandas as pd
from typing import Final
from urllib.request import urlretrieve
from subprocess import Popen
from src.student import Student

class MossPlagiarismChecker:

    MOSS_SCRIPT_LINK: Final[str] = 'http://moss.stanford.edu/general/scripts/mossnet'
    JAVASCRIPT_REPORT_NAME: Final[str] = 'overall_javascript_report.csv'
    CONVENTION_REPORT_NAME: Final[str] = 'convention_report.csv'
    MULTIPLE_JS_REPORT_NAME: Final[str] = 'multi_javascript_report.csv'
    MOSS_REPORT_NAME: Final[str] = 'moss_report.log'

    students: list[Student]

    def __init__(self, students_csv: str, homeworks_directory: str) -> None:
        df = pd.read_csv(students_csv)
        self.students = []
        for directory in os.listdir(homeworks_directory):
            github_username = '-'.join(directory.split('-')[2:])
            student_record = df[df['github_username'] == github_username]
            if student_record.shape[0] == 0:
                log.warn(f'No student record found for \'{directory}\'')
            elif student_record.shape[0] > 1:
                log.warn(f'More than 1 students found corresponding to \'{directory}\'')
            else:
                student = Student(student_record.iloc[0,:], os.path.join(homeworks_directory, directory))
                self.students.append(student)
        log.info(f'Loaded {len(self.students)} students from \'{students_csv}\'')

    
    def export_javascript_reports(self, test_directory: str) -> None:
        report = []
        for student in self.students:
            report.append({
                'asurite': student.asurite,
                'github_username': student.github_username,
                'js_files': len(student.javascripts),
                'naming_convention': len([javascript for javascript in student.javascripts if student.asurite in javascript]) > 0
            })
        df = pd.DataFrame(report)
        overall_javascript_report_path = os.path.join(test_directory, self.JAVASCRIPT_REPORT_NAME)
        df.to_csv(overall_javascript_report_path, index=False)
        log.info(f'Exported overall javascript report to \'{overall_javascript_report_path}\'')
        
        incorrect_convention_df = df[df['naming_convention'] == False]
        if incorrect_convention_df.shape[0] > 0:
            log.warn(f'Following students didn\'t follow \'asurite.js\' naming convention\n{incorrect_convention_df}')
            convention_report_path = os.path.join(test_directory, self.CONVENTION_REPORT_NAME)
            incorrect_convention_df.to_csv(convention_report_path, index=False)
            log.info(f'Exported naming convention report to \'{convention_report_path}\'')

        multiple_js_files_df = df[df['js_files'] > 1]
        if multiple_js_files_df.shape[0] > 0:
            log.warn(f'Following students have multiple javascript files\n{multiple_js_files_df}')
            multiple_js_report_path = os.path.join(test_directory, self.MULTIPLE_JS_REPORT_NAME)
            multiple_js_files_df.to_csv(multiple_js_report_path, index=False)
            log.info(f'Exported multiple javascript files report to \'{multiple_js_report_path}\'')


    def perform_moss_plagiarism_test(self, test_directory: str, moss_user_id: int, moss_tag: str) -> None:
        combined_js_directory = os.path.join(test_directory, 'js')
        if not os.path.isdir(combined_js_directory):
            os.mkdir(combined_js_directory)
        for student in self.students:
            with open(os.path.join(combined_js_directory, f'{student.asurite}.js'), 'w') as combined_file:
                for javascript in student.javascripts:
                    combined_file.write(f'// START OF FILE - {javascript}\n\n')
                    with open(javascript, 'r') as js_file:
                        combined_file.write(js_file.read())
                    combined_file.write(f'\n\n// END OF FILE - {javascript}\n\n')
        log.info(f'Exported combined javascript files to: {combined_js_directory}')

        moss_script_path = os.path.join(test_directory, 'moss.pl')
        if os.path.exists(moss_script_path):
            log.info(f'Removing previous moss script file from \'{moss_script_path}\'')
            os.remove(moss_script_path)
        urlretrieve(self.MOSS_SCRIPT_LINK, moss_script_path)

        script_lines = []
        with open(moss_script_path, 'r') as file:
            for line in file.readlines():
                if line.startswith('$userid'):
                    script_lines.append(f'$userid={moss_user_id};')
                else:
                    script_lines.append(line)
        with open(moss_script_path, 'w') as file:
            file.writelines(script_lines)

        Popen(['chmod', '+x', moss_script_path])
        moss_script_cmds = [
            moss_script_path, 
            '-l', 
            'javascript', 
            '-c', 
            f'"{moss_tag}"'
        ]
        for combined_file_path in os.listdir(combined_js_directory):
            if combined_file_path.endswith('js'):
                moss_script_cmds.append(os.path.join(combined_js_directory, combined_file_path))
        
        moss_report_path = os.path.join(test_directory, self.MOSS_REPORT_NAME)
        with open(moss_report_path, 'w') as file:
            Popen(moss_script_cmds, stdout=file).wait()      
        log.info(f'Exported moss script output to \'{moss_report_path}\'')
