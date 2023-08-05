

[MPNUM]


A matrix product representation library for Python

[Travis] [Documentation Status]

This code is work in progress.

mpnum is a Python library providing flexible tools to implement new
numerical schemes based on matrix product states (MPS). So far, we
provide:

-   basic tools for various matrix product based representations, such
    as:
-   matrix product states (MPS), also known as tensor trains (TT)
-   matrix product operators (MPO)
-   local purification matrix product states (PMPS)
-   arbitrary matrix product arrays (MPA)
-   basic MPA operations: add, multiply, etc; compression (SVD
    and variational)
-   computing ground states (the smallest eigenvalue and eigenvector) of
    MPOs
-   flexible tools to implement new schemes based on matrix product
    representations

For more information, see:

-   Introduction to mpnum
-   Notebook with code examples
-   Library reference

Required packages:

-   six, numpy, scipy, sphinx (to build the documentation)

Supported Python versions:

-   2.7, 3.3, 3.4, 3.5


Contributors

-   Daniel Suess, daniel@dsuess.me, University of Cologne
-   Milan Holzaepfel, mail@mjh.name, Ulm University


License

Distributed under the terms of the BSD 3-Clause License (see LICENSE).
