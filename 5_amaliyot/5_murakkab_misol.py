# 7.df -h natijasidan bo‘sh joyi 10% dan kam bo‘lgan disklarni kamjoy.log fayliga yozing.
import subprocess

def log_low_space_disks(threshold=50, logfile="kamjoy.log"):
    # df -h buyrug‘ini ishlatamiz
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")

    header = lines[0]
    disks = lines[1:]

    low_space = []
    for line in disks:
        parts = line.split()
        if len(parts) < 5:
            continue
        usage_str = parts[4]  # %Usage ustuni
        if usage_str.endswith("%"):
            usage = int(usage_str[:-1])
            free = 100 - usage
            if free < threshold:
                low_space.append(line)

    # Natijani log faylga yozamiz
    with open(logfile, "w") as f:
        f.write(header + "\n")
        for disk in low_space:
            f.write(disk + "\n")

    print(f"{len(low_space)} ta kam joyli disk '{logfile}' fayliga yozildi.")

if __name__ == "__main__":
    log_low_space_disks()
