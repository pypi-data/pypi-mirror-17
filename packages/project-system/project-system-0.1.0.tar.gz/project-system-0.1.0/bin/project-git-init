#!/bin/bash
# diamond-patterns 2016 Ian Dennis Miller
# http://github.com/iandennismiller/diamond-patterns

PROJECT_NAME="$1"

WORK_PATH=~/Work

if [ -f ~/.diamond-patterns.conf  ]; then
    source ~/.diamond-patterns.conf
fi

function project-git-init() {
    git init
    cat > Todo.md <<-EOF
# ${PROJECT_NAME}

## Milestone 1

- [ ] set up development environment

## Done
EOF
    echo "created Todo.md"
    echo "# ${PROJECT_NAME}" > Readme.md
    git add -A
    git commit -am "initial commit"
}

project-git-init