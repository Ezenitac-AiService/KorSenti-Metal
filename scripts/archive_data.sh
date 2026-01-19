#!/bin/bash

# Archive Artifacts Script
# Moves processed data, models, and logs to archive_artifacts directory

ARCHIVE_DIR="archive_artifacts"
mkdir -p "$ARCHIVE_DIR"

echo "[INFO] Archiving artifacts to $ARCHIVE_DIR..."

# Move data/processed if exists
if [ -d "data/processed" ]; then
    mv data/processed "$ARCHIVE_DIR/"
    echo "[INFO] Moved data/processed"
else
    echo "[WARN] data/processed not found"
fi

# Move data/model if exists
if [ -d "data/model" ]; then
    mv data/model "$ARCHIVE_DIR/"
    echo "[INFO] Moved data/model"
else
    echo "[WARN] data/model not found"
fi

# Move logs if exists
if [ -d "logs" ]; then
    mv logs "$ARCHIVE_DIR/"
    echo "[INFO] Moved logs"
else
    echo "[WARN] logs not found"
fi

# Re-create empty directories for structure (optional, but good for project structure)
mkdir -p data/processed
mkdir -p data/model
mkdir -p logs

# Add .gitkeep to keep them in git
touch data/processed/.gitkeep
touch data/model/.gitkeep
touch logs/.gitkeep

echo "[INFO] Archiving complete."
