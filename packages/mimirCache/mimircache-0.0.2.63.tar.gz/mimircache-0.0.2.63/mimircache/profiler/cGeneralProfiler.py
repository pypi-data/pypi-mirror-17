""" this module is used for all other cache replacement algorithms excluding LRU(LRU also works, but slow compared to
    using pardaProfiler),
"""
# -*- coding: utf-8 -*-


import math
import os, sys

# deal with headless situation
import traceback

import matplotlib

from multiprocessing import Process, Pipe, Array
from os import path

from mimircache.utils.printing import colorfulPrint

from mimircache.profiler.LRUProfiler import LRUProfiler

from mimircache.cacheReader.vscsiReader import vscsiReader
import matplotlib.ticker as ticker

from mimircache.cacheReader.plainReader import plainReader

import mimircache.c_generalProfiler as c_generalProfiler

import matplotlib.pyplot as plt

from mimircache.const import c_available_cache, cache_alg_mapping
from mimircache.profiler.abstract.abstractProfiler import profilerAbstract
from mimircache.const import *


class cGeneralProfiler:
    def __init__(self, reader, cache_name, cache_size, bin_size=-1, cache_params=None,
                 num_of_threads=DEFAULT_NUM_OF_THREADS):
        assert cache_name.lower() in cache_alg_mapping, "please check your cache replacement algorithm: " + cache_name
        assert cache_name.lower() in c_available_cache, \
            "cGeneralProfiler currently only available on the following caches: {}\n, " \
            "please use generalProfiler".format(c_available_cache)

        self.reader = reader
        self.cache_size = cache_size
        self.cache_name = cache_alg_mapping[cache_name.lower()]
        if bin_size == -1:
            self.bin_size = int(self.cache_size / DEFAULT_BIN_NUM_PROFILER)
            if self.bin_size == 0:
                self.bin_size =1
        else:
            self.bin_size = bin_size
        self.cache_params = cache_params
        self.num_of_threads = num_of_threads

        # if the given file is not basic reader, needs conversion
        need_convert = True
        for instance in c_available_cacheReader:
            if isinstance(reader, instance):
                need_convert = False
                break
        if need_convert:
            self.prepare_file()

    all = ["get_hit_count", "get_hit_rate", "get_miss_rate", "plotMRC", "plotHRC"]

    def prepare_file(self):
        self.num_of_lines = 0
        with open('temp.dat', 'w') as ofile:
            i = self.reader.read_one_element()
            while i is not None:
                self.num_of_lines += 1
                ofile.write(str(i) + '\n')
                i = self.reader.read_one_element()
        self.reader = plainReader('temp.dat')


    def get_hit_count(self, **kwargs):
        """

        :return: a numpy array, with hit count corresponding to size [0, bin_size, bin_size*2 ...]
        """
        sanity_kwargs = {}
        if 'num_of_threads' not in kwargs:
            sanity_kwargs['num_of_threads'] = self.num_of_threads
        else:
            sanity_kwargs['num_of_threads'] = kwargs['num_of_threads']
        if 'cache_size' in kwargs:
            cache_size = kwargs['cache_size']
        else:
            cache_size = self.cache_size
        if 'begin' in kwargs:
            sanity_kwargs['begin'] = kwargs['begin']
        if 'end' in kwargs:
            sanity_kwargs['end'] = kwargs['end']
        return c_generalProfiler.get_hit_count(self.reader.cReader, self.cache_name, cache_size,
                                               self.bin_size, cache_params=self.cache_params, **sanity_kwargs)

    def get_hit_rate(self, **kwargs):
        """

        :return: a numpy array, with hit rate corresponding to size [0, bin_size, bin_size*2 ...]
        """
        sanity_kwargs = {}
        if 'num_of_threads' not in kwargs:
            sanity_kwargs['num_of_threads'] = self.num_of_threads
        else:
            sanity_kwargs['num_of_threads'] = kwargs['num_of_threads']
        if 'cache_size' in kwargs:
            cache_size = kwargs['cache_size']
        else:
            cache_size = self.cache_size
        if 'begin' in kwargs:
            sanity_kwargs['begin'] = kwargs['begin']
        if 'end' in kwargs:
            sanity_kwargs['end'] = kwargs['end']
        if "prefetch" in kwargs and kwargs['prefetch']:
            return c_generalProfiler.get_hit_rate_with_prefetch(self.reader.cReader, self.cache_name, cache_size,
                                              self.bin_size, cache_params=self.cache_params, **sanity_kwargs)
        else:
            return c_generalProfiler.get_hit_rate(self.reader.cReader, self.cache_name, cache_size,
                                                            self.bin_size, cache_params=self.cache_params, **sanity_kwargs)

    def get_miss_rate(self, **kwargs):
        """

        :return: a numpy array, with miss rate corresponding to size [0, bin_size, bin_size*2 ...]
        """

        sanity_kwargs = {}
        if 'num_of_threads' not in kwargs:
            sanity_kwargs['num_of_threads'] = self.num_of_threads
        if 'cache_size' in kwargs:
            cache_size = kwargs['cache_size']
        else:
            cache_size = self.cache_size
        if 'begin' in kwargs:
            sanity_kwargs['begin'] = kwargs['begin']
        if 'end' in kwargs:
            sanity_kwargs['end'] = kwargs['end']
        return c_generalProfiler.get_miss_rate(self.reader.cReader, self.cache_name, cache_size,
                                               self.bin_size, cache_params=self.cache_params, **sanity_kwargs)

    def plotMRC(self, figname="MRC.png", **kwargs):
        MRC = self.get_miss_rate(**kwargs)
        try:
            # tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(x * self.bin_size))
            # plt.gca().xaxis.set_major_formatter(tick)
            plt.xlim(0, self.cache_size)
            plt.plot(range(0, self.cache_size + 1, self.bin_size), MRC)
            plt.xlabel("cache Size")
            plt.ylabel("Miss Rate")
            plt.title('Miss Rate Curve', fontsize=18, color='black')
            plt.savefig(figname, dpi=600)
            colorfulPrint("red", "plot is saved at the same directory")
            plt.show()
            plt.clf()
            del MRC
        except Exception as e:
            plt.savefig(figname)
            print("the plotting function is not wrong, is this a headless server?\n{}".format(e), file=sys.stderr)

    def plotHRC(self, figname="HRC.png", **kwargs):
        HRC = self.get_hit_rate(**kwargs)
        try:
            # tick = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(x * self.bin_size))
            # plt.gca().xaxis.set_major_formatter(tick)

            plt.xlim(0, self.cache_size)
            plt.plot(range(0, self.cache_size + 1, self.bin_size), HRC)
            plt.xlabel("cache Size")
            plt.ylabel("Hit Rate")
            plt.title('Hit Rate Curve', fontsize=18, color='black')
            plt.savefig(figname, dpi=600)
            colorfulPrint("red", "plot is saved at the same directory")
            plt.show()
            plt.clf()
            del HRC
        except Exception as e:
            plt.savefig(figname)
            print("the plotting function is not wrong, is this a headless server?")
            print(e)


    def __del__(self):
        if (os.path.exists('temp.dat')):
            os.remove('temp.dat')


def server_plot_all(path='/run/shm/traces/', threads=48):
    from mimircache.profiler.LRUProfiler import LRUProfiler
    folder = '0628_HRC'
    for filename in os.listdir(path):
        print(filename)
        if filename.endswith('.vscsitrace'):
            reader = vscsiReader(path + filename)
            p1 = LRUProfiler(reader)
            size = p1.plotHRC(figname=folder + "/" + filename + '_LRU_HRC.png')

            if os.path.exists(folder + "/" + filename + '_LRU4_HRC_' + str(size) + '_.png'):
                reader.close()
                continue

            p2 = cGeneralProfiler(reader, 'Optimal', cache_size=size, bin_size=int(size / 500), num_of_threads=threads)
            p2.plotHRC(figname=folder + "/" + filename + '_Optimal_HRC_' + str(size) + '_.png')
            p3 = cGeneralProfiler(reader, "LRU_K", cache_size=size, cache_params={"K": 2}, bin_size=int(size / 500))
            p3.plotHRC(figname=folder + "/" + filename + '_LRU2_HRC_' + str(size) + '_.png', num_of_threads=threads)
            # p4 = cGeneralProfiler(reader, "LRU_K", cache_size=size, cache_params={"K": 3}, bin_size=int(size / 500))
            # p4.plotHRC(figname=folder + "/" + filename + '_LRU3_HRC_' + str(size) + '_.png', num_of_threads=threads)
            # p5 = cGeneralProfiler(reader, "LRU_K", cache_size=size, cache_params={"K": 4}, bin_size=int(size / 500))
            # p5.plotHRC(figname=folder + "/" + filename + '_LRU4_HRC_' + str(size) + '_.png', num_of_threads=threads)
            reader.close()





if __name__ == "__main__":
    import time

    # server_plot_all('../data/', threads=8)

    # t1 = time.time()
    # r = plainCacheReader('../../data/test')
    # r = plainCacheReader('../data/parda.trace')
    # r = vscsiReader('../data/trace.vscsi')
    # r = vscsiReader("../data/traces/w38_vscsi1.vscsitrace")
    # print(r.get_num_of_total_requests())
    # r = vscsiReader("../1a1a11a/prefetch_input_data/w15/xab")
    # r = vscsiReader("/home/cloudphysics/traces/w38_vscsi1.vscsitrace")

    # cg = cGeneralProfiler(r, 'Optimal', 2000, 200)
    # cg = cGeneralProfiler(r, 'LRU_2', 38000, 200, num_of_threads=8)
    # cg = cGeneralProfiler(r, 'LRU_K', 2000, 200, cache_params={"K":2})
    # print(r.get_num_of_total_requests())
    # p = LRUProfiler(reader=r)
    # p.plotHRC(figname="HRC_LRU.png")

    # cg = cGeneralProfiler(r, 'YJC', 200000, 25000, num_of_threads=8,
    #                       cache_params={"LRU_percentage": 0.2, "LFU_percentage": 0.1})
    # cg = cGeneralProfiler(r, 'LRU', 200000, 1000, num_of_threads=8)
    # cg = cGeneralProfiler(r, 'LRU', 5000000, 100000, num_of_threads=8)


    # print(cg.get_hit_rate())
    # print(cg.get_hit_count())
    # print(cg.get_miss_rate())



    CACHE_SIZE = 20000
    BIN_SIZE = 200
    NUM_OF_THREADS = 8
    DAT = "w15"

    t1 = time.time()

    r = vscsiReader("../1a1a11a/prefetch_input_data/{}/xab".format(DAT))
    cg = cGeneralProfiler(r, 'LRU', CACHE_SIZE, BIN_SIZE, num_of_threads=NUM_OF_THREADS)

    prefetch = False
    figname = "{}_xab_non_prefetch.png".format(DAT)
    hr1 = cg.get_hit_rate(prefetch=prefetch)
    print("TIME: %f" % (time.time() - t1))
    t1 = time.time()


    prefetch = True
    figname = "{}_xab_prefetch.png".format(DAT)
    hr2 = cg.get_hit_rate(prefetch=prefetch)
    print("TIME: %f" % (time.time() - t1))


    plt.xlim(0, CACHE_SIZE)
    plt.plot(range(0, CACHE_SIZE + 1, BIN_SIZE), hr1, label="no_prefetch")
    plt.plot(range(0, CACHE_SIZE + 1, BIN_SIZE), hr2, label="prefetch")

    plt.legend()
    plt.xlabel("cache Size")
    plt.ylabel("Hit Rate")
    plt.title('Hit Rate Curve', fontsize=18, color='black')
    plt.savefig(figname, dpi=600)
    colorfulPrint("red", "plot is saved at the same directory")

