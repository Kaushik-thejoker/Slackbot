import logging
from fastapi_utilities import repeat_at
@repeat_at(cron="* * * * 1-5")
async def slack_post_message():
    """
    This CRON IS TO TEST THE CRON JOB FUNCTIONING
    """
    logging.info("This is a TEST CRON PLS IGNOR")