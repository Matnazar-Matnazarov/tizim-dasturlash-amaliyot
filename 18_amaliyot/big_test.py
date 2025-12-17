with open("big.txt", "w") as f:
    for i in range(1, 1_000_001):
        f.write(f"Line {i}: INFO message\n")

    f.write("CRITICAL ERROR FOUND HERE 1\n")
    f.write("Another ERROR just for test\n")
    f.write("ERROR final marker\n")
