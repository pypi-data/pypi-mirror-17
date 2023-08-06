from __future__ import absolute_import, unicode_literals

import celery
import os

from functools import partial

from celery.five import items
from kombu import Queue
from kombu.utils import symbol_by_name

CYANIDE_TRANS = os.environ.get('CYANIDE_TRANS', False)
default_queue = 'c.stress.trans' if CYANIDE_TRANS else 'c.stress'
CYANIDE_QUEUE = os.environ.get('CYANIDE_QUEUE', default_queue)

templates = {}

IS_CELERY_4 = celery.VERSION[0] >= 4


def template(name=None):

    def _register(cls):
        templates[name or cls.__name__] = '.'.join([__name__, cls.__name__])
        return cls
    return _register


if IS_CELERY_4:

    def use_template(app, template='default'):
        if isinstance(template, list) and len(template) == 1:
            # weird argparse thing
            template = template[0]
        template = template.split(',')

        # mixin the rest of the templates when the config is needed
        @app.on_after_configure.connect(weak=False)
        def load_template(sender, source, **kwargs):
            mixin_templates(template[1:], source)

        app.config_from_object(templates[template[0]])
else:

    def use_template(app, template='default'):  # noqa
        template = template.split(',')
        app.after_configure = partial(mixin_templates, template[1:])
        app.config_from_object(templates[template[0]])


def mixin_templates(templates, conf):
    return [mixin_template(template, conf) for template in templates]


def mixin_template(template, conf):
    cls = symbol_by_name(templates[template])
    conf.update(dict(
        (k, v) for k, v in items(vars(cls))
        if not k.startswith('_')
    ))


def template_names():
    return ', '.join(templates)


@template()
class default(object):
    CELERY_ACCEPT_CONTENT = ['json']
    BROKER_URL = os.environ.get('CYANIDE_BROKER', 'pyamqp://')
    BROKER_HEARTBEAT = 30
    CELERY_RESULT_BACKEND = os.environ.get('CYANIDE_BACKEND', 'rpc://')
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_RESULT_PERSISTENT = True
    CELERY_RESULT_EXPIRES = 300
    CELERY_MAX_CACHED_RESULTS = 100
    CELERY_DEFAULT_QUEUE = CYANIDE_QUEUE
    CELERY_IMPORTS = ['cyanide.tasks']
    CELERY_TRACK_STARTED = True
    CELERY_QUEUES = [
        Queue(CYANIDE_QUEUE,
              durable=not CYANIDE_TRANS,
              no_ack=CYANIDE_TRANS),
    ]
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TASK_PUBLISH_RETRY_POLICY = {
        'max_retries': 100,
        'interval_max': 2,
        'interval_step': 0.1,
    }
    CELERY_TASK_PROTOCOL = 2
    if CYANIDE_TRANS:
        CELERY_DEFAULT_DELIVERY_MODE = 1
    CELERYD_PREFETCH_MULTIPLIER = int(os.environ.get('CYANIDE_PREFETCH', 10))


@template()
class redis(default):
    BROKER_URL = os.environ.get('CYANIDE_BROKER', 'redis://')
    BROKER_TRANSPORT_OPTIONS = {
        'fanout_prefix': True,
        'fanout_patterns': True,
    }
    CELERY_RESULT_BACKEND = os.environ.get('CYANIDE_BACKEND', 'redis://')


@template()
class redistore(default):
    CELERY_RESULT_BACKEND = 'redis://'


@template()
class acks_late(default):
    CELERY_ACKS_LATE = True


@template()
class pickle(default):
    CELERY_ACCEPT_CONTENT = ['pickle', 'json']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'


@template()
class confirms(default):
    BROKER_URL = 'pyamqp://'
    BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}


@template()
class events(default):
    CELERY_SEND_EVENTS = True
    CELERY_SEND_TASK_SENT_EVENT = True


@template()
class execv(default):
    CELERYD_FORCE_EXECV = True


@template()
class sqs(default):
    BROKER_URL = 'sqs://'
    BROKER_TRANSPORT_OPTIONS = {
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
    }


@template()
class proto1(default):
    CELERY_TASK_PROTOCOL = 1


@template()
class vagrant1(default):
    BROKER_URL = 'pyamqp://testing:t3s71ng@192.168.33.123//testing'


@template()
class vagrant1_redis(redis):
    BROKER_URL = 'redis://192.168.33.123'
    CELERY_RESULT_BACKEND = 'redis://192.168.33.123'
