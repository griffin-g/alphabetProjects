import psutil
import time
outFile = "scan.txt"


# Scan running processes. Store in dict. Key: PID, Value: proc.info
# proc.info: {'pid': xx, 'name': xx, 'username': xx}
def scanProcs():
    scan = {}
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        info = proc.info
        scan[info['pid']] = info
    return scan

# Compare scans.
# Return Started, Stopped, and Continuing Procs
def compareScans(old, new):
    oldPids = set(old.keys())
    newPids = set(new.keys())

    started = newPids - oldPids
    stopped = oldPids - newPids
    continuing = oldPids & newPids

    return {
        "started": [new[pid] for pid in started],
        "stopped": [old[pid] for pid in stopped],
        "continuing": [new[pid] for pid in continuing]
    }

if __name__ == "__main__":
    scan1 = scanProcs()
    time.sleep(5)
    scan2 = scanProcs()

    diff = compareScans(scan1, scan2)

    print("Started:")
    for p in diff["started"]:
        print(p)

    print("\nStopped:")
    for p in diff["stopped"]:
        print(p)



