"""
Defines json payloads to be delivered to the streaming endpoint
"""
import thoughtful
from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.step_report import StepReport
from thoughtful.supervisor.reporting.streaming_actions import Action


class StreamingPayload:
    """Defines core payload data required for all streaming requests"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.client = thoughtful.supervisor.__name__
        self.version = thoughtful.__version__

    def __json__(self):
        return {
            "job_id": self.job_id,
            "client": self.client,
            "version": self.version,
        }


class StepReportStreamingPayload(StreamingPayload):
    """
    Defines the payload for a step report action, this occurs when entering or
    exiting a step context
    """

    def __init__(self, step_report: StepReport, job_id: str):
        self.step_report = step_report
        super().__init__(job_id)

    def __json__(self):
        _json = super().__json__()
        _json.update(
            action=Action.STEP_REPORT,
            payload={"step_report": self.step_report.__json__()},
        )
        return _json


class BotManifestStreamingPayload(StreamingPayload):
    """
    Defines the payload for posting the manifest to the opus streaming endpoint
    occurring when entering supervisor's main context
    """

    def __init__(self, manifest: Manifest, job_id: str):
        self.manifest = manifest
        super().__init__(job_id)

    def __json__(self):
        _json = super().__json__()
        _json.update(
            action=Action.BOT_MANIFEST,
            payload={"bot_manifest": self.manifest.__json__()},
        )
        return _json
