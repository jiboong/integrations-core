# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import os
from subprocess import PIPE, Popen
import time

# 3p
import memcache
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest

GAUGES = [
    "total_items",
    "curr_items",
    "limit_maxbytes",
    "uptime",
    "bytes",
    "curr_connections",
    "connection_structures",
    "threads",
    "pointer_size",

    # Computed metrics
    "get_hit_percent",
    "fill_percent",
    "avg_item_size"
]

RATES = [
    "rusage_user",
    "rusage_system",
    "cmd_get",
    "cmd_set",
    "cmd_flush",
    "get_hits",
    "get_misses",
    "delete_misses",
    "delete_hits",
    "evictions",
    "bytes_read",
    "bytes_written",
    "cas_misses",
    "cas_hits",
    "cas_badval",
    "total_connections",
    "listen_disabled_num"
]

# Not all rates/gauges reported by memcached test instance.
# This is the subset available with the default config/version.
ITEMS_RATES = [
    "evicted",
    "evicted_nonzero",
    "expired_unfetched",
    "evicted_unfetched",
    "outofmemory",
    "tailrepairs",
    "reclaimed",
    "crawler_reclaimed",
    "lrutail_reflocked",
]

ITEMS_GAUGES = [
    "number",
    "age",
    "evicted_time",
]

SLABS_RATES = [
    "get_hits",
    "cmd_set",
    "delete_hits",
    "incr_hits",
    "decr_hits",
    "cas_hits",
    "cas_badval",
    "touch_hits",
    "used_chunks",
]

SLABS_GAUGES = [
    "chunk_size",
    "chunks_per_page",
    "total_pages",
    "total_chunks",
    "used_chunks",
    "free_chunks",
    "free_chunks_end",
    "mem_requested",
]

SLABS_AGGREGATES = [
    "active_slabs",
    "total_malloced",
]

SERVICE_CHECK = 'memcache.can_connect'

PORT = 11212

@attr(requires='mcache')
class TestMemCache(AgentCheckTest):

    CHECK_NAME = "mcache"

    def setUp(self):
        c = memcache.Client(["localhost:{0}".format(PORT)])
        c.set("foo", "bar")
        c.get("foo")

    def testCoverage(self):
        config = {
            'init_config': {},
            'instances': [
                {'url': "localhost", 'port': PORT},
                {'url': "localhost", 'port': PORT, 'tags': ['instance:mytag']},
                {'url': "localhost", 'port': PORT, 'tags': ['foo']},
                {'socket': "foo/bar"}
            ]
        }

        self.assertRaises(Exception, self.run_check, config)

        tag_set = [
            ["url:localhost:11212"],
            ["url:localhost:11212", "instance:mytag"],
            ["url:localhost:11212", "foo"]
        ]

        for tags in tag_set:
            for m in GAUGES:
                self.assertMetric("memcache.{0}".format(m), tags=tags, count=1)

        good_service_check_tags = ["host:localhost", "port:{0}".format(PORT)]
        bad_service_check_tags = ["host:unix", "port:foo/bar"]

        self.assertServiceCheck(
            SERVICE_CHECK, status=AgentCheck.OK,
            tags=good_service_check_tags, count=3)
        self.assertServiceCheck(
            SERVICE_CHECK, status=AgentCheck.CRITICAL,
            tags=bad_service_check_tags, count=1)

        self.coverage_report()

        config = {
            'init_config': {},
            'instances': [
                {'url': "localhost", 'port': PORT},
                {'url': "localhost", 'port': PORT, 'tags': ['instance:mytag']},
                {'url': "localhost", 'port': PORT, 'tags': ['foo']},
            ]
        }

        self.run_check_twice(config, force_reload=True)
        for tags in tag_set:
            for m in GAUGES:
                self.assertMetric("memcache.{0}".format(m), tags=tags, count=1)
            for m in RATES:
                self.assertMetric(
                    "memcache.{0}_rate".format(m), tags=tags, count=1)

        good_service_check_tags = ["host:localhost", "port:{0}".format(PORT)]

        self.assertServiceCheck(
            SERVICE_CHECK, status=AgentCheck.OK,
            tags=good_service_check_tags, count=3)

        self.coverage_report()

    def _countConnections(self, port):
        pid = os.getpid()
        p1 = Popen(
            ['lsof', '-a', '-p%s' % pid, '-i4'], stdout=PIPE)
        p2 = Popen(["grep", ":%s" % port], stdin=p1.stdout, stdout=PIPE)
        p3 = Popen(["wc", "-l"], stdin=p2.stdout, stdout=PIPE)
        output = p3.communicate()[0]
        return int(output.strip())

    def testConnectionLeaks(self):
        for i in range(3):
            # Count open connections to localhost:11212, should be 0
            self.assertEquals(self._countConnections(11212), 0)
            new_conf = {'init_config': {}, 'instances': [
                {'url': "localhost", 'port': PORT}]
            }
            self.run_check(new_conf)
            # Verify that the count is still 0
            self.assertEquals(self._countConnections(11212), 0)

    def testOptionalItemsStats(self):
        config = {
            'init_config': {},
            'instances': [
                {'url': "localhost", 'port': PORT, 'tags': ['instance:mytag'], 'options': {'items': True}},
            ]
        }

        tags = ["url:localhost:11212", "instance:mytag"]

        self.run_check_twice(config, force_reload=True)
        for m in GAUGES:
            self.assertMetric("memcache.{0}".format(m), tags=tags, count=1)
        for m in RATES:
            self.assertMetric(
                "memcache.{0}_rate".format(m), tags=tags, count=1)

        for m in ITEMS_GAUGES:
            self.assertMetric("memcache.items.{0}".format(m), tags=tags+["slab:1"], count=1)
        for m in ITEMS_RATES:
            self.assertMetric(
                "memcache.items.{0}_rate".format(m), tags=tags+["slab:1"], count=1)

        self.assertServiceCheck(SERVICE_CHECK, status=AgentCheck.OK, tags=['host:localhost', 'port:11212'], count=1)

        self.coverage_report()

    def testOptionalSlabsStats(self):
        config = {
            'init_config': {},
            'instances': [
                {'url': "localhost", 'port': PORT, 'tags': ['instance:mytag'], 'options': {'slabs': True}},
            ]
        }

        tags = ["url:localhost:11212", "instance:mytag"]

        self.run_check_twice(config, force_reload=True)
        for m in GAUGES:
            self.assertMetric("memcache.{0}".format(m), tags=tags, count=1)
        for m in RATES:
            self.assertMetric(
                "memcache.{0}_rate".format(m), tags=tags, count=1)

        for m in SLABS_GAUGES:
            self.assertMetric("memcache.slabs.{0}".format(m), tags=tags+["slab:1"], count=1)
        for m in SLABS_AGGREGATES:
            self.assertMetric("memcache.slabs.{0}".format(m), tags=tags, count=1)
        for m in SLABS_RATES:
            self.assertMetric(
                "memcache.slabs.{0}_rate".format(m), tags=tags+["slab:1"], count=1)

        self.assertServiceCheck(SERVICE_CHECK, status=AgentCheck.OK, tags=['host:localhost', 'port:11212'], count=1)

        self.coverage_report()

    def testMemoryLeak(self):
        config = {
            'init_config': {},
            'instances': [
                {'url': "localhost", 'port': PORT},
                {'url': "localhost", 'port': PORT, 'tags': ['instance:mytag']},
                {'url': "localhost", 'port': PORT, 'tags': ['foo']},
            ]
        }

        self.run_check(config)

        import gc
        if not self.is_travis():
            gc.set_debug(gc.DEBUG_LEAK)
        gc.collect()
        try:
            start = len(gc.garbage)
            for i in range(10):
                self.run_check(config)
                time.sleep(0.3)
                self.check.get_metrics()

            end = len(gc.garbage)
            self.assertEquals(end - start, 0, gc.garbage)
        finally:
            gc.set_debug(0)
