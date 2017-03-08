import os
import subprocess

# TODO: accept args for tree/token
with open('repos.txt', 'r') as file:
    for line in file:
        repo = line.split('/')[-1].split('.')[0]
        org = line.split('/')[-2]

        # clone the repo into /tmp
        p = subprocess.Popen("git clone {0}".format(line), shell=True).wait()

        p = subprocess.Popen("mv {0} /tmp/".format(repo), shell=True)

        # generate conflerge results for repo
        p = subprocess.Popen("./test_repo.sh {0} {1} tree".format(repo, org + '-' + repo), shell=True).wait()

        # remove the repo
        p = subprocess.Popen("rm -rf /tmp/{0}".format(repo), shell=True).wait()


results_dir = "."
csv_header = ""
csv_data = []

for filename in os.listdir(results_dir):

    if not filename.endswith(".csv"):
        continue

    with open(filename) as f:
        lines = f.readlines()
        csv_header = lines[0].strip()
        data = lines[1]

    num_conflicts = int(data.split(",")[1])
    csv_data.append(data)

with open("totals.csv", "w") as file:

    file.write(csv_header + "\n")

    sum_found = 0
    sum_resolved = 0
    sum_perf = 0
    sum_perf_noc = 0

    for line in csv_data:
        file.write(line + '\n')
        sum_found += int(line.split(",")[1])
        sum_resolved += int(line.split(",")[2])
        sum_perf += int(line.split(",")[3])
        sum_perf_noc += int(line.split(",")[4])

    file.write("TOTAL,"
        + str(sum_found) + ","
        + str(sum_resolved) + ","
        + str(sum_perf) + ","
        + str(sum_perf_noc) + ","
        + str(sum_resolved*100 // sum_found) + ","
        + str(sum_perf*100 // sum_resolved) + ","
        + str(sum_perf_noc*100 // sum_resolved) + "\n")