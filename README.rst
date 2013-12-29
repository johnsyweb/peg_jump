Peg Jump |Build Status| |Code Health|
=====================================

Something I found hanging around on a hard disk. I think I wrote it on a #1
tram when I was starting out in Python and automated unit testing. Five years
after It was written, I've cleaned-up the code a bit and published it for your
amusement.

It's the common triangular variant (with five pegs on a side) of
`Peg Solitaire <http://en.wikipedia.org/wiki/Peg_solitaire>`__

Usage
-----

Get started like so::

    % ./game.py

            Welcome to Peg Jump.
            ====================


          /\
         / x \
        / x  x \
       / x  x  x \
      / x  x  x  x \
     / x  x  x  x  x \
    +-----------------+

    Please select a peg to remove(row, column): 0, 0
          /\
         / . \
        / x  x \
       / x  x  x \
      / x  x  x  x \
     / x  x  x  x  x \
    +-----------------+

    Please select a peg to move (row, column): 2, 0
    Please select a hole to move to (row, column): 0, 0
          /\
         / x \
        / .  x \
       / .  x  x \
      / x  x  x  x \
     / x  x  x  x  x \
    +-----------------+


Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Ensure the tests pass for all Pythons in
   `.travis.yml <https://github.com/johnsyweb/peg_jump/blob/master/.travis.yml>`__
5. Push to the branch (``git push origin my-new-feature``)
6. Create new Pull Request

Thanks
------

If you find this stuff useful, please follow this repository on
`GitHub <https://github.com/johnsyweb/peg_jump>`__. If you
have something to say, you can contact
`johnsyweb <http://johnsy.com/about/>`__ on
`Twitter <http://twitter.com/johnsyweb/>`__ and
`GitHub <https://github.com/johnsyweb/>`__.

.. |Build Status| image:: https://travis-ci.org/johnsyweb/peg_jump.png
   :target: https://travis-ci.org/johnsyweb/peg_jump
.. |Code Health| image:: https://landscape.io/github/johnsyweb/peg_jump/master/landscape.png
   :target: https://landscape.io/github/johnsyweb/peg_jump/master
