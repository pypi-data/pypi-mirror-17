#
# This file is part of mpi_map.
#
# mpi_map is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpi_map is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with mpi_map.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

__all__ = ['logger', 'get_avail_procs', 'split_data', 'mpi_map_code',
           'eval_method', 'barrier', 'MPI_Pool',
           'ReduceObject']

import os
import sys
import time
import marshal, types
import dill
import logging
import inspect
import itertools
import distutils.spawn
from mpi4py import MPI
import mpi_map

logger = logging.getLogger('mpi_map')
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s",
                              "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_avail_procs():
    return MPI.COMM_WORLD.Get_size()

def split_data(x, procs):
    # Split the input data
    ns = [len(x) // procs]*procs
    for i in range(len(x) % procs): ns[i] += 1
    for i in range(1,procs): ns[i] += ns[i-1]
    ns.insert(0,0)
    split_x = [ x[ns[i]:ns[i+1]] for i in range(0, procs) ]
    return (split_x, ns)

def mpi_map_code(f, x, params, procs, obj_dill=None):
    """ This function applies the function in ``func_code`` to the ``x`` inputs on ``procs`` processors.

    Args:
      f (function): function
      x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
      params (tuple): parameters to be passed to the function (pickable)
      procs (int): number of processors to be used
      obj (object): object where ``f``

    Returns:
      (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
    """
    sys.setrecursionlimit(10000)
    func_code = marshal.dumps(f.__code__)
    if not obj is None:
        obj_dill = dill.dumps(obj)
    else: obj_dill = None
    
    try:
        path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_eval.py'
    except KeyError:
        path = distutils.spawn.find_executable('mpi_eval.py')

    if len(x) > 0:
        cwd = os.getcwd()
        procs = min(procs,len(x))

        comm = MPI.COMM_SELF.Spawn(sys.executable,
                                   args=[path],
                                   maxprocs=procs)

        # Broadcast function and parameters
        comm.bcast((cwd, obj_dill, func_code, params), root=MPI.ROOT)

        # Split the input data
        split_x, ns = split_data(x, procs)

        # Scatter the data
        comm.scatter(split_x, root=MPI.ROOT)

        # # Avoid busy waiting
        # mpi_map.barrier(MPI.COMM_WORLD)

        # Gather the results
        fval = comm.gather(None,root=MPI.ROOT)

        comm.Disconnect()

        # Check for exceptions
        for v in fval:
            fail = False
            if isinstance(v, tuple) and isinstance(v[0], Exception):
                print (v[1])
                fail = True
        if fail:
            raise RuntimeError("Some of the MPI processes failed")

        if isinstance(fval[0], list):
            fval = list(itertools.chain(*fval))

    else:
        fval = []
    
    return fval

def eval_method(fname, x, params, obj, nprocs=None,
                reduce_obj=None, reduce_args=None,
                import_set=set(), splitted=False):
    """ This function applies the method with name ``fname`` of object ``obj`` to the ``x`` inputs on ``nprocs`` processors.

    Args:
      fname (str): name of the function defined in ``obj``
      x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
      params (tuple): parameters to be passed to the function (pickable)
      obj (object): object where ``f`` is defined
      nprocs (int): number of processes. If ``None`` then ``MPI.COMM_WORLD.Get_size()``
        processes will be started
      reduce_obj (object): object :class:`ReduceObject` defining the reduce
        method to be applied (if any)
      reduce_args (object): arguments to be provided to ``reduce_object``
      import_set (set): list of couples ``(module_name,as_field)`` to be imported
        as ``import module_name as as_field``
      splitted (bool): whether the input is already splitted

    Returns:
      (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
    """
    
    sys.setrecursionlimit(10000)
    obj_dill = dill.dumps(obj)
    red_obj_dill = dill.dumps(reduce_obj)
    
    try:
        path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_eval_method.py'
    except KeyError:
        path = distutils.spawn.find_executable('mpi_eval_method.py')

    if len(x) > 0:
        cwd = os.getcwd()

        if nprocs == None:
            nprocs = get_avail_procs()
        nprocs = min(nprocs,len(x))
        comm = MPI.COMM_SELF.Spawn(sys.executable,
                                   args=[path],
                                   maxprocs=nprocs)

        # Broadcast function and parameters
        comm.Barrier()
        comm.bcast((cwd, obj_dill, fname, params, red_obj_dill, import_set), root=MPI.ROOT)
        logger.debug("eval_method: broadcast")
        
        # Split the input data
        if splitted:
            if len(x) != nprocs:
                raise ValueError("The splitted input is not consistent with " + \
                                 "the number of processes")
            split_x = x
        else:
            split_x, ns = split_data(x, nprocs)

        # Split the reduce_args data
        if reduce_args is not None:
            if splitted:
                if len(reduce_args) != nprocs:
                    raise ValueError("The splitted reduce_args is not consistent with " + \
                                     "the number of processes")
                split_red_args = reduce_args
            else:
                split_red_args = reduce_obj.split_args(reduce_args, nprocs)
        else:
            split_red_args = [None for i in range(nprocs)]

        # Scatter reduce arguments
        comm.Barrier()
        comm.scatter(split_red_args, root=MPI.ROOT)
        logger.debug("eval_method: scatter")    
        
        # Scatter the data
        comm.Barrier()
        comm.scatter(split_x, root=MPI.ROOT)
        logger.debug("eval_method: scatter")

        # # Avoid busy waiting
        # mpi_map.barrier(MPI.COMM_WORLD)

        # Gather the results
        comm.Barrier()
        fval = comm.gather(None,root=MPI.ROOT)
        logger.debug("eval_method: gather")

        # Check for exceptions
        for v in fval:
            fail = False
            if isinstance(v, tuple) and isinstance(v[0], Exception):
                print (v[1])
                fail = True
        if fail:
            raise RuntimeError("Some of the MPI processes failed")

        if reduce_obj is None and isinstance(fval[0], list):
            fval = list(itertools.chain(*fval))

    else:
        fval = []

    if reduce_obj is not None:
        fval = reduce_obj.outer_reduce(fval, reduce_args)

    comm.Barrier()
    comm.Disconnect()
        
    return fval
    
def barrier(comm, tag=0, sleep=0.01):
    """ Function used to avoid busy-waiting.

    As suggested by Lisandro Dalcin at:
    * http://code.google.com/p/mpi4py/issues/detail?id=4 and
    * https://groups.google.com/forum/?fromgroups=#!topic/mpi4py/nArVuMXyyZI
    """
    size = comm.Get_size()
    if size == 1:
        return
    rank = comm.Get_rank()
    mask = 1
    while mask < size:
        dst = (rank + mask) % size
        src = (rank - mask + size) % size
        req = comm.isend(None, dst, tag)
        while not comm.Iprobe(src, tag):
            time.sleep(sleep)
        comm.recv(None, src, tag)
        req.Wait()
        mask <<= 1
    logger.debug("Mask %d, Size %d" % (mask, size))

class MPI_Pool(object):
    r""" Returns (but not start) a pool of ``nprocs`` processes

    Usage example::
    
        import numpy as np
        import numpy.random as npr
        from TransportMaps import get_mpi_pool, mpi_eval

        class Operator(object):
            def __init__(self, a):
                self.a = a
            def sum(self, x, n=1):
                out = x
                for i in range(n):
                    out += self.a
                return out

        op = Operator(2.)
        x = npr.randn(100,5)
        n = 2

        pool = get_mpi_pool()
        pool.start(3)
        try:
            xsum = mpi_eval("sum", op, x, (n,), mpi_pool=pool)
        finally:
            pool.stop()
    """
    
    def __init__(self):
        self.mpirun = False
        self.nprocs = None
        self.comm = None
        
    def start(self, nprocs=None, import_set=set()):
        r""" Start the pool of processes

        Args:
          nprocs (int): number of processes. If ``None`` then ``MPI.COMM_WORLD.Get_size()``
            processes will be started
          import_set (set): list of couples ``(module_name,as_field)`` to be imported
            as ``import module_name as as_field``

        """
        if self.comm is None:
            sys.setrecursionlimit(10000)
            try:
                path = os.environ['VIRTUAL_ENV'] + '/bin/mpi_pool.py'
            except KeyError:
                path = distutils.spawn.find_executable('mpi_pool.py')
            cwd = os.getcwd()

            self.nprocs = nprocs
            if self.nprocs == None: # The command has been called through mpirun
                self.mpirun = True
                self.nprocs = get_avail_procs()
            logger.debug("MPI_Pool.start: spawn [before]")
            self.comm = MPI.COMM_SELF.Spawn(sys.executable,
                                            args=[path],
                                            maxprocs=self.nprocs)
            logger.debug("MPI_Pool.start: spawn [after]")
            
            # Broadcast cwd
            self.comm.Barrier()
            logger.debug("MPI_Pool.start: broadcast [before]")
            self.comm.bcast((cwd, import_set), root=MPI.ROOT)
            logger.debug("MPI_Pool.start: broadcast [after]")
            
    def stop(self):
        r""" Stop the pool of processes
        """
        if self.comm is not None:
            logger.debug("MPI_Pool.stop: broadcast [before]")
            # Stop children
            self.comm.Barrier()
            self.comm.bcast(("STOP", None, None, None, None), root=MPI.ROOT)
            logger.debug("MPI_Pool.stop: broadcast [after]")
            # Gather any error
            self.comm.Barrier()
            logger.debug("MPI_Pool.stop: gather [before]")
            fval = self.comm.gather(None, root=MPI.ROOT)
            logger.debug("MPI_Pool.stop: gather [after]")
            # Disconnect
            self.comm.Barrier()
            # Check whether somebody is still connected
            logger.debug("MPI_Pool.stop: disconnect [before]")
            self.comm.Disconnect()
            logger.debug("MPI_Pool.stop: disconnect [after]")
            self.comm = None
            
    def eval_method(self, fname, x, params, obj,
                    reduce_obj=None, reduce_args=None,
                    import_set=set(), splitted=False):
        r""" Submit a job to the pool.

        Execute function ``fname`` belonging to the object ``obj`` with scattered
        input ``x`` and additional parameters ``params``

        Args:
          fname (str): name of the function in ``obj`` to be executed
          x (:class:`list` or :class:`ndarray<numpy.ndarray>`): input
          params (tuple): additional parameters
          obj (object): object where to find function ``fname``
          reduce_obj (object): object :class:`ReduceObject` defining the reduce
            method to be applied (if any)   
          reduce_args (object): arguments to be provided to ``reduce_object``
          import_set (set): list of couples ``(module_name,as_field)`` to be imported
            as ``import module_name as as_field``
          splitted (bool): whether the input is already splitted

        Returns:
          (:class:`list` [``nprocs``]) -- (ordered) outputs from all the processes
        """
        if len(x) > 0:
            obj_dill = dill.dumps(obj)
            red_obj_dill = dill.dumps(reduce_obj)
            # Broadcast function and parameters
            self.comm.Barrier()
            self.comm.bcast((obj_dill, fname, params, red_obj_dill, import_set),
                            root=MPI.ROOT)
            logger.debug("MPI_Pool.eval_method: broadcast")
            
            # Split the input data
            if splitted:
                if len(x) != self.nprocs:
                    raise ValueError("The splitted input is not consistent with " + \
                                     "the number of processes")
                split_x = x
            else:
                split_x, ns = split_data(x, self.nprocs)

            # Split the reduce_args data
            if reduce_args is not None:
                if splitted:
                    if len(reduce_args) != self.nprocs:
                        raise ValueError("The splitted reduce_args is not consistent with "+\
                                         "the number of processes")
                    split_red_args = reduce_args
                else:
                    split_red_args = reduce_obj.split_args(reduce_args, self.nprocs)
            else:
                split_red_args = [None for i in range(self.nprocs)]

            # Scatter reduce arguments
            self.comm.Barrier()
            self.comm.scatter(split_red_args, root=MPI.ROOT)
            logger.debug("MPI_Pool.eval_method: scatter")
            
            # Scatter the data
            self.comm.Barrier()
            self.comm.scatter(split_x, root=MPI.ROOT)
            logger.debug("MPI_Pool.eval_method: scatter")
            
            # Gather the results
            self.comm.Barrier()
            fval = self.comm.gather(None,root=MPI.ROOT)
            logger.debug("MPI_Pool.eval_method: gather")
            # Check for exceptions
            for v in fval:
                fail = False
                if isinstance(v, tuple) and isinstance(v[0], Exception):
                    print (v[1])
                    fail = True
            if fail:
                self.stop()
                raise RuntimeError("Some of the MPI processes failed")
            if isinstance(fval[0], list):
                fval = list(itertools.chain(*fval))
        else:
            fval = []

        if reduce_obj is not None:
            fval = reduce_obj.outer_reduce(fval, reduce_args)
            
        return fval

class ReduceObject(object):
    r""" [Abstract] Generic object to be passed to MPI methods in order to define reduce operations.
    """
    def __init__(self):
        raise NotImplementedError("[Abstract]: needs to be extended")
    def split_args(self, red_args, nprocs):
        r""" [Abstract] Split the arguments into ``nprocs`` chunks

        Returns:
          (:class:`list<list>`) -- list of arguments chunks
        """
        raise NotImplementedError("[Abstract]: needs to be extended")
    def inner_reduce(self, x, red_args=None):
        r""" [Abstract] Reduce function called interally by every process
        """
        raise NotImplementedError("[Abstract]: needs to be extended")
    def outer_reduce(self, x, red_args=None):
        r""" [Abstract] Reduce function called by the root process
        """
        raise NotImplementedError("[Abstract]: needs to be extended")
