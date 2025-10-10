#!/bin/bash

# Start nodemon and serve in the background
# nodemon rebuilds the presentation when files change
# serve serves the built presentation on http://localhost:3000

npx nodemon &
npx serve build -l 3000 &

# Wait for both background processes
wait
