from datetime import datetime
from typing import Optional

from coiote.utils import ApiEndpoint, api_call, ISO_INSTANT_FORMAT, sanitize_request_param
from coiote.v3.model.device_monitoring import MonitoringStatus, MonitoringDataResponse


class DeviceMonitoring(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="deviceMonitoring")

    @api_call(MonitoringStatus)
    def is_monitored(self, device_id: str) -> MonitoringStatus:
        return self.session.get(self.get_url(f"/configuration/device/{device_id}/enabled"))

    @api_call(MonitoringDataResponse)
    def get_data_batch(self, device_id: str, lwm2m_url: str, start_time: datetime, end_time: Optional[datetime],
                       limit=2048) -> MonitoringDataResponse:
        safe_lwm2m_url = sanitize_request_param(lwm2m_url)
        params = {"timeRangeStart": start_time.strftime(ISO_INSTANT_FORMAT), "limit": limit}
        if end_time:
            params["timeRangeEnd"] = end_time.strftime(ISO_INSTANT_FORMAT)
        return self.session.get(
            self.get_url(f"/data/{device_id}/resourceUrl/{safe_lwm2m_url}"),
            params=params
        )
