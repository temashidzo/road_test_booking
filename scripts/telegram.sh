#!/bin/bash
source /projects/mpi/.venv/bin/activate
nohup python3 -u /projects/mpi/src/telegram.py >> /projects/mpi/logs/telegram.log &