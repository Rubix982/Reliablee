#!/usr/bin/env python3

# Package imports
from dotenv import load_dotenv
import os

load_dotenv() # take environment variables from .env

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