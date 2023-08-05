#!/usr/bin/env bash
# Process scores from each participants, compute error rates, and plot DET curves

# folder where folders with submissions are
prefix_folder=$1

# it is 'dev' (development scores) or 'test' (test scores)
group=$2

submissions=(Baseline CPqD Idiap IITKGP_ABSP SJTUSpeech)

# loop through participants
for p in "${submissions[@]}"; do
    echo "$p"

    if [ "${group}" == "test" ]; then
        # for Test set, we need to de-randomize the file names, using provided list with mataching names.
        # Then, split scores into Real and Attack file lists
        recovery_path="${prefix_folder}/to_recover_test_files"
        ./bin/derandomize-test-scores.py  -r ${recovery_path}/real-dev-anchors4test.txt -a ${recovery_path}/attack-dev-anchors4test.txt -m ${recovery_path}/btas2016-testset-match-names.txt -d ${prefix_folder}/${p}/dev-scores.txt -i ${prefix_folder}/${p}/test-scores_v2.txt avspoof_btas2016
    else
        # for Dev set, just split scores into Real and Attack file lists
        ./bin/split_dev_scores.py  -i ${prefix_folder}/${p}/dev-scores.txt avspoof --protocol physical_access
    fi
done