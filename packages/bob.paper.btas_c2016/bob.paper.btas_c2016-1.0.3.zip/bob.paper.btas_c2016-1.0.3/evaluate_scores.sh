#!/usr/bin/env bash
# Process scores from each participants, compute error rates, and plot DET curves

# folder where folders with submissions are
prefix_folder=$1

# it is DEV (development scores) or TEST (test scores)
group=$2

submissions=(Baseline CPqD Idiap IITKGP_ABSP SJTUSpeech)

# loop through participants
for p in "${submissions[@]}"; do
    echo "$p"

    if [ "${group}" == "test" ]; then
        scorepath_dev="${prefix_folder}/${p}/dev-scores"
    else
        scorepath_dev="${prefix_folder}/${p}/${group}-scores"
    fi
    scorepath="${prefix_folder}/${p}/${group}-scores"

    command="-n 20 -m 40 -t ${scorepath_dev}-attack.txt -d ${scorepath_dev}-real.txt -f ${scorepath}-attack.txt -e ${scorepath}-real.txt -o plots_btas2016_${p}_${group}"

    # compute error rates and plot DET curves for each participant and for different attacks
    ./bin/plot_pad_results.py $command -s all -k all --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s replay -k laptop --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s replay -k laptop_HQ_speaker --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s replay -k phone1 --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s replay -k phone2 --pretty-title "${p}"
    if [ "${group}" == "test" ]; then
        ./bin/plot_pad_results.py $command -s replay -k phone2_phone3 --pretty-title "${p}"
        ./bin/plot_pad_results.py $command -s replay -k laptop_phone3 --pretty-title "${p}"
    fi
    ./bin/plot_pad_results.py $command -s voice_conversion -k physical_access --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s speech_synthesis -k physical_access --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s voice_conversion -k physical_access_HQ_speaker --pretty-title "${p}"
    ./bin/plot_pad_results.py $command -s speech_synthesis -k physical_access_HQ_speaker --pretty-title "${p}"

    # combine error rates in one LaTeX table for each participant
    echo bin/plot_far_frr_pad.py -t btas2016_${p} -p ${group} -d plots -o stats_${p}.txt
    ./bin/plot_far_frr_pad.py -t btas2016_${p} -p ${group} -d plots -o stats_${p}_${group}.txt
done