from subprocess import Popen, PIPE


def run_py(file, in_data):
    p = Popen('python3 ' + file, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)  # Run file
    #print(str(in_data))
    # value = bytes(str(in_data) + '\n', 'UTF-8')
    value = (str(in_data) + '\n').encode('utf-8')
    p.stdin.write(value)
    p.stdin.flush()

    result = p.stdout.readline().strip().decode()
    error = p.stderr.readline().strip().decode()
    code = 'CO'

    if error:
        code = 'ER'
        result = error
    
    return code, result


if __name__ == "__main__":
    print(run_py('test.py', 5))
