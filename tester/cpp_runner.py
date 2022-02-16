from subprocess import Popen, PIPE, run


def run_cpp(in_data):
    # file_cpp = file
    # run(['g++', file_cpp])  # Compile file

    p = Popen(['a.exe'], shell=True, stdout=PIPE, stdin=PIPE)  # Run file
    value = bytes(str(in_data) + '\n', 'UTF-8')
    p.stdin.write(value)
    p.stdin.flush()
    result = p.stdout.readline().strip().decode()
    # TODO: Check result errors
    return result


if __name__ == "__main__":
    print(run_cpp(int(input())))
