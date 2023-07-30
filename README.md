# How to use

There is a hosted version of the final report: https://cpsimpson.github.io/psych420-final-group1/

## To build our final report - with interactive simulations

1. Install required python packages
    `pip install -r references.txt`
1. Generate shinylive website output
    `shinylive export . docs`
1. Run local python static website
    `python3 -m http.server --directory docs --bind localhost 8008`
1. Open in browser
    `http://127.0.0.1:8008`


## To run the simulations

We have provided a main file which will run our simulations with default values.

1. Run `main.py`
