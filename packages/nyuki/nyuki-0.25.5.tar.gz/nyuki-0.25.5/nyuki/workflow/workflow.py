import asyncio
from datetime import datetime
import logging
from tukio import Engine, TaskRegistry, get_broker, EXEC_TOPIC
from tukio.workflow import (
    TemplateGraphError, Workflow, WorkflowTemplate, WorkflowExecState
)

from nyuki import Nyuki
from nyuki.bus import reporting
from nyuki.websocket import websocket_ready

from .api.factory import (
    ApiFactoryRegex, ApiFactoryRegexes, ApiFactoryLookup, ApiFactoryLookups,
    ApiFactoryLookupCSV
)
from .api.templates import (
    ApiTasks, ApiTemplates, ApiTemplate, ApiTemplateVersion, ApiTemplateDraft
)
from .api.workflows import ApiWorkflow, ApiWorkflows, ApiTest, ApiTestTopic
from .storage import MongoStorage
from .tasks import *
from .tasks.utils import runtime


log = logging.getLogger(__name__)


class BadRequestError(Exception):
    pass


def serialize_wflow_exec(obj):
    """
    JSON default serializer for workflows and datetime/isoformat.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Workflow):
        return obj.report()
    raise TypeError('obj not serializable: {}'.format(obj))


class WorkflowNyuki(Nyuki):

    """
    Generic workflow nyuki allowing data storage and manipulation
    of tukio's workflows.
    https://github.com/optiflows/tukio
    """

    CONF_SCHEMA = {
        'type': 'object',
        'required': ['mongo'],
        'properties': {
            'mongo': {
                'type': 'object',
                'required': ['host'],
                'properties': {
                    'host': {'type': 'string', 'minLength': 1},
                    'database': {'type': 'string', 'minLength': 1}
                }
            },
            'topics': {
                'type': 'array',
                'items': {'type': 'string', 'minLength': 1}
            }
        }
    }
    HTTP_RESOURCES = Nyuki.HTTP_RESOURCES + [
        ApiTasks,
        ApiTemplate,
        ApiTemplates,
        ApiTemplateDraft,
        ApiTemplateVersion,
        ApiWorkflow,
        ApiWorkflows,
        ApiFactoryRegex,
        ApiFactoryRegexes,
        ApiFactoryLookup,
        ApiFactoryLookupCSV,
        ApiFactoryLookups,
        ApiTest,
        ApiTestTopic,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_schema(self.CONF_SCHEMA)
        self.migrate_config()
        self.engine = None
        self.storage = None

        self.AVAILABLE_TASKS = {}
        for name, value in TaskRegistry.all().items():
            self.AVAILABLE_TASKS[name] = getattr(value[0], 'SCHEMA', {})

        runtime.bus = self.bus
        runtime.config = self.config

    @property
    def mongo_config(self):
        return self.config['mongo']

    @property
    def topics(self):
        return self.config.get('topics', [])

    async def setup(self):
        self.engine = Engine(loop=self.loop)
        await self.reload_from_storage()
        for topic in self.topics:
            asyncio.ensure_future(self.bus.subscribe(
                self.bus.publish_topic(topic), self.workflow_event
            ))
        # Enable workflow exec follow-up
        if 'websocket' in self._services.all:
            log.info('Setting up websocket updates of workflow instances')
            get_broker().register(self.report_workflow, topic=EXEC_TOPIC)
            # Set workflow serializer
            self.websocket.serializer = serialize_wflow_exec

    async def reload(self):
        await self.reload_from_storage()

    async def teardown(self):
        if self.engine:
            await self.engine.stop()

    @websocket_ready
    async def websocket_ready(self, token):
        """
        Immediately send all instances of workflows to the client.
        """
        return self.engine.instances

    async def report_workflow(self, event):
        """
        Send all worklfow updates to the clients.
        """
        await self.websocket.broadcast({
            'type': event.data['type'],
            'data': event.data.get('content', {}),
            'source': dict(event.source._asdict())
        })

    async def workflow_event(self, efrom, data):
        await self.engine.data_received(data, efrom)

    async def reload_from_storage(self):
        """
        Check mongo, retrieve and load all templates
        """
        self.storage = MongoStorage(**self.mongo_config)

        templates = await self.storage.templates.get_all(
            latest=True,
            with_metadata=False
        )

        for template in templates:
            try:
                await self.engine.load(WorkflowTemplate.from_dict(template))
            except Exception as exc:
                # Means a bad workflow is in database, report it
                reporting.exception(exc)
