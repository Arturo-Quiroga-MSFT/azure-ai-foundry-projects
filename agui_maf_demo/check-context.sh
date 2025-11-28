#!/bin/bash
# Test what's being included in the Docker build context

echo "Creating test tarball to see what would be sent..."
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo

# Create a tar using the same .dockerignore
tar --exclude-from=.dockerignore -czf /tmp/test-context.tar.gz .

echo ""
echo "Total size: $(du -h /tmp/test-context.tar.gz | cut -f1)"
echo ""
echo "Top 20 largest items:"
tar -tzf /tmp/test-context.tar.gz | while read file; do
    if [ -f "$file" ]; then
        du -h "$file" 2>/dev/null
    fi
done | sort -hr | head -20

echo ""
echo "Directory summary:"
tar -tzf /tmp/test-context.tar.gz | sed 's|/.*||' | sort | uniq -c | sort -nr | head -20

rm /tmp/test-context.tar.gz
