import logging

# Create a root logger
logging.basicConfig(
    level=logging.DEBUG,
    filename='woc.log',
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
)

root_logger = logging.getLogger('WorldOfCitizens')
