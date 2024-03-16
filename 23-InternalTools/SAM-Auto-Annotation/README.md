# Automatic Image Annotation with SAM - Quickstart
For an instant setup, download this entire directory to your machine, activate your Python/conda environment, and run `python autoannot.py test-images annotations true`. You can replace the images in test-images with your own and delete the Annotations folder.

You can also run `python ttsplit.py test-images train test 0.8` to create the directories `train/` and `test/` in the same location as `test-images/`, putting approx. 80% of your images into `train/`. You can replace the last argument (`0.8`) with any number between 0 and 1 for a different ratio.

Additionally, you can create a COCO annotation file (in the `.json` format) if you have already executed `autoannot.py` as described above. For example, to split test-images, annotate the training set, and create a COCO annotation file for it, you can run the following:
```
python ttsplit.py test-images train test 0.8
python autoannot.py train annotations true
python cocogen.py train/annotations
```

Alternatively, upload a .zip file of this entire directory to Sockeye with `scp <path-to-zip> <cwl>@sockeye.arc.ubc.ca:<path-to-working-directory>` and run `unzip` on it. Modify aademo.sh in vi as needed and submit your job with `sbatch aademo.sh`. To perform the three-script task described directly above, you can use `sbatch aademo-coco.sh` instead.

See the [Confluence Guide](https://ubcagrobotappliedai.atlassian.net/wiki/spaces/KB/pages/26214401/Automatic+Image+Annotation+with+Meta+AI+s+SAM+Segment-Anything+Model) for more details.
