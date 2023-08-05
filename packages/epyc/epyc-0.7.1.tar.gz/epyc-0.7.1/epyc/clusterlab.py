# Simulation "lab" experiment management, parallel cluster version
#
# Copyright (C) 2016 Simon Dobson
# 
# Licensed under the GNU General Public Licence v.2.0
#

import epyc

import numpy
import pickle
import dill
import time

from ipyparallel import Client, RemoteError


class ClusterLab(epyc.Lab):
    '''A laboratory running over a cluster. Experiments are submitted to
    engines in the cluster for execution in parallel, with the experiments
    being performed asynchronously to allow for disconnection and subsequent
    retrieval of results. Combined with a persistent LabNotebook, this
    allows for fully decoupled access to an on-going computational
    experiment with piecewise retrieval.

    This class requires a cluster to already be set up and running, configured
    for persistent access, with access to the necessary code and libraries,
    and with appropriate security information available.'''

    # The "waiting time", the period between checks when waiting for the
    # completion of penbding results. Setting this too low increases network
    # traffic, probably unnecessarily. Default is 30s
    WaitingTime = 30

    
    def __init__( self, notebook = None, url_file = None, profile = None, profile_dir = None, ipython_dir = None, context = None, debug = False, sshserver = None, sshkey = None, password = None, paramiko = None, timeout = 10, cluster_id = None, **extra_args ):
        '''Create an empty lab attached to the given cluster. most of the arguments
        are as expected by the ipyparallel.Client class, and are used to create the
        underlying connection to the cluster.

        Lab arguments:
           notebook: the notebook used to results (defaults to an empty LabNotebook)

        Cluster client arguments:
           url_file: file containing connection information for accessing cluster
           profile: name of the IPython profile to use
           profile_dir: directory containing the profile's connection information
           ipython_dir: directory containing profile directories
           context: ZMQ context
           debug: whether to issue debugging information (defaults to False)
           sshserver: username and machine for ssh connections
           sshkey: file containing ssh key
           password: ssh password
           paramiko: True to use paramiko for ssh (defaults to False)
           timeout: timeout in seconds for ssh connection (defaults to 10s)
           cluster_id: string added to runtime files to prevent collisions'''
        super(epyc.ClusterLab, self).__init__(notebook)
        
        # record all the connection arguments for later
        self._arguments = dict(url_file = url_file,
                               profile = profile,
                               profile_dir = profile_dir,
                               ipython_dir = ipython_dir,
                               context = context,
                               debug = debug,
                               sshserver = sshserver,
                               sshkey = sshkey,
                               password = password,
                               paramiko = paramiko,
                               timeout = timeout,
                               cluster_id = cluster_id,
                               **extra_args)
        self._client = None

        # connect to the cluster
        self.open()
        
        # make us use Dill as pickler by default
        self.use_dill()

    def open( self ):
        '''Connect to the cluster.'''
        if self._client is None:
            self._client = Client(**self._arguments)
        
    def close( self ):
        '''Close down the connection to the cluster.'''
        if self._client is not None:
            self._client.close()
            self._client = None
        
    def numberOfEngines( self ):
        '''Return the number of engines available to this lab.

        returns: the number of engines'''
        self.open()
        return len(self._client[:])

    def engines( self ):
        '''Return a list of the available engines.

        returns: a list of engines'''
        self.open()
        return self._client[:]

    def use_dill( self ):
        '''Make the cluster use Dill as pickler for transferring results.'''
        self.open()
        with self.sync_imports(quiet = True):
            import dill
        self._client.direct_view().use_dill()

    def sync_imports( self, quiet = False ):
        '''Return a context manager to control imports onto all the engines
        in the underlying cluster. This method is used within a with statement.

        quiet: if True, suppresses messages (defaults to False)
        returns: a context manager'''
        self.open()
        return self._client[:].sync_imports(quiet = quiet)
    
    def _mixup( self, ps ):
        '''Private method to mix up a list of values in-place using a Fisher-Yates
        shuffle (see https://en.wikipedia.org/wiki/Fisher-Yates_shuffle).

        ps: the array
        returns: the array, shuffled in-place'''
        for i in xrange(len(ps) - 1, 0, -1):
            j = int(numpy.random.random() * i)
            temp = ps[i]
            ps[i] = ps[j]
            ps[j] = temp
        return ps
     
    def runExperiment( self, e ):
        '''Run the experiment across the parameter space in parallel using
        all the engines in the cluster. This method returns immediately.
        The experiments are run asynchronously, with the points in the parameter
        space being explored randomly so that intermediate retrievals of results
        are more representative of the overall result. Put another way, for a lot
        of experiments the results available will converge towards a final
        answer, so we can plot them and see the answer emerge.        

        e: the experiment'''

        # create the parameter space
        space = self.parameterSpace()

        # only proceed if there's work to do
        if len(space) > 0:
            nb = self.notebook()
            
            # randomise the order of the parameter space so that we evaluate across
            # the space as we go along to make intermediate (incomplete) result
            # sets more representative of the overall result set
            ps = self._mixup(space)

            try:
                # connect to the cluster
                self.open()
            
                # submit an experiment at each point in the parameter space to the cluster
                view = self._client.load_balanced_view()
                jobs = view.map_async((lambda p: e.set(p).run()), ps)
                
                # record the mesage ids of all the jobs as submitted but not yet completed
                psjs = zip(ps, jobs.msg_ids)
                for (p, j) in psjs:
                    nb.addPendingResult(p, j)
            finally:
                # commit our pending results in the notebook
                nb.commit()
                self.close()

    def updateResults( self ):
        '''Update the jobs record with any newly-completed jobs.

        returns: the number of jobs completed at this call'''
        nb = self.notebook()

        # look for pending results if we're waiting for any
        n = 0
        if nb.numberOfPendingResults() > 0:
            # we have results to get, so query the cluster for all the
            # pending results in a single transaction
            retrieved = []
            try:
                self.open()
                try:
                    status = self._client.result_status(nb.pendingResults(), status_only = False)
                    #print "{c} jobs completed, {p} pending".format(c = len(status['completed']),
                    #                                               p = len(status['pending']))
                except RemoteError as re:
                    print re.ename, re.evalue
                    # deep-inspect the exception to check if we're a key error to one
                    # of the job ids, using the unfortunately conviluted syntac ipyparallel
                    # forces upon us
                    if re.ename is 'KeyError':
                        # it's a key error, check for the job id
                        j = re.evalue.rsplit(' ', 1)
                        if j in nb.pendingResults():
                            # there seems to be a race condition when retrieving jobs,
                            # so mask these errors since they shouldn't occur (assuming
                            # we're managing the data structures properly)
                            print "Can't retrieve {id}, will try again".format(id = j)
                        else:
                            # not a job id we asked for propagate the error
                            raise re
                    else:
                        # not an error we should mask, propagate it
                        raise re
                if len(status['completed']) > 0:
                    # add all the completed results to the notebook
                    for j in status['completed']:
                        r = status[j]

                        # update the result in the notebook, cancelling
                        # the pending result as well
                        nb.addResult(r, j)

                        # record that we retrieved the results
                        #print "Job {j}, results {r}".format(j = j, r = r)
                        n = n + 1
                        retrieved.append(j)
            finally:
                if n > 0:
                    # commit changes to the notebook
                    nb.commit()

                    # purge the completed jobs from the cluster
                    self._client.purge_hub_results(retrieved)

                # whatever happens, close our connection 
                self.close()
        return n
                
    def _availableResults( self ):
        '''Private method to return the number of results available.
        This does not update the results fetched from the cluster.

        returns: the number of available results'''
        return self.notebook().numberOfResults()

    def _availableResultsFraction( self ):
        '''Private method to return the fraction of results available, as a real number
        between 0 and 1. This does not update the results fetched from the cluster.

        returns: the fraction of available results'''
        tr = self.notebook().numberOfResults() + self.notebook().numberOfPendingResults()
        if tr == 0:
            return 0
        else:
            return (self.notebook().numberOfResults() + 0.0) / tr
    
    def readyFraction( self ):
        '''Test what fraction of results are available. This will change over
        time as the results come in.

        returns: the fraction from 0 to 1'''
        self.updateResults()
        return self._availableResultsFraction()
    
    def ready( self ):
        '''Test whether all the results are available. This will change over
        time as the results come in.

        returns: True if all the results are available'''
        return (self.readyFraction() == 1)

    def wait( self, timeout = -1 ):
        '''Wait for all pending results to be finished. If timeout is set,
        return after this many seconds regardless.

        timeout: timeout period in seconds (defaults to forever)
        returns: True if all the results completed'''

        # sd: we can't use ipyparallel.Client.wait() for this, because that
        # method only works for cases where the Client object is the one that
        # submitted the jobs to the cluster hub -- and therefore has the
        # necessary data structures to perform synchronisation. This isn't the
        # case for us, as one of the main goals of eypc is to support disconnected
        # operation, which implies a different Client object retrieving results
        # than the one that submitted the jobs in the first place. This is
        # unfortunate, but understandable given the typical use cases for
        # Client objects.
        #
        # Instead. we have to code around a little busily. The ClusterLab.WaitingTime
        # global sets the latency for waiting, and we repeatedly wait for this amount
        # of time before updating the results. The latency value essentially controls
        # how busy this process is: given that most simulations are expected to
        # be long, a latency in the tens of seconds feels about right as a default
        nb = self.notebook()
        
        if nb.numberOfPendingResults() > 0:
            # we've got pending results, wait for them
            jobs = nb.pendingResults()
            timeWaited = 0
            while (timeout < 0) or (timeWaited < timeout):
                # get any jobs that have completed
                self.updateResults()
                
                if nb.numberOfPendingResults() == 0:
                    # no pending jobs left, we're complete
                    return True
                else:
                    # not done yet, calculate the waiting period
                    if timeout == -1:
                        # wait for the default waiting period
                        dt = self.WaitingTime
                    else:
                        # wait for the default waiting period or until the end of the timeout.
                        # whichever comes first
                        if (timeout - timeWaited) < self.WaitingTime:
                            dt = timeout - timeWaited
                        else:
                            dt = self.WaitingTime
                            
                    # sleep for a while
                    time.sleep(dt)
                    timeWaited = timeWaited + dt

            # if we get here, the timeout expired, so do a final check
            # and then exit
            self.updateResults()
            return (nb.numberOfPendingResults() == 0)

        else:
            # no results, so we got them all
            return True
        
        
