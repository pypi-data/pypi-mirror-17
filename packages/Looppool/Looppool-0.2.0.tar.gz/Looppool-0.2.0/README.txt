.. image:: https://drone.io/bitbucket.org/saaj/looppool/status.png
    :target: https://drone.io/bitbucket.org/saaj/looppool/latest
.. image:: https://codecov.io/bitbucket/saaj/looppool/branch/default/graph/badge.svg
    :target: https://codecov.io/bitbucket/saaj/looppool/branch/default 
.. image:: https://badge.fury.io/py/Looppool.png
    :target: https://pypi.python.org/pypi/Looppool

********
Looppool
********
Looppool is a Python 3 package for running worker process pool of Tornado IO loops. It's useful
for a heavy asynchronous application which doesn't fit into single process due to increasing
CPU usage and suffers from IO loop blocking (see ``set_blocking_log_threshold`` [1]_).

It was developed as a part of performance optimisation of a Tornado data extraction application.
The application mixed IO-bound and CPU-bound tasks. Moreover, the CPU-bound tasks were highly
coupled with IO loop. Because of such coupling much simpler approach of ``concurrent.futures`` 
[3]_ wouldn't have helped.

Design
======
A picture worth a thousand words.

.. image:: https://bytebucket.org/saaj/looppool/raw/default/manual/overview.png
    :target: https://bitbucket.org/saaj/looppool/src/default/manual/overview.png

A few observations and notes:

    1. Messages are off-loaded to IO loops immediately. Thus there's no much sense
       in setting ``max_size`` to the queues. And if your workers don't timely process
       them memory usage will quickly grow. 
    2. Without proper synchronisation, `Barrier` [4]_, task listener threads 
       would greedily take message from the queue which would make "winner" busy while
       others idle. 
    3. ``add_callback`` [2]_ is safe (and only safe) method to pass control from other
       thread to IO loop's thread.
    4. Because queue message handlers (``fn1`` and ``fn2``) are called from IO loop
       they can be coroutines.
    5. ``Pool`` stops its workers by sending ``PoisonPill`` task message per worker.

Worker
======
There are two workers in the package: ``Worker`` and ``SafeWorker``. Both require 
override of ``_process_message(self, message)`` in a subclass. The difference between
them is that on receipt of poison pill ``SafeWorker`` will wait until its task are
completed, while ``Worker`` won't. The latter is sufficient when tasks are not critical,
which is typically true in a data extraction application. Also it will make application
process supervision simpler, because ``Pool`` will quickly stop.

Subclassing
-----------
``WorkerSubclass._process_message`` may be plain function or coroutine. It processes
task messages and puts them in result queue, like ``self._result_queue.put_nowait('some result')``.
``SafeWorkerSubclass._process_message`` must also call ``self._task_queue.task_done()`` in 
``try-finally`` clause, like::

    def _process_message(self, url):
        try:
            result = 'some processing'
            self._result_queue.put_nowait(result)
        finally:
            self._task_queue.task_done()
            
Or use ``task_done`` decorator (see example below).

More details are available in the package's unit test module [6]_.

Stateful worker
---------------
If you want to run stateful workers, for instance, use some periodically calculated lookup table,
but don't want to calculate it in every workers (e.g. burden of maintaining database connection),
you can rely on ``Barrier`` synchronisation. Sending ``2n - 1`` messages guarantees receipt by 
every workers at least once, where ``n`` is number of workers. On start of pool, ``n`` messages
are sufficient because there's no overlap over the ``Barrier``.

.. note::
    If your process start method [5]_ is *fork* (default on \*nix platforms), you can share
    some static data from parent process.

Installation
============
.. sourcecode:: bash

    pip install Looppool
    
Usage
=====
.. sourcecode:: python

    #!/usr/bin/env python3
    
    
    import looppool
    from tornado import gen, ioloop, httpclient
    
    
    class FetchWorker(looppool.SafeWorker):
        
        _http_client = None
        '''Tornado asynchronous HTTP client'''
      
        
        def _initialise(self):
            self._http_client = httpclient.AsyncHTTPClient()
        
        @looppool.task_done
        @gen.coroutine
        def _process_message(self, url):
            response = yield self._http_client.fetch(url)
            self._result_queue.put_nowait((url, response.headers.get('server')))
    
    
    @gen.coroutine
    def main():
        loop = ioloop.IOLoop.instance()
        pool = looppool.Pool(loop, pool_size = 4, worker_class = FetchWorker)
        pool.process_message = print
        pool.start()
        
        urls = [
            'https://python.org/',
            'http://tornadoweb.org/',
            'https://google.com/',
            'https://stackoverflow.com/',
        ]
        list(map(pool.put_nowait, urls))
        
        pool.stop()
    
    
    if __name__ == '__main__':
        ioloop.IOLoop.instance().run_sync(main)

Maintenance
===========
Maintaining a process group instead of one process is more tricky thing to do. 
Initially, you may want to see if your pool instance has actually spawned any
processes. Here's what you can do visualise your process tree, which has main process,
one or two (depending on start method) ``multiprocessing`` helper processes, and processes
of your ``looppool`` pools (you can use different pools for different tasks):: 

    htop -p $(pgrep -d"," -g $(pgrep -f "main-process-name-or-its-start-args"))
    
``top`` will also work but is limited to 20 PIDs. Enforcing the process tree stop is also
different. If something goes wrong process tree should be killed like::

    kill -9 -- -$(pgrep -f "main-process-name-or-its-start-args")

Killing only may process will leave helper and worker processes running.

.. note::
    Pool workers intentionally ignore ``SIGINT`` and ``SIGTERM`` because these signals
    propagate to children from parent process and break normal, message-based shutdown.
    
You can improve the names of your worker processes by setting them in worker's 
initialiser with ``setproctitle`` [7]_ (see example below).

Monitoring
----------
Generally it's very important to know how well your application behaves. Even more 
important it is for single-threaded (asynchronous) and multi-process applications.
For the former is critical to know that the process doesn't use 100% CPU except for rare peaks,
which would otherwise impair IO loop's ability to schedule tasks. For the latter CPU usage 
shows how well current number of workers handle the load. This is being said about application
metrics.

``looppool`` comes with build-in ``loopppol.utility.ResourceReporter`` which periodically 
(10 seconds by default) sends metrics as CPU usage, memory usage (RSS) and length of IO 
loop backlogs (``ioloop._handlers``, ``ioloop._callbacks`` and ``ioloop._timeouts``) to 
statsd-compatible server [9]_.  


Logging
-------
Multi-process logging is complicated. Most important part of logging is error reporting.
Sentry [8]_ goes a great solution to error reporting problem. It seamlessly integrates
with ``logging`` and is suggested tool to know what errors occur in your workers.

Instrumentated worker
---------------------
For the following code you will need to run ``pip install raven statsd setproctitle``.

.. sourcecode:: python

    #!/usr/bin/env python3
    
    
    import logging
    
    import looppool
    from looppool.utility import ResourceReporter 
    from statsd import StatsClient
    from raven import Client
    from raven.exceptions import InvalidDsn
    from raven.handlers.logging import SentryHandler
    from setproctitle import setproctitle
    
    
    class InstrumentatedWorker(looppool.Worker):
    
        _resource_reporter = None
        '''CPU, RSS and IO loop stats reporter'''
        
        
        def _initialise(self):
            setproctitle('python APP_NAME POOL_NAME pool worker')
            
            statsd = StatsClient('localhost', 8125, 'APP_PREFIX')
            self._resource_reporter = ResourceReporter(self._ioloop, statsd,
                'worker.instrumentated.process.{}'.format(self._number))
            
            try:
                handler = SentryHandler(Client('SENTRY_DSN'))
                handler.setLevel(logging.WARNING)
            except InvalidDsn:
                logging.exception('Cannot configure Sentry handler')
            else:
                logging.basicConfig(handlers=[handler], level=logging.WARNING)
            
        def _process_message(self, message):
            self._result_queue.put_nowait((message, self._number))
            
        def start(self):
            super().start()
            
            self._resource_reporter.start()
            
        def join(self):
            self._resource_reporter.stop()
            
            super().join()


.. [1] http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop.set_blocking_log_threshold
.. [2] http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop.add_callback
.. [3] https://docs.python.org/3/library/concurrent.futures.html
.. [4] https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Barrier
.. [5] https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_start_method
.. [6] https://bitbucket.org/saaj/looppool/src/default/looppool/test.py
.. [7] https://pypi.python.org/pypi/setproctitle
.. [8] https://pypi.python.org/pypi/sentry
.. [9] https://github.com/etsy/statsd/wiki#server-implementations
