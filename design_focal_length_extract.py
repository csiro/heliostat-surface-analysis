import os

scans_dir = r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\old-scans\newcastle-field-2"

with open(os.path.join(scans_dir, "designfocallengths.txt"), "w") as file:        
    for scan_file in os.listdir(os.path.join(scans_dir, "scans")):
        scan_name = scan_file.split(".")[0]
        parts = scan_name.split("-")
        focal_length = parts[1][2:]
        file.write(f"{scan_name}\t{focal_length}\n")
