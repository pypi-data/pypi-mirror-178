# _Probabilistic_ Principal Component Analysis model

This project implements a PPCA model implemented in Rust for Python using `pyO3` and `maturin`.

## Installing

PyPI package comming soon:
```bash
pip install ppca_rs # hopefully!
```


## Quick example

```python
import numpy as np
from ppca_rs import Dataset, PPCATrainer, PPCA

samples: np.ndarray

# Create your dataset from a rank 2 np.ndarray, where each line is a sample.
# Use non-finite values (`inf`s and `nan`) to signal masked values
dataset = Dataset(samples)

# Train the model:
model: PPCAModel = PPCATrainer(dataset).train(state_size=10, n_iters=10)


# And now, let's have fun!

# Extrapolates the missing values with the most probable values:
model.extrapolate(dataset)

# Smooths (removes noise from) samples and fills in missing values:
model.filter_extrapolate(dataset)
```

## Building from soure

### Prerequisites

You will need [Rust](https://rust-lang.org/), which can be installed locally (i.e., without `sudo`) and you will also need `maturin`, which can be installed by 
```bash
pip install maturin
```
`pipenv` is also a good idea if you are going to mess around with it locally. At least, you need a `venv` set, otherwise, `maturin` will complain with you.

### Installing it locally

Check the `Makefile` for the available commands (or just type `make`). To install it locally, do
```bash
make install    # optional: i=python.version (e.g, `i=3.9`)
```

### Messing around and testing

To mess around, _inside a virtual environment_ (a `Pipfile ` is provided for the `pipenv` lovers), do
```bash
maturin develop  # use the flag --release to unlock superspeed!
```
This will install the package locally _as is_ from source.

## How do I use this stuff?

See the examples in the `examples` folder. Also, all functions are type hinted and commented. If you are using `pylance` or `mypy`, it should be easy to navigate.

## Is it faster than the pure Python implemetation you made?

You bet!
