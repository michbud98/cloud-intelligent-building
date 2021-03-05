from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import dummy_machines.requester as requester

import logging
import argparse
import sys

# Set logging to DEBUG which prints additional information
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

def scheduled_job(args: dict = dict()):
    """
    Job that is run on schedule.

    Args:
        args (dict, optional): [description]. Defaults to dict().
    """
    logging.debug(f'Running scheduled job. Args: {args}')
    requester.make_request(**args)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("device_type", help="Type of device [Thermometer/Sunblind]")
    parser.add_argument("device_id", help="Number representing id of device", type=int)
    parser.add_argument('-url',action="store", dest="url",
    help="URL of Django control app [default localhost:8000]")
    parser.add_argument('-s', "--seconds",action="store", dest="seconds",
    help="Trigger interval in seconds", type=int)
    parser.add_argument('-m', "--minutes",action="store", dest="minutes",
    help="Trigger interval in minutes [on default 1 min]", type=int)
    
    
    return parser

def create_job(args, parser, sched):
    device_type = None
    if args.device_type == "Thermometer":
        device_type = requester.DeviceType.THERMOMETERS
    elif args.device_type == "Sunblind":
        device_type = requester.DeviceType.BLINDS
    else:
        parser.print_help(sys.stderr)
        logging.info(f"Device type argument [{args.device_type}] is not valid argument")
        exit(1)
    
    if args.url is None:
        url = "http://localhost:8000"
    else:
        url = args.url

    if args.seconds is not None:
        sched.add_job(scheduled_job, args=[{"django_url": url, "device_type": device_type, "id": args.device_id}],
        trigger='interval', seconds=args.seconds)
    elif args.minutes is not None:
        sched.add_job(scheduled_job, args=[{"django_url": url, "device_type": device_type, "id": args.device_id}],
        trigger='interval', minutes=args.minutes)
    else:
        sched.add_job(scheduled_job, args=[{"django_url": url, "device_type": device_type, "id": args.device_id}],
        trigger='interval', minutes=1)

def main():
    parser = init_argparse()
    args = parser.parse_args()
    sched = BlockingScheduler()
    create_job(args, parser, sched)

    logging.info("Jobs scheduled.")
    sched.start()
