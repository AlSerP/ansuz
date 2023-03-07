from tester.cpp_runner import run_cpp
from tester.python_runner import run_py
from tester.test_ssh import ssh_compile_cpp, ssh_run_cpp
# from cpp_runner import run_cpp
# from python_runner import run_py
from subprocess import call, PIPE
from django.conf import settings
import json

def test_solution(file, input, output):
    type = file.split('.')[-1]
    file_path = file
    if type == 'cpp':
        # return test_cpp(settings.MEDIA_ROOT + '/' + file, input, output)
        return test_cpp(settings.MEDIA_ROOT + '/' + file, input, output)
    if type == 'py':
        return test_py(settings.MEDIA_ROOT + '/' + file, input, output)
    else:
        # ERROR MESSAGE
        pass


def test_cpp(file, input, output):
    report = {}
    # status = run(['/usr/bin/g++', file], stdout=PIPE, stderr=PIPE)
    # status = run(['ls'], stdout=PIPE, stderr=PIPE)
    status = ssh_compile_cpp(file)
    status = status.decode()
    my_file = open("LOGS.txt", "a")
    my_file.write(status + ' WGWERGWE')
    my_file.close()
    
    if status:
        # Error case
        report['return_code'] = 'ER'
        report['message'] = status

    else:
        correctness = True
        correct_counter = 0

        report['results'] = []
        in_list, out_list = json.loads(input), json.loads(output)
        tests_number = len(in_list)
        for i, question, answer in zip(range(1, tests_number + 1), in_list, out_list):
            program_out = ssh_run_cpp(question)

            test_correctness = (str(answer) == str(program_out))
            correctness *= test_correctness
            correct_counter += test_correctness

            result = {}
            result['test'] = i
            result['input'] = question
            result['output'] = program_out
            result['answer'] = answer
            result['is_correct'] = test_correctness

            report['results'].append(result)

        if correctness:
            report['return_code'] = 'CO'
        else:
            report['return_code'] = 'WR'

        report['tests_passed'] = correct_counter
        report['tests_number'] = tests_number
        report['mark'] = correct_counter * 100 // tests_number

    # with open('data.json', 'w') as outfile:
    #     json.dump(report, outfile)
    return report

def test_py(file, input, output):
    report = {}

    correctness = True
    correct_counter = 0
    report['results'] = []
    
    in_list, out_list = json.loads(input), json.loads(output)
    # in_list, out_list = input, output
    tests_number = len(in_list)

    for i, question, answer in zip(range(1, tests_number + 1), in_list, out_list):
        # code, program_out = run_py(file, question)
        code, program_out = run_py(file, question)
        if code == 'ER':
            report['return_code'] = 'ER'
            report['message'] = program_out
            return report

        test_correctness = (str(answer) == str(program_out))
        correctness *= test_correctness
        correct_counter += test_correctness

        result = {}
        result['test'] = i
        result['input'] = question
        result['output'] = program_out
        result['answer'] = answer
        result['is_correct'] = test_correctness

        report['results'].append(result)

    if correctness:
        report['return_code'] = 'CO'
    else:
        report['return_code'] = 'WR'

    report['tests_passed'] = correct_counter
    report['tests_number'] = tests_number
    report['mark'] = correct_counter * 100 // tests_number

    return report

if __name__ == "__main__":
    print(test_cpp('test.cpp', '["1", "2"]', '["2 - 3", "3 - 6"]'))
