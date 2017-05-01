# Copy batchIngestImages.sh file from working directory into all subdirectories.
# Use for Clark mss.
# Usage: first customize path in batchIngestImages.sh with Nuxeo path, then run script to copy the file into all subdirectories.
# Subdirectories in this case = Clark mss volumes

for d in ./*/ ; do (cd "$d" && cp ../batchIngestImages.sh ./); done