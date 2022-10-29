from subprocess import Popen, PIPE, run


def run_py(file, in_data):
    p = Popen('python ' + file, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)  # Run file
    value = bytes(str(in_data) + '\n', 'UTF-8')
    p.stdin.write(value)
    p.stdin.flush()

    result = p.stdout.readline().strip().decode()
    code = 'CO'

    if p.stderr:
        code = 'ER'
        result = p.stderr.readline().strip().decode()
    
    return code, result


# if __name__ == "__main__":
#     print(test_py('test.py', [1, 2, 3, 4], [2, 4, 6, 8]))
