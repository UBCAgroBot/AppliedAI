# Automatic Image Annotation with SAM - Quickstart
For an instant setup, download this entire directory to your machine, activate your Python/conda environment, and run `python autoannot.py test-images annotations true`. You can replace the images in test-images with your own and delete the Annotations folder.

Alternatively, upload a .zip file of this entire directory to Sockeye with `scp <path-to-zip> <cwl>@sockeye.arc.ubc.ca:<path-to-working-directory>` and run `unzip` on it. Modify aademo.sh in vi as needed and submit your job with `sbatch aademo.sh`.

See the [Confluence Guide](https://ubcagrobotappliedai.atlassian.net/wiki/spaces/KB/pages/26214401/Automatic+Image+Annotation+with+Meta+AI+s+SAM+Segment-Anything+Model) for more details.
