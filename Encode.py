import bitIO
import sys
import PQHeap
import Element
import tree_classes as tc

def Huffman(C):
    '''
    Genererer et Huffman-træ fra en liste af frekvenser.
    Tager en liste C som argument, hvor hver frekvens svarer til hyppigheden af et element.

    Funktionen opretter først et tomt prioritetskø (PQ) og indsætter alle bladnoder med deres respektive frekvenser.
    Derefter kombineres de to noder med mindst frekvens løbende, indtil der kun er én node tilbage, som bliver træets rod.

    Returnerer roden til trææt.
    '''
    n = len(C) #Antal af elementer i listen
    Q = PQHeap.createEmptyPQ() #Brug vores PQHeap for at oprette en tom prioritetskø

    for i in range(n):
        leaf = tc.leaf_node(i) #Opret en bladnode for hvert element i C
        z = Element.Element(C[i], leaf) #brug classen Element for at pakke hvert element i en instans med frekvensen
        PQHeap.insert(Q,z) #Indsæt elementet i prioritetskøen

    while len(Q) > 1:
        x = PQHeap.extractMin(Q) #extract elementet med mindst frekvens
        y = PQHeap.extractMin(Q) #extract elementet med næstmindst frekvens
        #Opret en ny internal node og sæt venstre barn til X og højre barn til y
        internal_node = tc.internal_node()  
        internal_node.left = x
        internal_node.right = y
        #Opret en ny element med summen af x's og y's nøgler
        z = Element.Element(x.key + y.key, internal_node)
        PQHeap.insert(Q,z) #indsæt det nye node i prioritetskøen
    return PQHeap.extractMin(Q) #returner det sidste element i køen, som er Huffman-træets rod

def generate_huffman_codes(root):
    """
    Genererer Huffman-koder for alle bladnoder i et givet Huffman-træ. 
    Udfører en dybdegående gennemgang af Huffman-træet fra roden for at generere de binære koder for hver bladnode.
    Tager Huffman-træets rod som argument
    Returnerer en dictionary der indeholder elemeterne med deres respektive Huffmann-koder
    """
    codes = {} 

    def traverse(node, prefix=""):
        """
        Hjælpefunktion til rekursiv gennemgang af Huffman-træet for at generere koder.
        Tager den nuværende node i træet som argument.
        """
        if isinstance(node.data, tc.leaf_node):
        # Hvis den nuværende node er en bladnode, tilføj dens kode til ordbogen    
            codes[node.data.data] = prefix
        else:
        # Hvis det er en indre node, fortsæt gennemgang til venstre og højre børn
            if node.data.left is not None:
                traverse(node.data.left, prefix + "0")
            if node.data.right is not None:
                traverse(node.data.right, prefix + "1")

    traverse(root) #start gennemgang fra roden
    return codes # returner det fulde sæt af Huffman-koder


with open(sys.argv[1], 'rb') as data_in:
    #Åben inputfilen til læsning i binært format
    frequency_table = [0] * 256 #Opret frekvenstabellen for hver byte
    byte = data_in.read(1) #Læs filen en byte ad gangen
    while byte:
        frequency_table[byte[0]] += 1
        # Inkrementer frekvensen for den læste byte i frekvenstabellen
        byte = data_in.read(1)

# Generer et Huffman-træ baseret på frekvenstabellen
huffman_tree = Huffman(frequency_table)
# Generer Huffman-koder for alle bladnoder i Huffman-træet
huffman_codes = generate_huffman_codes(huffman_tree)

#Åben inputfilen til læsning og outputfilen til skrivning (begge i binært format)
with open(sys.argv[1], 'rb') as data_in, open(sys.argv[2], 'wb') as data_out:
    #Brug BitWriter classen fra bitIO for at oprette en BitWriter
    #som håndterer bit-skrivning til outputfilen
    data_out_bits = bitIO.BitWriter(data_out)

    # Skriv frekvenstabellen til outputfilen som 32-bit integers
    for frequency in frequency_table:
        data_out_bits.writeint32bits(frequency)

    # Encode data ved at læse fra inputfilen byte for byte
    byte = data_in.read(1)
    while byte:
        bits = huffman_codes[byte[0]]
        for bit in bits:
            data_out_bits.writebit(int(bit))
        byte = data_in.read(1)
    #Luk BitWriter for at sikre, at alle bits bliver skrevet korrekt
    data_out_bits.close()
    