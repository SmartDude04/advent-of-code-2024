import enum
import re
import copy


class Register(enum.Enum):
    A = 0
    B = 1
    C = 2


result = ""


def perform_instruction(opcode: int, operand: int, registers: dict[Register, int], instruction_pointer: int, ) -> int:
    if opcode == 0:
        return adv(operand, registers, instruction_pointer)
    elif opcode == 1:
        return bxl(operand, registers, instruction_pointer)
    elif opcode == 2:
        return bst(operand, registers, instruction_pointer)
    elif opcode == 3:
        return jnz(operand, registers, instruction_pointer)
    elif opcode == 4:
        return bxc(operand, registers, instruction_pointer)
    elif opcode == 5:
        return out(operand, registers, instruction_pointer)
    elif opcode == 6:
        return bdv(operand, registers, instruction_pointer)
    elif opcode == 7:
        return cdv(operand, registers, instruction_pointer)
    else:
        raise ValueError('Invalid opcode')


def get_combo_operand(literal_operand: int, registers: dict[Register, int]) -> int:
    if 0 <= literal_operand <= 3:
        return literal_operand
    elif literal_operand == 4:
        return registers[Register.A]
    elif literal_operand == 5:
        return registers[Register.B]
    elif literal_operand == 6:
        return registers[Register.C]
    else:
        raise ValueError(f"Failure converting literal operand {literal_operand} into combo operand")


def adv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.A] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
    return instruction_pointer + 2


def bxl(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.B] = registers[Register.B] ^ operand
    return instruction_pointer + 2


def bst(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.B] = get_combo_operand(operand, registers) % 8
    return instruction_pointer + 2


def jnz(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    if registers[Register.A] != 0:
        return operand
    return instruction_pointer + 2


def bxc(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.B] = registers[Register.B] ^ registers[Register.C]
    return instruction_pointer + 2


def out(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    global result
    result += str(get_combo_operand(operand, registers) % 8) + ","
    return instruction_pointer + 2


def bdv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.B] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
    return instruction_pointer + 2


def cdv(operand: int, registers: dict[Register, int], instruction_pointer: int) -> int:
    registers[Register.C] = registers[Register.A] // pow(2, get_combo_operand(operand, registers))
    return instruction_pointer + 2


def run_program(registers: dict[Register, int], program: list[int]) -> str:
    global result
    program_registers = copy.deepcopy(registers)
    program_program = copy.deepcopy(program)

    result = ""
    inst_pointer = 0
    while inst_pointer < len(program_program):
        inst_pointer = perform_instruction(program[inst_pointer], program[inst_pointer + 1], program_registers,
                                           inst_pointer)
    return result


registers: dict[Register, int] = {Register.A: 0, Register.B: 0, Register.C: 0}
program: list[int] = []
with open("input.txt") as f:
    while line := f.readline():
        line = line.strip()
        if line.find("Register") != -1:
            if line.find("A") != -1:
                registers[Register.A] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("B") != -1:
                registers[Register.B] = int(re.findall(r"[0-9]+", line)[0])
            elif line.find("C") != -1:
                registers[Register.C] = int(re.findall(r"[0-9]+", line)[0])
        elif len(line) > 0:
            program = [int(num) for num in re.findall(r"[0-9]+", line)]


print(run_program(registers, program))