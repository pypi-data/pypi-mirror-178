<p align="center">
  <a href="https://github.com/murilo-cunha/stream-wars"><img width="50%" alt="logo" src="https://raw.githubusercontent.com/murilo-cunha/stream-wars/main/images/stream-wars-logo.png"></a>
</p>
<p align="center">
  <a href="https://pypi.org/project/stream-wars/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/stream-wars" /></a>
  <a href="https://pypi.org/project/stream-wars/"><img alt="PiPy" src="https://img.shields.io/pypi/v/stream-wars" /></a>
  <a href="https://pepy.tech/project/stream-wars"><img alt="Downloads" src="https://pepy.tech/badge/stream-wars" /></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>
</p>

> A Star Wars crawl component for Streamlit apps!

A wrapper around [`star-wars-crawl-greensock-with-hooks`](https://github.com/mandiwise/star-wars-crawl-greensock-with-hooks)
by [@mandiwise](https://github.com/mandiwise), using the
[`streamlit-component-template-react-hooks`](https://github.com/whitphx/streamlit-component-template-react-hooks)
by [@whitphx](https://github.com/whitphx) (credits to them! 👏👏).

## Details

This is a small project putting together a "Star Wars" crawl component written in React and a React hooks-based template for Streamlit apps.

Why? The official documentation lists the class based components for React. React has released the hook-based API, which is arguably simpler and generally preferred over the class based components. Personally, I also prefer hook-based components over class-based ones. The project also uses `poetry` over the official documentation's `setup.py` and `MANIFEST.in` files - another personal decision.

## Features

- [x] Custom button
- [x] Custom intro
- [x] Custom episode text
- [x] Custom episode title
- [x] Custom crawl content
- [ ] Available on `wide` layout
