Copyright (c) 2016, Pedro Lopes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Description: Compressed Deque
        ================
        
        A deque which compresses its items for a decreased volatile and persistent memory footprint.
        
        Installation
        ------------
        
        .. code-block:: bash
        
            $ pip install compressed-deque
        
        
        How to Use it
        -------------
        
        .. code-block:: python
        
            from compdeque import CompressedDeque
        
            # Instantiate the Deque
            collection = CompressedDeque()
        
            # Use it as a normal deque
            collection.append(1)
        
            # Persist to a file
            CompressedDeque.save_to_file(collection, file_path="/path/to/collection.dat")
        
            # ...
        
            # and load it when you need it later
            loaded_collection = CompressedDeque.load_from_file("/path/to/collection.dat")
        
        Tests and documentation
        -----------------------
        
        On the project's root folder:
        
        .. code-block:: bash
        
            # Run all tests
            $ make test
        
            # Generate documentation
            $ make docs
        
        Structure
        ---------
        
        Compressed Deque inherits from `deque <https://docs.python.org/2/library/collections.html#collections.deque>`_ and stores its items as zlib compressed pickles. The middle pickle layer only serves as a generic serialization method which can provide a serialized object string for zlib to compress. Although pickle can compress objects, its compression rate does not match zlib's, even using `higher protocols <https://docs.python.org/2/library/pickle.html#data-stream-format>`_.
        
        .. image:: docs/images/value_layers.png
        
        ``save_to_file()`` and ``load_from_file()`` static methods are provided to persist the collection directly into disk in its compressed representation, without much overhead.
        
        The persisted file contains a sequence of header/compressed_value pairs: the header is a 4 byte integer description of the compressed value's length and the compressed value is similiar to its in-memory representation.
        
        .. image:: docs/images/persisted_values.png
Keywords: compressed deque zipped zlib
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: Topic :: Software Development :: Build Tools
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
