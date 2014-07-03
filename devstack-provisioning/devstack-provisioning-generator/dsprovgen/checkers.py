import os

# Examples of the possible validation

def check_host_exists(host):
    # not the most portable way of doing so, but for now will suffice
    if os.system("ping -o -c 3 -W 3000 %s > /dev/null 2>&1" % host.hostname) != 0:
        _validation_error("%s: host is not reachable" % host.hostname, host)
        return False

    return True


def check_fixed_range_exists(host):
    fixed_range = _check_key_exists("devstack.fixed_range", host)
    if len(fixed_range.split("/")) != 2:
        _validation_error("devstack.fixed_range must follow the pattern of <ip>/<net_mask>", host)
        return False

    return True


# INTERNAL

_BG_HEADER = '\033[95m'
_BG_OKBLUE = '\033[94m'
_BG_OKGREEN = '\033[92m'
_BG_WARNING = '\033[93m'
_BG_FAIL = '\033[91m'
_BG_ENDC = '\033[0m'


def _validation_error(message, host):
    print _BG_FAIL + message + _BG_ENDC
    print "\nThe failure appeared when processing the host:\n"
    print host


def _check_key_exists(key, host):
    def find_entry(k, d):
        if k[0] in d:
            if len(k) == 1:
                return d[k[0]]
            else:
                return find_entry(k[1:], d[k[0]])
        else:
            _validation_error("Key %s is not defined" % key, host)

    return find_entry(key.split("."), host.config)