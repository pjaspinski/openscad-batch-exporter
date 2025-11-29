import csv
import sys
import subprocess
import os
import time
from concurrent.futures import ProcessPoolExecutor

OUTPUT_PATH = 'output'
NUMBER_OF_PARALLEL_RENDERS = 4

csv_file_path = sys.argv[1]
project_file_path = sys.argv[2]

def prepare_output_dir():
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
        return
    files = os.listdir(OUTPUT_PATH);
    for file in files:
        os.remove(f'{OUTPUT_PATH}/{file}')

def get_command(var_names, var_values):
    parts = ["openscad", "--export-format", "binstl", "-o"]
    output_file_name = f'{OUTPUT_PATH}/{"_".join(var_values)}.stl'
    parts.append(output_file_name)
    for name, value in zip(var_names, var_values):
        parts.append("-D")
        parts.append(f'{name}="{value}"')
    parts.append(project_file_path)
    return parts

def generate_stl(command):
    print(f'Executing command: {subprocess.list2cmdline(command)}')
    start = time.time();
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(result.stdout)
    print(result.stderr)
    print(f'Completed in: {time.time() - start}s')


if __name__ == '__main__':
    prepare_output_dir()

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        headers = next(reader)
        commands = []
        for row in reader:
            commands.append(get_command(headers, row))

    print(f'Generating {len(commands)} objects.')

    with ProcessPoolExecutor(max_workers = NUMBER_OF_PARALLEL_RENDERS) as executor:
        executor.map(generate_stl, commands)

