# -*- coding: utf-8 -*-
from datetime import datetime


def filter_jobs(sacct_jobs, failed=True):
    """Filter jobs that have a FAILED etc. status."""
    if failed:
        categories = ('FAILED', 'CANCELLED')
    else:
        categories = ('COMPLETED', 'RUNNING', 'PENDING')
    filtered_jobs = [job for job in sacct_jobs if job['state'] in categories]
    return filtered_jobs


def time_to_sec(time_str):
    """Convert time in string format to seconds."""
    total_sec = 0
    if '-' in time_str:
        # parse out days
        days, time_str = time_str.split('-')
        total_sec += (int(days) * 60 * 60 * 24)

    time_parts = map(lambda val: int(round(float(val))), time_str.split(':'))
    total_sec += time_parts[-1]               # seconds
    total_sec += time_parts[-2] * 60          # minutes
    if len(time_parts) == 3:
        total_sec += time_parts[-3] * 60 * 60  # hours
    return total_sec


def convert_job(row):
    """Convert sacct row to dict."""
    state = row[9]
    if state not in ('PENDING', 'CANCELLED'):
        start_time = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')
        if state != 'RUNNING':
            end_time = datetime.strptime(row[8], '%Y-%m-%dT%H:%M:%S')
        else:
            end_time = None
    else:
        start_time = end_time = None

    return {
        'id': row[0],
        'name': row[1],
        'state': state,
        'start': start_time,
        'end': end_time,
        'elapsed': time_to_sec(row[6]),
        'cpu': time_to_sec(row[5]),
    }


def parse_sacct(sacct_stream):
    """Parse out information from sacct status output."""
    rows = (line.split() for line in sacct_stream)
    # filter rows that begin with a SLURM job id
    relevant_rows = (row for row in rows if row[0].isdigit())
    jobs = [convert_job(row) for row in relevant_rows]
    return jobs


def get_analysistime(sacct_jobs):
    """Calculate the total/overall time of the analysis."""
    completed_at = sacct_jobs[-1]['end']
    delta = completed_at - sacct_jobs[0]['start']
    total_cpu = sum(job['cpu'] for job in sacct_jobs)
    return int(delta.total_seconds()), total_cpu, completed_at
