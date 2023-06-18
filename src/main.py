import asyncio
import aiohttp
import sys
import logging
from datetime import datetime, timedelta

import uvloop

import smartis
from core.config import settings


logger = logging.getLogger(__name__)


async def read_reports():
    logger.info('Start read reports')
    smartis_report = smartis.SmartisReports(settings.auth_token)
    async with aiohttp.ClientSession() as session:
        report = await smartis_report.get_report(
            session=session,
            project='object_282',
            metrics='vse-obrascheniya-novyy-_1508235518;comagic_calls;crm_contracts',
            date_from=(datetime.now() - timedelta(weeks=4)),
            date_to=datetime.now(),
            group_by='day',
            top_count=250,
        )
        logger.info(str(report))
        logger.info('Read filters')
        filters = await smartis_report.get_filters(session=session)
        logger.info(str(filters))
    logger.info('Finish read reports') 
        

async def main():
    task_read_reports = asyncio.create_task(read_reports())

    await task_read_reports

if __name__ == '__main__':
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
