import psutil
import io


def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception:
        pass
    return False


def to_gib(bytes, factor=2 ** 30, suffix="GiB"):
    """ Convert a number of bytes to Gibibytes

        Ex : 1073741824 bytes = 1073741824/2**30 = 1GiB
    """
    return "%0.2f%s" % (bytes / factor, suffix)


def get_stats(filters=None):
    if filters is None:
        filters = {}
    results = {}

    if True:
        results['cpus'] = tuple("%s%%" % x for x in psutil.cpu_percent(percpu=True))

    if filters.get('show_memory', True):
        try:
            memory = psutil.phymem_usage()
            results['memory'] = '{used}/{total} ({percent}%)'.format(
                used=to_gib(memory.used),
                total=to_gib(memory.total),
                percent=memory.percent
            )
        except Exception:
            pass

    if True:
        disks = {}
        for device in psutil.disk_partitions():
            # skip mountpoint not actually mounted (like CD drives with no disk on Windows)
            if device.fstype != "":
                usage = psutil.disk_usage(device.mountpoint)
                disks[device.mountpoint] = '{used}/{total} ({percent}%)'.format(
                    used=to_gib(usage.used),
                    total=to_gib(usage.total),
                    percent=usage.percent
                )
        results['disks'] = disks
    return results

