# Run batchIngestImages.sh in all directories within the working directory.
# Usage: make sure path in batchIngestImages.sh is correct, and that there is a copy in each directory.

for d in ./*/ ; do (cd "$d" && bash batchIngestClark.sh); done
