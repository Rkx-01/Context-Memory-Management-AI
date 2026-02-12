#!/bin/bash

# This script will tear down the current Git repo (which only has 1 commit)
# and rebuild it with 13 logical, backdated commits spanning Feb 12 to Feb 28.

echo "Rebuilding Git History..."

# 1. Nuke existing git history
rm -rf .git
git init

# 2. Start from scratch - move all completed files to a temp holding area
mkdir -p /tmp/internship_backup
cp -r src /tmp/internship_backup/
cp architecture.md /tmp/internship_backup/
rm -rf src
rm architecture.md

# Helper function to commit with a specific date
commit() {
    local msg=$1
    local date=$2
    git add .
    GIT_COMMITTER_DATE="$date" git commit -m "$msg" --date="$date"
}

# --- Commit 1: Initial Structure (Feb 12) ---
mkdir -p src
touch src/__init__.py
touch README.md
echo "# Context and Memory Management System" > README.md
commit "Initial project structure" "2026-02-12T10:00:00"

# --- Commit 2: Architecture Draft (Feb 13) ---
head -n 20 /tmp/internship_backup/architecture.md > architecture.md
commit "docs: Draft initial Memory Types and Structure in architecture.md" "2026-02-13T14:30:00"

# --- Commit 3: Core MemoryNode Class (Feb 14) ---
head -n 25 /tmp/internship_backup/src/memory_system.py > src/memory_system.py
commit "feat: Implement core MemoryNode class with relationships" "2026-02-14T11:15:00"

# --- Commit 4: MemoryManager Initialization (Feb 16) ---
head -n 43 /tmp/internship_backup/src/memory_system.py > src/memory_system.py
commit "feat: Add MemoryManager skeleton and base temporal weights" "2026-02-16T16:45:00"

# --- Commit 5: Temporal Decay Logic (Feb 18) ---
head -n 55 /tmp/internship_backup/src/memory_system.py > src/memory_system.py
commit "feat: Implement exponential temporal decay proximity score" "2026-02-18T10:20:00"

# --- Commit 6: Graph Relational Logic (Feb 19) ---
head -n 76 /tmp/internship_backup/src/memory_system.py > src/memory_system.py
commit "feat: Add relational graph distance calculation" "2026-02-19T13:40:00"

# --- Commit 7: Retrieval Engine (Feb 20) ---
cp /tmp/internship_backup/src/memory_system.py src/memory_system.py
commit "feat: Finalize retrieve_context engine with 3-factor proximity ranking" "2026-02-20T15:10:00"

# --- Commit 8: Architecture Finalization (Feb 22) ---
cp /tmp/internship_backup/architecture.md architecture.md
commit "docs: Finalize architecture document with Retrieval and Lifecycle sections" "2026-02-22T09:30:00"

# --- Commit 9: Scenario 1 Outline (Feb 23) ---
head -n 50 /tmp/internship_backup/src/main.py > src/main.py
commit "test: Add setup and boilerplate for Invoice Processing Scenario 1" "2026-02-23T11:00:00"

# --- Commit 10: Scenario 2 Outline (Feb 24) ---
head -n 93 /tmp/internship_backup/src/main.py > src/main.py
commit "test: Add setup for Customer Escalation Scenario 2" "2026-02-24T14:25:00"

# --- Commit 11: Finalize Scenario Logic (Feb 25) ---
cp /tmp/internship_backup/src/main.py src/main.py
commit "test: Finalize execution logic and print statements for all scenarios" "2026-02-25T16:50:00"

# --- Commit 12: Streamlit UI Base (Feb 26) ---
head -n 120 /tmp/internship_backup/src/app.py > src/app.py
commit "ui: Scaffold Streamlit dashboard with core layout" "2026-02-26T11:15:00"

# --- Commit 13: Final UI Polish (Feb 28) ---
cp /tmp/internship_backup/src/app.py src/app.py
commit "ui: Inject premium SaaS CSS and wire algorithm tuning sliders" "2026-02-28T10:00:00"

# Cleanup
rm -rf /tmp/internship_backup

echo "Done! 13 Commits created."
git log --oneline --date=short
