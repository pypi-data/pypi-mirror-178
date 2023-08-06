'''
This package contains classes for building Plotly Dash application.

- Bootstrapped - application with preloaded bootstrap theme

- CoLab - for running inside Google CoLab notebook

- PyScript - contains preloaded [PyScript](https://pyscript.net/) environment

- Servers - provides methods for running development server and/or production server with HTTP/2
    support and serving local static files
'''


from ._dash import Bootstrapped, CoLab, PyScript, Servers
