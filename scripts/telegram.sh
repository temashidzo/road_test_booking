#!/bin/bash
source /root/Docs/MPI_Bot/.venv/bin/activate
nohup python3 -u /root/Docs/MPI_Bot/src/telegram.py >> /root/Docs/MPI_Bot/logs/telegram.log &