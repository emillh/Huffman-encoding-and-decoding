# Emil Ludvig Henriksen, emhen16@student.sdu.dk
# Áron Török-Czirmay, artor22@student.sdu.dk

import sys
import bitIO
import PQHeap
import Element
import tree_classes as tc

# Vi genbruger vores implementering af Huffman algoritmen fra Encode.py
def Huffman(C):
    n = len(C)
    Q = PQHeap.createEmptyPQ()

    for i in range(n):
        leaf = tc.leaf_node(i)
        z = Element.Element(C[i], leaf)
        PQHeap.insert(Q,z)

    while len(Q) > 1:
        x = PQHeap.extractMin(Q)
        y = PQHeap.extractMin(Q)
        internal_node = tc.internal_node()
        internal_node.left = x
        internal_node.right = y
        z = Element.Element(x.key + y.key, internal_node)
        PQHeap.insert(Q,z)
    return PQHeap.extractMin(Q)

# Vi aflæser huffmankoderne fra filen og dekoder dem
def decode_huffman(root, bit_reader):
    """
    For at dekode huffmankoderne, starter vi fra roden af træet og bevæger os nedad.
    Hvis vi rammer et blad, returnerer vi dataen i bladet.
    Ellers læser vi et bit fra bit_readeren og bevæger os enten til venstre eller højre i træet afhængigt af bitværdien.
    Hvis vi rammer enden af filen, stopper vi.
    """
    current_node = root
    while True:
        if isinstance(current_node.data, tc.leaf_node):
            yield current_node.data.data
            current_node = root
        else:
            bit = bit_reader.readbit()
            if bit == 0:
                current_node = current_node.data.left
            else:
                current_node = current_node.data.right
        if not bit_reader.readsucces():
            break

# Vi åbner inputfilen og outputfilen
with open(sys.argv[1], 'rb') as file_in, open(sys.argv[2], 'wb') as file_out:
    """
    Vi læser frekvenstabellen fra filen og rekonstruerer Huffman træet. Vi åbner også outputfilen.
    Derefter dekoder vi dataen og skriver den til outputfilen.
    Vi bruger frekvenstabellen til at tælle antallet af tegn, vi skal dekode.
    Når vi har dekodet det antal tegn, stopper vi, og filen er dekodet.
    """
    bit_reader = bitIO.BitReader(file_in)

    frequency_table = [bit_reader.readint32bits() for _ in range(256)]

    total_characters = sum(frequency_table)

    root = Huffman(frequency_table)

    decoder = decode_huffman(root, bit_reader)
    characters_decoded = 0
    for byte in decoder:
        if characters_decoded >= total_characters:
            break
        file_out.write(bytearray([byte]))
        characters_decoded += 1
