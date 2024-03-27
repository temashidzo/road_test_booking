#!/bin/bash
source /projects/mpi/.venv/bin/activate
nohup python3 -u /projects/mpi/src/mpi.py >> /projects/mpi/logs/mpi.log &