#!/usr/bin/env bash

# The directory where you would like the 
# correction results to end up.
RESULTS_DIR=test_pipe2

# The ASV table you would like to run the analysis on.
ASV=../emp_data/VMP_16SmergedASVs_NOmito.txt

# The metadata table for each of the samples in the 
# asv table
META=../emp_data/metadata.txt

# config file should be in the same directory
# as where you run this script.
CONFIG=config.cfg
DOC=${RESULTS_DIR}/${CONFIG}

# create the directory to store the formattted input files and results
# from running habitat correction.
mkdir ${RESULTS_DIR}

# make a copy of the config file and this file 
# in the results directory
cat ${CONFIG} > ${DOC}
cat con_hab.sh > ${RESULTS_DIR}/con_hab.sh

# convert files
conda deactivate && conda activate habcor_py3
python convert_asv_meta_to_hc.py \
    --threshold 100  \
    --ASV ${ASV} \
    --meta ${META} \
    --out_a ${RESULTS_DIR}/asv_form.txt \
    --out_m ${RESULTS_DIR}/meta_form.txt

# run hab corr
conda deactivate && conda activate habcor_py2
python2 HabitatCorrectedNetwork.py \
    -A ${RESULTS_DIR}/asv_form.txt \
    -S ${RESULTS_DIR}/meta_form.txt \
    -out ${RESULTS_DIR}/pipe_test \
    -s config -sfn ${CONFIG}

# comment this out if you would 
# like to keep the formatted files
rm ${RESULTS_DIR}/*_form.txt
