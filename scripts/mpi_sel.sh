#!/bin/bash
source /root/Docs/MPI_Bot/.venv/bin/activate
nohup python3 -u /root/Docs/MPI_Bot/src/mpi_sel.py >> /root/Docs/MPI_Bot/logs/script.log &