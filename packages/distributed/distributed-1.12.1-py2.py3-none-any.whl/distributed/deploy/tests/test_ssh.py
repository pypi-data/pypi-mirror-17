from __future__ import print_function, division, absolute_import

from time import sleep, time

import pytest
pytest.importorskip('paramiko')

from distributed import Executor
from distributed.deploy.ssh import SSHCluster
from distributed.utils_test import slow
from distributed.utils_test import loop

@pytest.mark.avoid_travis
def test_cluster(loop):
    with SSHCluster(scheduler_addr = '127.0.0.1',
                    scheduler_port = 7437,
                    worker_addrs = ['127.0.0.1', '127.0.0.1']) as c:
        with Executor(c, loop=loop) as e:
            start = time()
            while len(e.ncores()) != 2:
                sleep(0.01)
                assert time() < start + 5

            c.add_worker('127.0.0.1')

            start = time()
            while len(e.ncores()) != 3:
                sleep(0.01)
                assert time() < start + 5
