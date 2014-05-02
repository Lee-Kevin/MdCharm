import os
import sys
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    if sys.argv[1] == "debug":
        if os.path.isfile("version.h"):
            print 'Already Exist'
            sys.exit(0)
    version_h = open('version.h.in').read()
    mdcharm_rc = open('mdcharm.rc.in').read()
    revision_output = os.popen('git log -1 --format="%H"')
    revision = None
    if revision_output:
        revision = str(revision_output.read()).strip()
    else:
        sys.exit(2)
    tag_output = str(os.popen('git tag').read()).strip()
    tag = None
    if tag_output:
        tag = tag_output.replace('\r\n', '\n').split('\n')[-1]
    else:
        sys.exit(3)
    if len(tag.split('.')) != 3:
        sys.exit(4)
    version_list = tag.split('.')
    ntime_str = datetime.now().strftime('%B %d %Y %H:%M:%S +0800')
    real_version_h = version_h.strip().format(tag,
                                              version_list[0],
                                              version_list[1],
                                              version_list[2],
                                              revision,
                                              ntime_str)
    result_file = file("version.h", 'w+')
    result_file.write(real_version_h)
    result_file.close()
    real_rc_file = mdcharm_rc.format(version_list[0], version_list[1], version_list[2], 0, tag)
    rc_file = file("../res/mdcharm.rc", 'w+')
    rc_file.write(real_rc_file)
    rc_file.close()
