"""Profile a Tornado application via REST."""
import logging
from operator import itemgetter

import tornado.web
import yappi

__author__ = "Megan Kearl Patten <megkearl@gmail.com>"


logger = logging.getLogger(__name__)


def start_profiling():
    """Start profiler."""
    # POST /profiler
    yappi.start(builtins=False, profile_threads=False)


def is_profiler_running():
    """Return True if the profiler is running."""
    # GET /profiler
    return yappi.is_running()


def stop_profiling():
    """Stop the profiler."""
    # DELETE /profiler
    yappi.stop()


def clear_stats():
    """Clear profiler statistics."""
    # DELETE /profiler/stats
    yappi.clear_stats()


def get_profiler_statistics(sort="cum_time", count=20):
    """Return profiler statistics.

    :param str sort: dictionary key to sort by
    :param int|None count: the number of results to return, None returns all results.
    """
    json_stats = []
    pstats = yappi.convert2pstats(yappi.get_func_stats())
    pstats.strip_dirs()

    for func, func_stat in pstats.stats.iteritems():
        path, line, func_name = func
        cc, num_calls, total_time, cum_time, callers = func_stat
        json_stats.append({
            "path": path,
            "line": line,
            "func_name": func_name,
            "num_calls": num_calls,
            "total_time": total_time,
            "total_time_per_call": total_time/num_calls if total_time else 0,
            "cum_time": cum_time,
            "cum_time_per_call": cum_time/num_calls if cum_time else 0
        })

    return sorted(json_stats, key=itemgetter(sort))[:count]


class ProfileStatsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get(self):
        """Return current profiler statistics."""
        try:
            statistics = get_profiler_statistics()
            self.write({'statistics': statistics})
            self.set_status(200)
        except TypeError:
            logger.exception('Error while retrieving profiler statistics')
            self.write({'error': 'No stats available. Start and stop the profiler before trying to retrieve stats.'})
            self.set_status(404)

        self.finish()

    def delete(self):
        """Clear profiler statistics."""
        clear_stats()
        self.set_status(204)
        self.finish()


class ProfilerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def post(self):
        """Start a new profiler."""
        if is_profiler_running():
            self.set_status(201)
            self.finish()
            return

        start_profiling()
        self.set_status(201)
        self.finish()

    def delete(self):
        """Stop the profiler."""
        stop_profiling()
        self.set_status(204)
        self.finish()

    def get(self):
        """Check if the profiler is running."""
        running = is_profiler_running()
        self.write({"running": running})
        self.set_status(200)
        self.finish()


class TornadoProfiler(object):

    def __init__(self, prefix="", handler_base_class=object):
        self.prefix = prefix
        self.handler_base_class = handler_base_class

    def get_routes(self):
        class UpdatedProfilerHandler(ProfilerHandler, self.handler_base_class):
            pass

        class UpdatedProfilerStatsHandler(ProfileStatsHandler, self.handler_base_class):
            pass

        return [
            (self.prefix + "/profiler", UpdatedProfilerHandler),
            (self.prefix + "/profiler/stats", UpdatedProfilerStatsHandler)
        ]


def main(port=8888):
    """Run as sample test server."""
    import tornado.ioloop

    routes = [] + TornadoProfiler().get_routes()
    app = tornado.web.Application(routes)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(port=8888)
