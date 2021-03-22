import time  # library used to measure time spent on each section
import json  # library used to convert dictionary into string, then convert dictionary string into dict
from bitstring import BitArray  # library used to write binary file


def compression(target_file):
    """This is the compression section"""

    start_dict = float(time.process_time())  # measure time from here
    # frequency dictionary
    letter_freq = {}  # collect all characters in a text file

    opened_file = target_file
    filename = opened_file
    with open(opened_file, encoding="utf_8_sig") as f:
        for line in f:
            for letter in line:
                # print("'" + letter + "' found!") # test code
                try:
                    letter_freq[letter] += 1  # dict take every characters

                except:
                    KeyError  # ignore other characters not in the dictionary
                    letter_freq.update({letter: 1})  # add new character to dict

    # print("letter_freq", letter_freq)
    # Class for creating node objects in a tree
    class Node(object):
        """This is the class that creates an object that holds 2 daughter objects"""

        # constructor
        def __init__(self, left_node=None, right_node=None):
            """
            In a binary tree, each node can only have up to 2 daughters.
            The variable 'left' and 'right' stores the daughter nodes when initialised.
            The node stored in the daughters can either be a character (leaf) or another node object.
            """
            self.left_node = left_node  # left-hand nodes
            self.right_node = right_node  # right-hand node

        # getter method for left and right item
        def daughters(self):
            """This is a method that returns the contents of both nodes stored from their parent node"""
            return self.left_node, self.right_node

    # a ascending sorted array list of nodes (can be either a node object or a character node) in tuple
    # sort all tuple item by their second element (at position 1) in the array
    # convert evey item in the letter frequency dictionary 'letter_freq' into a tuple consist of a character and number
    list_nodes_objects = sorted(letter_freq.items(), key=lambda x: x[1], reverse=False)
    # print(list_nodes_objects)  # test code

    # this while loop iterates
    while len(list_nodes_objects) > 1:
        """
        This while loop iterates the list of node tuple until one item is left.
        The goal of this loop is to generate 1 node, which contains all the combined nodes
        """
        # take the 2 least weight nodes
        (character_1, freq_1) = list_nodes_objects[0]  # tuple (character, freq)
        (character_2, freq_2) = list_nodes_objects[1]
        list_nodes_objects = list_nodes_objects[2:]  # list of nodes updated after 2 nodes are taken out

        # print("list_nodes_objects ", list_nodes_objects)  # test code

        new_node = Node(character_1, character_2)  # new node, contains the 2 combined smallest node in an object
        list_nodes_objects.append(
            (new_node, freq_1 + freq_2))  # put the combined node back to the array of node with new weight
        # (combined node, sum of weight)

        # sort the array in order after a new node is append
        list_nodes_objects = sorted(list_nodes_objects, key=lambda x: x[1], reverse=False)

    # print("sorted list_nodes_objects ", list_nodes_objects)  # test code

    # Huffman dictionary generator
    def huffman_dictionary(node_object, binary=''):
        """
        This recursive function returns the huffman code mapping (hash table) for each characters in dictionary.
        The parameter 'node' can either be a node object or a character. e.g. (node, weight)
        The parameter 'bitString' stores the binary information of a character in every recursion.
        """
        # if a leaf (a string, not an object) is reached:
        if type(node_object) is str:
            return {node_object: binary}  # insert a new mapping to the dictionary

        # create a tuple, extract items (left_item, right_item) from a nodes' daughter
        (left_item, right_item) = node_object.daughters()

        encoding_dict = {}  # dictionary contains all the encoding
        # print("1 ", encoding_dict)  # test code

        # call itself recursively until all dictionary is added, depth first search algorithm
        encoding_dict.update(huffman_dictionary(left_item, binary + '0'))
        encoding_dict.update(huffman_dictionary(right_item, binary + '1'))
        # print("2 ", encoding_dict)  # test code
        return encoding_dict  # output the dictionary

    # trigger the function 'huffman_dictionary' to generate the huffman dictionary
    # by passing the [first object] in the [first tuple]
    # in the [list of tuple node object] created in the loop.
    huffman_encoding = huffman_dictionary(list_nodes_objects[0][0])
    # print(huffman_encoding)  # test code

    end_dict = float(time.process_time())  # end measure time in this line to check processing time for this section
    print(str(end_dict - start_dict) + " second taken to create a unique huffman hash table!")

    # add letter frequency to the compressed file

    # convert a dictionary object into string
    string_dict = json.dumps(letter_freq)
    # print("string dict: ", string_dict)  # test code

    # convert dictionary to ascii binary
    byte_array = string_dict.encode()

    binary_int = int.from_bytes(byte_array, "big")
    binary_string = bin(binary_int)

    dict_binary = binary_string[2:]
    # print("dict bin: ", dict_binary)  # test code

    # add binary identifier (a catchphrase) for the dictionary section
    # this separate the hash table with the huffman code
    byte_array1 = "catchphrase".encode()

    binary_int1 = int.from_bytes(byte_array1, "big")
    binary_catchphrase = bin(binary_int1)[2:]
    # print("catch bin: ", binary_catchphrase)  # test code
    # print("catch bin len: ",len(binary_catchphrase))  # test code: 87
    # ------

    huffman_binary = ''
    # insert binary encoding to a new compression file
    opened_file = open(opened_file, encoding="utf_8_sig")
    with opened_file as f:
        for line in f:
            for letter in line:
                # print(huffman_encoding[letter])  # test code
                huffman_binary += huffman_encoding[letter]
                # print(letter, huffman_encoding[letter])  # test code

    # print("huff: ",huffman_binary) # test code

    # compress file with hash table into binary
    encodingString = ""  # the encoded content
    # insert decoding hash table and the catchphrase

    encodingString += dict_binary + binary_catchphrase + huffman_binary
    # encodingString += dict_binary + binary_catchphrase + huffman_binary  # test code
    # print("binary: ", encodingString)  # test code

    # extract original file name
    file_name = filename[:-4]  # assuming the file to be compressed is .txt
    # print(file_name)  # test code

    # write 'encodingString' into a binary file
    compressed_file = BitArray(bin=encodingString)
    open_file = file_name + '.bin'
    with open(open_file, 'wb') as f:
        compressed_file.tofile(f)

    print("Compression completed!")
    end_compress = float(time.process_time())  # end measure time in this line to check processing time for this section
    print(str(end_compress - end_dict) + " second taken to compress file!")
    main()


def decompress(target_file):
    """This is the decompression section"""

    # extract binary string from a file
    start_decompress = float(time.process_time())  # start measure time in this line to check processing time

    binary_file_name = target_file
    filename = target_file
    with open(binary_file_name, 'rb') as f:
        binary_content = BitArray(f.read())

    binary_string = binary_content.bin

    # print("content: ",binary_string)  # test code
    # print(type(binary_string))  # test code

    # identify dictionary string section
    def Invalid():
        """This function display a warning if not catchphrase is found
        which indicate the compressed .bin file could be random"""
        print("Decompression Error! Invalid compressed file!")
        exit()

    pos = 0  # position counter
    catch_found = False

    while catch_found is False:

        if binary_string[len(binary_string) - 87 - pos:len(
                binary_string) - pos] == "110001101100001011101000110001101101000011100000110100001110010011000010111001101100101":
            # print("found!")  # test code
            catch_found = True
        else:
            pos += 1

        if pos > len(binary_string):
            Invalid()  # wrong file

    # print(pos)  # test code
    # dict_binary = binary_string[(pos + 87):] # the binary string of the dictionary ####
    dict_binary = binary_string[0:len(binary_string) - pos - 87]  ####
    # dict_binary = binary_string[pos:]
    # print("dict: ", dict_binary)  # test code
    # print("dict")
    # print("catch: ",binary_string[pos:(pos+87)])  # test code

    # convert to dictionary text
    # convert dict binary back to dict text
    binary_int3 = int(dict_binary, 2)
    byte_number3 = binary_int3.bit_length() + 7 // 8
    binary_array3 = binary_int3.to_bytes(byte_number3, "big")
    dict_ascii_text = str(binary_array3.decode())
    # print(type(dict_ascii_text))  # test code
    # print(dict_ascii_text)  # test code
    # print("len: ",len(str(dict_ascii_text)))  # test code

    # the binary conversion to string creates a ton of spaces before the actual dictionary string
    cpos = 0
    cfound = False
    # remove space before dictionary string
    while cfound is False:
        if dict_ascii_text[cpos] == "{":
            cfound = True
        cpos += 1
    # print(cpos)  # test code
    dict_text = dict_ascii_text[cpos - 1:]
    # print(len(dict_text))  # test code

    # convert dictionary string into a dictionary
    huffman_feq = json.loads(dict_text)
    # print("freq dictionary: ", huffman_feq)  # test code
    # print(type(huffman_hash))  # test code

    # identify binary content
    binary_content = binary_string[len(binary_string) - pos:]

    # print("bin: ", binary_content)  # test code
    # print("bin")

    # decompress to a new file: reconstruct the huffman tree and traverse

    # Class for creating node objects in a tree
    class Node(object):
        """This is the class that creates an object that holds 2 daughter objects"""

        # constructor
        def __init__(self, left_node=None, right_node=None):
            """
            In a binary tree, each node can only have up to 2 daughters.
            The variable 'left' and 'right' stores the daughter nodes when initialised.
            The node stored in the daughters can either be a character (leaf) or another node object.
            """
            self.left_node = left_node  # left-hand nodes
            self.right_node = right_node  # right-hand node

        # getter method for left and right item
        def daughters(self):
            """This is a method that returns the contents of both nodes stored from their parent node"""
            return self.left_node, self.right_node

    # a ascending sorted array list of nodes (can be either a node object or a character node) in tuple
    # sort all tuple item by their second element (at position 1) in the array
    # convert evey item in the letter frequency dictionary 'letter_freq' into a tuple consist of a character and number
    list_nodes_objects = sorted(huffman_feq.items(), key=lambda x: x[1], reverse=False)
    # print(list_nodes_objects)  # test code

    # this while loop iterates
    while len(list_nodes_objects) > 1:
        """
        This while loop iterates the list of node tuple until one item is left.
        The goal of this loop is to generate 1 node, which contains all the combined nodes
        """
        # take the 2 least weight nodes
        (character_1, freq_1) = list_nodes_objects[0]  # tuple (character, freq)
        (character_2, freq_2) = list_nodes_objects[1]
        list_nodes_objects = list_nodes_objects[2:]  # list of nodes updated after 2 nodes are taken out

        # print("list_nodes_objects ", list_nodes_objects)  # test code

        new_node = Node(character_1, character_2)  # new node, contains the 2 combined smallest node in an object
        list_nodes_objects.append(
            (new_node, freq_1 + freq_2))  # put the combined node back to the array of node with new weight
        # (combined node, sum of weight)

        # sort the array in order after a new node is append
        list_nodes_objects = sorted(list_nodes_objects, key=lambda x: x[1], reverse=False)

    # print("sorted list_nodes_objects ", list_nodes_objects)  # test code

    # tree traversal

    print("decompressing...%..")

    decompress_string = ""  # store the decoding result
    print(decompress_string)

    current_node = list_nodes_objects[0][0]  # root node

    for i in binary_content:
        # if a node is a string, that means it is a leaf
        if type(current_node) is str:
            decompress_string += current_node  # the leaf contains the character, add to string
            current_node = list_nodes_objects[0][0]  # reset traversal from root

        # create a tuple, extract items (left_item, right_item) from a nodes' daughter

        (left_item, right_item) = current_node.daughters()

        if int(i) == 0:
            # go to 'left'
            current_node = left_item

        elif int(i) == 1:
            # go to 'right'
            current_node = right_item
        else:
            print("Error!\nNon_binary content detected, abort decompression.")
            exit()

    # print("result: ", decompress_string)  # test code

    # write file
    file_name = filename[:-4]  # assuming the file to be decompressed is .bin
    open_file = file_name + '-Decompressed' + '.txt'

    f = open(open_file, "w", encoding="utf_8_sig")  # create new file
    f.write(decompress_string)  # write text
    f.close()

    print("decompression completed!")
    end_decompress = float(
        time.process_time())  # end measure time in this line to check processing time for this section
    print(str(end_decompress - start_decompress) + " second taken to compress file!")
    main()


def file_exist(file_name):
    """This function detects if the file is placed in the same folder with the program"""
    # if does not exist print warning and back to main
    try:
        with open(file_name, encoding="utf_8_sig") as f:
            test = file_name
    except:
        FileNotFoundError
        print("Warning! " + file_name + " does not exist.\nPlease try again.")
        main()
    return


def main():
    """This section decide what to do with the file"""
    message = """
    +----------------------------------------+
    |ECM1414 DSA lossless compression project|
    |          ____________________          |
    | Enter a file name ends either with:    |
    | ".txt" to compress or                  |
    | ".bin" to decompress                   |
    |                                        |
    | Enter 0 to exit program                |
    +----------------------------------------+
    """
    print(message)
    file_name = input("Please enter the full file name:")

    if file_name[-4:] == ".txt":
        # compress file
        file_exist(file_name)
        # print("1",file_name)  # test code
        compression(file_name)
    elif file_name[-4:] == ".bin":
        # decompress file
        file_exist(file_name)
        # print("2",file_name)  # test code
        decompress(file_name)
    elif file_name == "0":
        print("exiting...%...")
        exit()
    else:
        print("Only accept .txt or .bin file format")
        main()


main()  # program starts here
