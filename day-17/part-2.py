import enum
import re
import copy

A = 0
B = 1
C = 2

#
#
# def perform_instruction(opcode: int, operand: int, registers: dict[Register, int], instruction_pointer: int, ) -> int:
#     if opcode == 0:
#         return adv(operand, registers, instruction_pointer)
#     elif opcode == 1:
#         return bxl(operand, registers, instruction_pointer)
#     elif opcode == 2:
#         return bst(operand, registers, instruction_pointer)
#     elif opcode == 3:
#         return jnz(operand, registers, instruction_pointer)
#     elif opcode == 4:
#         return bxc(operand, registers, instruction_pointer)
#     elif opcode == 5:
#         return out(operand, registers, instruction_pointer)
#     elif opcode == 6:
#         return bdv(operand, registers, instruction_pointer)
#     elif opcode == 7:
#         return cdv(operand, registers, instruction_pointer)
#     else:
#         raise ValueError('Invalid opcode')
#
#
# def get_combo_operand(literal_operand: int, registers: dict[Register, int]) -> int:
#     if 0 <= literal_operand <= 3:
#         return literal_operand
#     elif literal_operand == 4:
#         return registers[Register.A]
#     elif literal_operand == 5:
#         return registers[Register.B]
#     elif literal_operand == 6:
#         return registers[Register.C]
#     else:
#         raise ValueError(f"Failure converting literal operand {literal_operand} into combo operand")
#
#
# def adv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"adv: regA <- regA / 2^{get_combo_operand(operand, registers)} operand {operand}")
#     registers[Register.A] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
#     return instruction_pointer + 2
#
#
# def bxl(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"bxl: regB <- regB ^ {operand}")
#     registers[Register.B] = registers[Register.B] ^ operand
#     return instruction_pointer + 2
#
#
# def bst(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"bst: regB({registers[Register.B]}) <- {get_combo_operand(operand, registers)} % 8 operand {operand}")
#     registers[Register.B] = get_combo_operand(operand, registers) % 8
#     return instruction_pointer + 2
#
#
# def jnz(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     if registers[Register.A] != 0:
#         print(f"jnz: inst_ptr <- {operand}")
#         print(f"Registers: {registers}")
#         print("--------\n")
#         return operand
#     print(f"jnz: inst_ptr <- {instruction_pointer + 2}")
#     print(f"Registers: {registers}")
#     print("--------\n")
#     return instruction_pointer + 2
#
#
# def bxc(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"bxc: regB <- regB({registers[Register.B]}) ^ regC({registers[Register.C]})")
#     registers[Register.B] = registers[Register.B] ^ registers[Register.C]
#     return instruction_pointer + 2
#
#
# def out(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"out: result <- {get_combo_operand(operand, registers) % 8} operand {operand}")
#     global result
#     result += str(get_combo_operand(operand, registers) % 8) + ","
#     return instruction_pointer + 2
#
#
# def bdv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"bdv: regB <- regA / 2^{get_combo_operand(operand, registers)}")
#     registers[Register.B] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
#     return instruction_pointer + 2
#
#
# def cdv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
#     print(f"cdv: regC <- regA / 2^{get_combo_operand(operand, registers)} operand {operand}")
#     registers[Register.C] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
#     return instruction_pointer + 2


def execute_loop(a: int) -> str:
    result = 0
    b = (a % 8) ^ 5
    c = a // pow(2, b)
    b = b ^ 6 ^ c
    return b % 8


registers: list[int] = [0, 0, 0]
program: list[int] = []
with open("input.txt") as f:
    while line := f.readline():
        line = line.strip()
        if line.find("Register") != -1:
            if line.find("A") != -1:
                registers[A] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("B") != -1:
                registers[B] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("C") != -1:
                registers[C] = int(re.findall(r"[0-9]+", line)[0])
        elif len(line) > 0:
            program = [int(num) for num in re.findall(r"[0-9]+", line)]


#   Notes:
# - Program is a loop that runs floor(logbase8(start regA)) + 1 times
# - Output is last 3 bits of register b

initial = 34615120
while initial != 0:
    print(execute_loop(initial))
    initial = initial // 8