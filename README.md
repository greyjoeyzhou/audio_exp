# audio-exp

## Bootstrap

1. Install `rye`
    - following instructions in https://rye-up.com/guide/installation/#installing-rye to install `rye`
      - use `python` provisioned by the `rye`
2. Run `rye sync` to install all specified depedencies and create the virtualenv
    - this should install `maturin` as a development dep for this project and enable compilation of rust code as a python extension
    - inside venv (`. .venv/bin/activate`), install maturin by `pip install maturin` 
3. Develop in the Rust world
    - run `cargo add <dep>` to install cargo dependencies
    - inside venv (`. .venv/bin/activate`), run `maturin develop --skip-install` to compile rust code to a python extension and make it available in the virtualenv
    - run `rye build` to build wheel

## TODOs

- pyo3 to bridge rust enum or struct to a python class
- expriment more ndarray usage in rust side
- more usage of rust generics

- get simple usage sample for symphonia

- experiment and decide how to do logging
- more memory manamgent and lifetime management in rust side

- more usage samples for hound and symphonia
- more usage samples for making use of candle to provision some AI based audio processing tools
