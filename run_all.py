import os

METHOD_PATHS = [
    r"./alda/runner.py",
    r"./traffic_lights_static_alda/runner.py",
    r"./traffic_lights_static/runner.py",
]

# for path in METHOD_PATHS:
#     output = path.split(r"/")[1]
#     os.system(f"python3 {path} > output/{output}.txt")
name = METHOD_PATHS[0].split(r"/")[1]
os.system(f'runas /user:PhD "python3 {METHOD_PATHS[0]} --output_path output/{name}.txt > output/logs.txt"')
# os.system(f"python3 {METHOD_PATHS[0]} --output_path output/{name}.txt> output/logs.txt")

# import subprocess
#
# def main():
#     # List of Python scripts you want to execute with admin rights
#     script_list = [
#         r"./alda/runner.py",
#         r"./traffic_lights_static_alda/runner.py",
#         r"./traffic_lights_static/runner.py",
#     ]
#
#     # Output file path to save the output of each script
#     output_file = "output.txt"
#
#     with open(output_file, "w") as f:
#         for script_path in script_list:
#             # Run the script with admin rights and capture its output
#             command = f'runas /PhD:Administrator "python3 {script_path}"'
#             output = subprocess.check_output(command, shell=True)
#             output_str = output.decode("utf-8")

            # Write the output to the output file
#             f.write(f"Output for {script_path}:\n")
#             f.write(output_str)
#             f.write("\n\n")
#
#
# if __name__ == "__main__":
#     main()
