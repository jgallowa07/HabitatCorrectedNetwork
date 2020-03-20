

TEMP_CONVERT_DATA_DICT=test_pipe2
ASV=../emp_data/VMP_16SmergedASVs_NOmito.txt
META=../emp_data/metadata.txt
CONFIG=config.cfg
DOC=${TEMP_CONVERT_DATA_DICT}/README.md

# create the directory to store the formattted input files and results
# from running habitat correction.
mkdir ${TEMP_CONVERT_DATA_DICT}

# echo into a readme where the data came from.
echo config: > ${DOC}
cat ${CONFIG} >> ${DOC}

# convert files
python3 convert_asv_meta_to_hc.py \
    --threshold 0 \
    --ASV ${ASV} \
    --meta ${META} \
    --out_a ${TEMP_CONVERT_DATA_DICT}/asv_form.txt \
    --out_m ${TEMP_CONVERT_DATA_DICT}/meta_form.txt

# run hab corr
python HabitatCorrectedNetwork.py \
    -A ${TEMP_CONVERT_DATA_DICT}/asv_form.txt \
    -S ${TEMP_CONVERT_DATA_DICT}/meta_form.txt \
    -out ${TEMP_CONVERT_DATA_DICT}/pipe_test \
    -s config -sfn ${CONFIG}

# comment this out if you would like to keep the formatted files
rm ${TEMP_CONVERT_DATA_DICT}/*_form.txt
