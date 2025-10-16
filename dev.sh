#!/bin/bash

# Start nodemon with inline configuration and serve in the background
# nodemon rebuilds the presentation when files change
# serve serves the built presentation on http://localhost:3000

npx nodemon \
  --watch . \
  --ext md,py \
  --ignore build/ \
  --ignore node_modules/ \
  --exec "python index.py" &

npx serve build -l 3000 &

# Wait for both background processes
wait
