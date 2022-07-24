import os
import stat
from tester.cpp_runner import run_cpp
from subprocess import run, CompletedProcess
import json


def test_cpp(file: str, input: list, output: list) -> dict:
    report = {}
    # try:
    #     status = run(['g++', 'media/' + file], capture_output=True)  # Compile file
    # except:
    #     report = {}
    #     report['return_code'] = 'ER'
    #     return report

    status = run(['g++', 'media/' + file], capture_output=True)

    if status.returncode == 1:
        # Error case
        # print(status.stderr.decode())
        report['return_code'] = 'ER'
        # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        # print(status.stdout.decode().split('media/'))
        # print(status.stderr.decode())
        # report['message'] = status.stdout.decode()
        report['message'] = status.stderr.decode()
        # return False

    else:
        correctness = True
        correct_counter = 0

        report['results'] = []
        in_list, out_list = json.loads(input), json.loads(output)
        tests_number = len(in_list)
        for i, question, answer in zip(range(1, tests_number + 1), in_list, out_list):
            program_out = run_cpp(question)

            test_correctness = (answer == program_out)
            correctness *= test_correctness
            correct_counter += test_correctness

            result = {}
            result['test'] = i
            result['input'] = question
            result['output'] = program_out
            result['answer'] = answer
            result['is_correct'] = test_correctness

            report['results'].append(result)
            # tests_results.append([i, test_correctness, question, answer, program_out])

        if correctness:
            report['return_code'] = 'CO'
        else:
            report['return_code'] = 'WR'

        report['tests_passed'] = correct_counter
        report['tests_number'] = tests_number
        report['mark'] = correct_counter * 100 // tests_number
        # return [correctness, f'passed {correct_counter}/{tests_number} tests', tests_results]

    # with open('data.json', 'w') as outfile:
    #     json.dump(report, outfile)
    return report


if __name__ == "__main__":
    # print(test_cpp('.\\tester\\main.cpp', ['1 2', '2 2', '3 3', '4 1'], ['6', '8', '12', '10']))
    print(test_cpp(input(), ['1 2', '2 2', '3 3', '4 1'], ['6', '8', '12', '10']))
