# --------------------------------------------------------
# Name: Jugal Sadhnani
# ccid: sadhnani
# id: 1631943
# Course: CMPUT 274
# Assignment: #02 Huffman Coding
# ---------------------------------------------------------

import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''

    # uses pickle model to load the tree stream
    uncompressed_stream=pickle.load(tree_stream) 
    return(uncompressed_stream)

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """

    # checks if tree leaf has reached or not
    # if reached, returns value
    if not hasattr(tree,"getRight") and not hasattr(tree,"getLeft"):
      if tree.getValue()!=None:
        return(tree.getValue())
      else:
        return(None)
    #tries to read bit, exits if reached EOF
    try:
      bit=bitreader.readbit()
    except EOFError:
      pass
      exit()

    # If bit==1, go to the right tree branch
    if bit:
      return decode_byte(tree.getRight(),bitreader)
    return decode_byte(tree.getLeft(),bitreader)



def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''

    # initializes streams to respective bit reader and writer
    uncompressed_stream=bitio.BitWriter(uncompressed)
    compressed_stream=bitio.BitReader(compressed)
    # reads the tree from the compressed file
    huffman_tree=read_tree(compressed)

    symbols=""
    # loops infinitly until EOF
    while True:
      symbols=decode_byte(huffman_tree,compressed_stream)
      if symbols!=None:
        uncompressed_stream.writebits(symbols,8)
      elif symbols==None:
        break

    return uncompressed


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    # uses pickle model to write the tree to the tree stream
    serialized_tree=pickle.dump(tree,tree_stream)
    return serialized_tree

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''

    # writes the tree to the compressed file
    serialized_tree_01=write_tree(tree,compressed)
    # initializes streams to respective bit reader and writer
    uncompressed_stream_01=bitio.BitReader(uncompressed)
    compressed_stream_01=bitio.BitWriter(compressed)
    table=huffman.make_encoding_table(tree) # is a dictionary with encoded values
    byte_02=""
    # loops infinitly until EOF 
    while True:
      try:
        byte_01=uncompressed_stream_01.readbits(8) #reads 8 bits at a time, (byte)
        # checks if the read byte is in the table
        # if it is, then writes the encoded values
        if byte_01 in table:
          for j in table[byte_01]:
            compressed_stream_01.writebit(j)
      except EOFError:
        # once eof is reached, writes the "none" value from the table
        for k in table[None]:
          compressed_stream_01.writebit(k)
        break
    # flush has been used to take care of any partial bits
    compressed_stream_01.flush()
    return compressed



