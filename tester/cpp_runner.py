from subprocess import Popen, PIPE

def run_cpp(in_data):
    p = Popen(['./a.out'], shell=True, stdout=PIPE, stdin=PIPE)  # Run file
    value = (str(in_data) + '\n').encode('utf-8')
    p.stdin.write(value)
    p.stdin.flush()
    result = p.stdout.readline().strip().decode()
    return result


if __name__ == "__main__":
    print(run_cpp(int(input())))
