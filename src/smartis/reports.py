from datetime import datetime

from aiohttp import ClientSession

from .base import SmartisBase


class SmartisReports(SmartisBase):
    """Reports methods API Smartis."""
    default_prefix_url = 'reports'

    async def get_report(self, session: ClientSession, project: str, metrics: str, 
                         date_from: datetime, date_to: datetime, group_by: str,
                         top_count: int, type: str | None = None,
                         filters: list[dict] | None = None, 
                         attribution: dict | None = None, 
                         fields: list | None = None) -> dict:
        """Read reports from Smartis."""
        payload = {
            'project': project,
            'metrics': metrics,
            'datetimeFrom': f'{date_from:%Y-%m-%d %H:%M:%S}',
            'datetimeTo': f'{date_to:%Y-%m-%d %H:%M:%S}',
            'groupBy': group_by,
            'type': type,
            'filters': filters,
            'attribution': attribution,
            'fields': fields,
            'topCount': top_count,
        }
        return await self._http_post(session, 'getReport', payload)
    
    async def get_filters(self, session: ClientSession) -> dict:
        """Read filters from Smartis."""
        return await self._http_post(session, 'getFilters') 

    async def _http_post(self, session: ClientSession, prefix_method: str,
                         payload: dict | None = None) -> dict:
        return await super()._http_post(session, prefix_method, payload)
