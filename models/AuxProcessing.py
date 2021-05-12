#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import binascii
import os

load_dotenv()  # take environment variables from .env


class AuxProcessing:

    @staticmethod
    def IntegersToBinary(integer_representation) -> str:
        '''This assumes that each integer in the integer representation should be representated as 4 bits, that is, '0' in dec is '0000' in binary, even though '0' can also be used. This is done so for ease of parsing here'''
        return str(''.join([((int(os.environ['ENTRY_LENGTH']) - len(bin_value)) * '0') + bin_value for bin_value in [bin(int(character))[2:] for character in str(integer_representation)]]))

    @staticmethod
    def BinaryToIntegers(binary_representation) -> int:
        '''This assumes that each representation is
        split into a nibble format, that is, the number
        of bits to represent a single value consists of 4 bits, regardless of the value, from 0000 to 1111'''
        return int(''.join([str(int(binary_representation[index:index+4], 2)) for index in range(0, len(binary_representation), 4)]))

    @staticmethod
    def UTF8ToBinary(utf8_representation, encoding='utf-8', errors='surrogatepass') -> str:
        '''According to the UTF-8 standard,

        Unciode Range           # UTF-8 Bytes           Characters
        \u000000-\u00007F       1 byte                  The first 128 characters (US-ASCII)
        \u000080-\u0007FF       2 bytes                 Latin characters with diacritics and Greek, etc
        \u000800-\u00FFFF       3 bytes                 Rest of the basic multilingual plane
        \u010000-\u10FFFF       4 bytes                 All the other unicode characters

        Thus, for now, I'm going to represent a character only as 1 byte because of the files that I have
        can be easily be represented as ASCII. Which means each character will be of 8 bits exactly, from
        0-127 in the ASCII representation
        '''
        bits = bin(int(binascii.hexlify(
            utf8_representation.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    @staticmethod
    def BinaryToUTF8(binary_representation, encoding='utf-8', errors='surrogatepass') -> str:
        return AuxProcessing.IntegerToBytes(int(binary_representation, 2)).decode(encoding, errors)

    @staticmethod
    def IntegerToBytes(integer_representation) -> bytes:
        hex_string = '%x' % integer_representation
        number = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(number + (number & 1)))
