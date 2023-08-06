All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * Neither the name of the email-normalize library nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: email-normalize
        ===============
        Return a normalized email-address stripping ISP specific behaviors such as
        "Plus addressing" (``foo+bar@gmail.com``). It will also parse out addresses that
        are in the ``"Real Name" <address>`` format.
        
        |Version| |Downloads| |Status| |Coverage| |CodeClimate| |License| |PythonVersions|
        
        Example
        -------
        
        .. code:: python
        
            from email_normalize import normalize
        
            # Returns ``foo@gmail.com``
            normalized = normalize('f.o.o+bar@gmail.com')
        
        .. |Version| image:: https://img.shields.io/pypi/v/email-normalize.svg?
           :target: https://pypi.python.org/pypi/email-normalize
        
        .. |Status| image:: https://img.shields.io/travis/gmr/email-normalize.svg?
           :target: https://travis-ci.org/gmr/email-normalize
        
        .. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/email-normalize.svg?
           :target: https://codecov.io/github/gmr/email-normalize?branch=master
        
        .. |Downloads| image:: https://img.shields.io/pypi/dm/email-normalize.svg?
           :target: https://pypi.python.org/pypi/email-normalize
        
        .. |License| image:: https://img.shields.io/github/license/gmr/email-normalize.svg?
           :target: https://github.com/gmr/email-normalize
        
        .. |CodeClimate| image:: https://img.shields.io/codeclimate/github/gmr/email-normalize.svg?
           :target: https://codeclimate.com/github/gmr/email-normalize
        
        .. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/email-normalize.svg?
           :target: https://github.com/gmr/email-normalize
        
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Classifier: Topic :: Communications
Classifier: Topic :: Internet
Classifier: Topic :: Software Development :: Libraries
