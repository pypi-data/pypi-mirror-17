"""
Graphite backend for the metrics api.
"""

from datetime import datetime
from urllib import urlencode
from urlparse import urljoin

from twisted.internet.defer import (
    Deferred, inlineCallbacks, succeed, returnValue)

import treq

from confmodel.errors import ConfigError
from confmodel.fields import ConfigText, ConfigBool, ConfigInt
from confmodel.fallbacks import SingleFieldFallback

from vumi.blinkenlights.metrics import (
    Metric, MetricManager, SUM, AVG, MAX, MIN, LAST)
from vumi.service import Worker, WorkerCreator

from go_metrics.metrics.base import (
    Metrics, MetricsBackend, MetricsBackendError, BadMetricsQueryError)
from go_metrics.metrics.graphite_time_parser import (
    interval_to_seconds, parse_time)


def strip_aggregator(name, aggregator):
    name = name.split('.')
    if name[-1] == aggregator.name:
        return '.'.join(name[:-1])
    return '.'.join(name)


def is_error(resp):
    return 400 <= resp.code <= 599


def omit_nulls(datapoints):
    return [d for d in datapoints if d['y'] is not None]


def zeroize_nulls(datapoints):
    return [{
        'x': d['x'],
        'y': 0.0 if d['y'] is None else d['y']
    } for d in datapoints]


null_parsers = {
    'keep': lambda x: x,
    'omit': omit_nulls,
    'zeroize': zeroize_nulls,
}


class GraphiteMetrics(Metrics):
    aggregators = {
        'sum': SUM,
        'avg': AVG,
        'max': MAX,
        'min': MIN,
        'last': LAST,
    }

    def _agg_from_name(self, name):
        aggregator_name = name.split('.')[-1]
        aggregator = self.aggregators.get(aggregator_name)
        if aggregator is None:
            raise BadMetricsQueryError(
                "Aggregator '%s' is not a valid aggregator" % aggregator_name)
        return aggregator

    def _get_full_metric_name(self, name, disable_auto_prefix=False):
        if disable_auto_prefix:
            return '%s.%s' % (self.owner_id, name)
        return '%s.%s.%s' % (
            self.backend.config.prefix, self.owner_id, name)

    def _build_metric_name(self, name, interval, align_to_from):
        agg = self._agg_from_name(name).name
        full_name = self._get_full_metric_name(name)

        return (
            "alias(summarize(%s, '%s', '%s', %s), '%s')" %
            (full_name, interval, agg, align_to_from, name))

    def _build_render_url(self, params):
        metrics = params['m']

        targets = [
            self._build_metric_name(
                name, params['interval'], params['align_to_from'])
            for name in metrics]

        url = urljoin(self.backend.config.graphite_url, 'render/')
        return "%s?%s" % (url, urlencode({
            'format': 'json',
            'target': targets,
            'from': params['from'],
            'until': params['until'],
        }, True))

    def _parse_datapoints(self, datapoints):
        return [{
            'x': x * 1000,
            'y': y,
        } for (y, x) in datapoints]

    def _parse_response(self, data, null_parser):
        return dict(
            (d['target'], null_parser(self._parse_datapoints(d['datapoints'])))
            for d in data)

    def _get_auth(self):
        config = self.backend.config

        if config.username is not None and config.password is not None:
            return (config.username, config.password)
        else:
            return None

    def _predict_data_size(self, start, end, interval):
        """
        Use the start and end times and interval size to predict the number of
        data points being requested.
        """
        now = datetime.utcnow()
        # "end" can be earlier than "start".
        period = abs(parse_time(end, now) - parse_time(start, now))
        interval_secs = interval_to_seconds(interval)
        return (period.seconds + 86400 * period.days) / interval_secs

    @inlineCallbacks
    def get(self, **kw):
        params = {
            'm': [],
            'from': '-24h',
            'until': '-0s',
            'nulls': 'zeroize',
            'interval': '1hour',
            'align_to_from': 'false',
        }
        params.update(kw)

        if (isinstance(params['m'], basestring)):
            params['m'] = [params['m']]

        predicted_size = self._predict_data_size(
            params['from'], params['until'], params['interval'])
        predicted_size *= max(1, len(params['m']))
        max_response_size = self.backend.config.max_response_size
        if predicted_size > max_response_size:
            raise BadMetricsQueryError(
                "%s data points requested, maximum allowed is %s" % (
                    predicted_size, max_response_size))

        if params['nulls'] not in null_parsers:
            raise BadMetricsQueryError(
                "Unrecognised null parser '%s'" % (params['nulls'],))

        url = self._build_render_url(params)
        resp = yield treq.get(
            url,
            auth=self._get_auth(),
            persistent=self.backend.config.persistent)

        if is_error(resp):
            raise MetricsBackendError(
                "Got error response interacting with metrics backend")

        null_parser = null_parsers[params['nulls']]
        returnValue(self._parse_response((yield resp.json()), null_parser))

    @inlineCallbacks
    def fire(self, **kw):
        metrics = []
        metrics_values = []
        for mname, mvalue in kw.iteritems():
            aggregator = self._agg_from_name(mname)
            metric_name = strip_aggregator(
                self._get_full_metric_name(
                    mname,
                    self.backend.config.disable_auto_prefix),
                aggregator)

            try:
                mvalue = float(mvalue)
            except (ValueError, TypeError):
                raise BadMetricsQueryError(
                    '%r is not a valid metric value,'
                    'should be a floating point number' % mvalue)

            metrics.append((Metric(metric_name, [aggregator]), mvalue))
            metrics_values.append({
                'name': mname,
                'value': mvalue,
                'aggregator': aggregator.name,
            })

        mm = yield self.backend.worker.get_metric_manager()
        [mm.oneshot(metric, value) for metric, value in metrics]

        returnValue(metrics_values)


class MetricWorker(Worker):
    def __init__(self, *args, **kwargs):
        super(MetricWorker, self).__init__(*args, **kwargs)
        self._started_d = Deferred()

    @inlineCallbacks
    def startWorker(self):
        self._metric_manager = yield self.start_publisher(
            MetricManager, '%s.' % self.config.get('prefix'))
        self._started_d.callback(self._metric_manager)

    @inlineCallbacks
    def stopWorker(self):
        if not self._started_d.called:
            yield self._started_d
        self._metric_manager.stop()

    def get_metric_manager(self):
        if self._started_d.called:
            return succeed(self._metric_manager)
        return self._started_d


class GraphiteBackendConfig(MetricsBackend.config_class):
    graphite_url = ConfigText(
        "Url for the graphite web server to query",
        default='http://127.0.0.1:8080')

    prefix = ConfigText(
        "Prefix for all metric names. Defaults to 'go.campaigns'",
        default='go.campaigns')

    disable_auto_prefix = ConfigBool(
        "Disable prefixing, sometimes leads to double prefixing depending"
        "on the configuration.",
        default=False)

    persistent = ConfigBool(
        ("Flag given to treq telling it whether to maintain a single "
         "connection for the requests made to graphite's web app."),
        default=True)

    basicauth_username = ConfigText(
        'Username for Basic Authentication for the Metrics API.',
        required=False)

    basicauth_password = ConfigText(
        'Password for Basic Authentication for the Metrics API.',
        required=False)

    graphite_username = ConfigText(
        "Basic auth username for authenticating requests to graphite.",
        required=False, fallbacks=[SingleFieldFallback("username")])

    graphite_password = ConfigText(
        "Basic auth username for authenticating requests to graphite.",
        required=False, fallbacks=[SingleFieldFallback("password")])

    username = ConfigText(
        ("Basic auth username for authenticating requests to graphite. "
         "DEPRECATED, use graphite_username instead."),
        required=False)

    password = ConfigText(
        ("Basic auth password for authenticating requests to graphite. "
         "DEPRECATED, use graphite_password instead."),
        required=False)

    max_response_size = ConfigInt(
        ("Maximum number of data points to return. If a request specifies a "
         "time range and interval that contains more data than this, it is "
         "rejected."),
        default=10000)

    amqp_hostname = ConfigText(
        "Hostname for where AMQP broker is located",
        default='127.0.0.1')

    amqp_port = ConfigInt(
        "Port to connect to the AMQP broker",
        default=5672)

    amqp_username = ConfigText(
        "Username to connect to the AMQP broker",
        default="guest")

    amqp_password = ConfigText(
        "Password to connect to the AMQP broker",
        default="guest")

    amqp_vhost = ConfigText(
        "Virtualhost for AMQP broker",
        default="/")

    amqp_spec = ConfigText(
        "Spec file for AMQP",
        default="amqp-spec-0-8.xml")

    def post_validate(self):
        auth = (self.username, self.password)
        exists = [x is not None for x in auth]

        if any(exists) and not all(exists):
            raise ConfigError(
                "Either both a username and password need to be given or "
                "neither for graphite backend config")


class GraphiteBackend(MetricsBackend):
    model_class = GraphiteMetrics
    config_class = GraphiteBackendConfig

    def initialize(self):
        self.worker = self.create_worker()
        self.worker.startService()

    def create_worker(self):
        config = self.config
        worker_creator = WorkerCreator({
            'hostname': config.amqp_hostname,
            'port': config.amqp_port,
            'username': config.amqp_username,
            'password': config.amqp_password,
            'vhost': config.amqp_vhost,
            'specfile': config.amqp_spec,
        })
        return worker_creator.create_worker_by_class(
            MetricWorker, {'prefix': config.prefix})

    @inlineCallbacks
    def teardown(self):
        yield self.worker.stopService()
