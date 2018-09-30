import argparse
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_lines(file):
    all_lines = []
    acc_lines = []
    loss_lines = []
    for cnt, line in enumerate(file):
        all_lines.append(line)
        if 'accuracy' in line:
            acc_lines.append(line)
            loss_lines.append(all_lines[cnt-1])
    return acc_lines,loss_lines


def get_acc_number(lines):
    accuracies = []
    for line in lines:
        m = re.findall(r'-?\d+\.?\d*', line)
        if m:
            found = m[0]
            accuracies.append(float(found))
    return accuracies

def get_loss_number(lines):
    accuracies = []
    for line in lines:
        m = re.findall(r'-?\d+\.?\d*', line)
        if m:
            found = m[1]
            accuracies.append(float(found))
    return accuracies

def get_evaluation(file):
    acc_lines, loss_lines = get_lines(file)
    accuracies = get_acc_number(acc_lines)
    losses = get_loss_number(loss_lines)
    return accuracies, losses

def plot(data_series,steps):
    plt.xlabel('iterations')
    for key, value in data_series.items():
        x = [i * steps for i in range(0,len(value))]
        plt.plot(x, value, label=key)
    plt.legend()
    plt.show()    

def main(file_path):
    # with open(file_path, "r") as f:
    #     accuracies, losses = get_evaluation(f)
    accuracy_1 = [98,80,72,10,24]
    accuracy_2 = [12,80,12,19,33]
    accuracy_series = {
        "train": accuracy_1,
        "val": accuracy_2
    }
    plot(accuracy_series,3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="log file to be parsed")
    args = parser.parse_args()
    file_path = args.file
    main(file_path)