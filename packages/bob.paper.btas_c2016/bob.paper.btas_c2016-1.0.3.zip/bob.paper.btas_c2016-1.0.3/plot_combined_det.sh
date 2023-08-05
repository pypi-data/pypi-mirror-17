#!/usr/bin/env bash

# plot DET curves from different participants in one joint graph

# path to folder where folders with submissions are
prefix=$1

# it is DEV (development scores) or TEST (test scores)
group=$2

# folder where to output results
outpath=$3

function plot {

  titles=""
  realfiles=""
  attackfiles=""
  thr=""
  names=$1
  if [ "${group}" == "test" ]; then
    thresholds=$2
  fi
  for i in "${!names[@]}"; do
    realfiles="$realfiles$prefix/${names[$i]}/${group}-scores-real.txt "
    attackfiles="$attackfiles$prefix/${names[$i]}/${group}-scores-attack.txt "
    titles="$titles${names[$i]} "
    if [ "${group}" == "test" ]; then
        thr="$thr${thresholds[$i]} "
    fi
  done
  realfiles="$realfiles"
  attackfiles="$attackfiles"
  titles="$titles"
  thr="$thr"


  if [ "${group}" == "test" ]; then
    echo "bin/plot_det_from_sets.py -r $realfiles -a $attackfiles -l $titles --thresholds $thr -o ${outpath}"
    ./bin/plot_det_from_sets.py -r $realfiles -a $attackfiles -l $titles --thresholds $thr -o ${outpath}
  else
    echo "bin/plot_det_from_sets.py -r $realfiles -a $attackfiles -l $titles -o ${outpath}"
    ./bin/plot_det_from_sets.py -r $realfiles -a $attackfiles -l $titles -o ${outpath}
  fi
}

# names of the participants
names=(Baseline CPqD SJTUSpeech Idiap IITKGP_ABSP)
# pre-computed thresholds on Development set (you can run evaluate_scores.sh script for that)
thresholds=(0.182592450800 0.014654500000 -191.993500000000 -0.012448608350 1.945350000000)

# call the plot function
plot $names $thresholds

