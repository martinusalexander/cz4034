import os
import shlex
import subprocess

def main():
    elasticsearch_dir = os.path.join(os.path.join(os.getcwd(), 'search'), 'elasticsearch-2.4.1')
    if not os.path.exists(elasticsearch_dir):
        print("Elasticsearch not found... Please install...")
        return
    try:
        command = os.path.join(os.path.join(elasticsearch_dir, 'bin'), 'elasticsearch')
        args = shlex.split(command)
        print(command)
        # Reference: http://stackoverflow.com/a/4417735
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)

        for line in iter(process.stdout.readline, b''):
            print(line.rstrip())
        process.stdout.close()
        return_code = process.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, args)
    except KeyboardInterrupt:
        print('Stopped manually')
        exit()
    except subprocess.CalledProcessError as error:
        print('Elasticsearch encounters error')
        print(error)
        exit()



if __name__ == "__main__":
    # execute only if run as a script
    main()

