import os
import re
import sys


class SymbolTable:
    symbols = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'SCREEN': 0x4000,
        'KBD': 0x6000
    }
    nextAddress = 16

    def addEntry(self, symbol, address):
        self.symbols[symbol] = address

    def _contains(self, symbol):
        if symbol in self.symbols:
            return True
        else:
            return False

    def GetAddress(self, symbol):
        if not self._contains(symbol):
            self.symbols[symbol] = self.nextAddress
            self.nextAddress += 1
        return self.symbols[symbol]


class Code:
    def __init__(self, file, symbol_table):
        self.file = file
        self.symbol_table = symbol_table

    def _write(self, line):
        self.file.write(line + '\n')

    def _dest(self, dest):
        destination = ""
        if 'A' in dest:
            destination += '1'
        else:
            destination += '0'
        if 'D' in dest:
            destination += '1'
        else:
            destination += '0'
        if 'M' in dest:
            destination += '1'
        else:
            destination += '0'
        return destination

    def _comp(self, comp):
        if 'M' in comp:
            comp = comp.replace('M', 'A')
            a = '1'
        else:
            a = '0'

        if comp == '0':
            return a + "101010"
        if comp == '1':
            return a + "111111"
        if comp == '-1':
            return a + "111010"
        if comp == 'D':
            return a + "001100"
        if comp == 'A':
            return a + "110000"
        if comp == '!D':
            return a + "001101"
        if comp == '!A':
            return a + "110001"
        if comp == '-D':
            return a + "001111"
        if comp == '-A':
            return a + "110011"
        if comp == 'D+1':
            return a + "011111"
        if comp == 'A+1':
            return a + "110111"
        if comp == 'D-1':
            return a + "001110"
        if comp == 'A-1':
            return a + "110010"
        if comp == 'D+A':
            return a + "000010"
        if comp == 'D-A':
            return a + "010011"
        if comp == 'A-D':
            return a + "000111"
        if comp == 'D&A':
            return a + "000000"
        if comp == 'D|A':
            return a + "010101"

    def _jump(self, jump):
        if jump == 'JGT':
            return "001"
        if jump == 'JEQ':
            return "010"
        if jump == 'JGE':
            return "011"
        if jump == 'JLT':
            return "100"
        if jump == 'JNE':
            return "101"
        if jump == 'JLE':
            return "110"
        if jump == 'JMP':
            return "111"
        return "000"

    def _encoded_a(self, instruction):
        address = instruction[1:]
        if not address.isdigit():
            address = self.symbol_table.GetAddress(address)
        return "{0:016b}".format(int(address))

    def _encoded_c(self, instruction):
        # dest=comp;jump
        if ';' in instruction:
            dandc, jump = instruction.split(';')
        else:
            jump = ""
            dandc = instruction

        if '=' in dandc:
            dest, comp = dandc.split('=')
        else:
            dest = ""
            comp = dandc

        return "111" + self._comp(comp) + self._dest(dest) + self._jump(jump)

    def encode(self, instruction):
        if instruction[0] == '@':
            encoded_instruction = self._encoded_a(instruction)
        else:
            encoded_instruction = self._encoded_c(instruction)
        self._write(encoded_instruction)


class Parser:
    def __init__(self, code, symbol_table):
        self.coded = code
        self.symbol_table = symbol_table

    def _replace(self, line):
        line = re.sub('//.*', '', line)
        line = re.sub(r'\s', '', line)
        return line

    def parse(self, filename):
        instructions = []
        with open(filename) as file:
            for line in file.readlines():
                line = self._replace(line)
                if len(line):
                    if line[0] == '(':
                        self.symbol_table.addEntry(line[1:-1], len(instructions))
                    else:
                        instructions.append(line)
        for instruction in instructions:
            self.coded.encode(instruction)


if __name__ == '__main__':
    asm_filename = 'RectL.asm'
    hack_filename = os.path.splitext(asm_filename)[0] + ".hack"
    with open(hack_filename, "w") as hack_file:
        symbol_table = SymbolTable()
        writer = Code(hack_file, symbol_table)
        parser = Parser(writer, symbol_table)
        parser.parse(asm_filename)
