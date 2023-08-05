SCRIPT = """
#!/bin/bash
echo "K-ON $(k version)"

CURRENT_PROFILE = $(k profile current)

echo "** Initialize profile: $CURRENT_PROFILE **"

echo "$(k profile ls-env --raw)" > /tmp/k.env

while read -r line
do
  export $line
done < /tmp/k.env

export SPACESHIP_VENV_PREFIX=kuse
export VIRTUAL_ENV=$CURRENT_PROFILE

# export $(grep -v '^#' /tmp/k.env | xargs -0)
"""
