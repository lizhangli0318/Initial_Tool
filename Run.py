# -*- coding: utf-8 -*-
import os
import sys
import yaml
import datetime


def find_all_robot_file(path):
    """
    find all robot files.
    """
    full_file_names = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        for file_name in file_names:
            if file_name.endswith('.robot'):
                full_file_names.append(dir_path + '/' + file_name)
    return full_file_names


def get_file_name_without_suffix(file_name, suffix):
    """
        get file name without suffix.
        """
    file_name_without_suffix = file_name.split('/')[-1].replace(suffix, '')
    return file_name_without_suffix


def get_test_cases_of_robot_file(file_name):
    cases_list = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("TC-"):
                cases_list.append(line)


def generate_cmd(robot_file, _cases_list: list = None):
    _cases_list_str = " -t ".join(_cases_list) if _cases_list else ""
    _cases_list_str = "-t %s" % _cases_list_str if _cases_list_str else ""
    robot_report = get_file_name_without_suffix(robot_file, '.robot')
    robot_output_file_name = robot_report + '/' + robot_report + '_output.xml'
    robot_report_file_name = robot_report + '/' + robot_report + '_report.html'
    robot_log_file_name = robot_report + '/' + robot_report + '_log.html'
    # get_test_cases_of_robot_file(robot_file)
    cmd_str = 'python -m robot.run -d "%s" -o "%s" -r "%s" -l "%s" %s %s' % (
        output_dir, robot_output_file_name, robot_report_file_name, robot_log_file_name, _cases_list_str,
        robot_file)
    return cmd_str


def run_cases_cmd_list(robots):
    cmd_list = []
    for robot_file in robots:
        cmd_list.append(generate_cmd(robot_file))
    return cmd_list


if __name__ == '__main__':
    if len(sys.argv) == 3:
        test_cases_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        with open("./Run.yaml", 'r', encoding='utf-8') as _yaml_file:
            _yaml_content = yaml.load(_yaml_file, Loader=yaml.SafeLoader)
            test_cases_dir = _yaml_content["Test_Cases"]
            cases_list = _yaml_content.get("Cases_List")
            output_dir = _yaml_content["Output"]
    _start_time = datetime.datetime.now()
    print("Start Time:" + _start_time.strftime('%Y-%m-%d %H:%M:%S'))
    if os.path.isdir(test_cases_dir):
        robot_files = find_all_robot_file(test_cases_dir)
        run_cmd_list = run_cases_cmd_list(robot_files)
        for cmd in run_cmd_list:
            print(cmd)
            os.system(cmd)
    else:
        run_cmd = generate_cmd(test_cases_dir, cases_list)
        print(run_cmd)
        os.system(run_cmd)
    _end_time = datetime.datetime.now()
    _elapse_time = (_end_time - _start_time).seconds
    print("End Time:" + _end_time.strftime('%Y-%m-%d %H:%M:%S'))
    print("Elapse Time: %d" % _elapse_time)
