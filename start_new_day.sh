#!/bin/bash

YEAR="2025"
DIR_ROOT="aoc${YEAR}"
DIR_PATTERN="day_"
SEARCH_PATH="./${DIR_ROOT}"

LAST_DAY=$(find "$SEARCH_PATH" -maxdepth 1 -type d -name "${DIR_PATTERN}*" 2>/dev/null |
           xargs -n 1 basename |
           sed "s/${DIR_PATTERN}//" |
           sort -n |
           tail -n 1)

if [ -z "$LAST_DAY" ]; then
    NEXT_DAY=1
else
    NEXT_DAY=$((LAST_DAY + 1))
fi

echo "Setting up AoC ${YEAR} - Day ${NEXT_DAY}"

FOLDER_NAME="${DIR_PATTERN}${NEXT_DAY}"
FILE_NAME="${FOLDER_NAME}.py"
FOLDER_PATH="${SEARCH_PATH}/${FOLDER_NAME}"
FILE_PATH="${FOLDER_PATH}/${FILE_NAME}"
INSTRUCTIONS_FILE="${FOLDER_PATH}/instructions.md"

echo "Creating directory: ${FOLDER_PATH}"
mkdir -p "$FOLDER_PATH"

echo "Creating file: ${FILE_PATH}"
cat << EOF > "$FILE_PATH"
"""
Advent of Code ${YEAR} - Day ${NEXT_DAY}

https://adventofcode.com/${YEAR}/day/${NEXT_DAY}

See instructions.md for problem description.
"""

import json

from requests_cache import CachedSession

# stole this from Kevin
INPUT = (
    CachedSession()
    .get(
        "https://adventofcode.com/${YEAR}/day/${NEXT_DAY}/input",
        cookies=json.load(open("cookie.json")),
    )
    .content.strip()
    .decode()
    .splitlines()
)

EXAMPLE_INPUT = """""".splitlines()  # noqa: W291


def solution(raw_input: list[str] = EXAMPLE_INPUT) -> int:
    # return the answer for part 1
    return -1


if __name__ == "__main__":
    print("----- Example Input -----")
    solution(EXAMPLE_INPUT)

    print("----- Solution -----")
    solution(INPUT)

EOF

# 4. Create an empty instructions file for problem description
echo "Creating instructions file: ${INSTRUCTIONS_FILE}"
touch "$INSTRUCTIONS_FILE"
cat << EOF > "$INSTRUCTIONS_FILE"
# Advent of Code 2025 - Day ${NEXT_DAY} Instructions

## Part 1

*Paste the problem description here.*
EOF

echo -e "\n✅ Setup for Day ${NEXT_DAY} complete!"
echo "Folder: ${FOLDER_NAME}"
echo "File: ${FILE_PATH}"