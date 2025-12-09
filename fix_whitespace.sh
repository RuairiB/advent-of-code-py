#!/bin/bash

# my mac keyboard keeps adding non-breaking spaces (0xC2 0xA0) instead of regular spaces, and it's "definitely" not my fault...
BAD_CHAR=$(printf '\xc2\xa0')

TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

# happening in markdown files mostly, when hitting space too soon after a "#"
find "$TARGET_DIR" -type f \( -name "*.md" -o -name "*.py" \) -print0 | while IFS= read -r -d '' file; do
    if grep -q "$BAD_CHAR" "$file"; then
        # I'd love for macs to have gnu sed by default...
        sed -i.bak "s/$BAD_CHAR/ /g" "$file"
        if diff "$file" <(sed "s/$BAD_CHAR/ /g" "$file.bak") > /dev/null; then
            rm "$file.bak"
            echo "Fixed: $file"
        else
            echo "⚠️  Verification Failed: $file (backup preserved)"
        fi
    fi
done