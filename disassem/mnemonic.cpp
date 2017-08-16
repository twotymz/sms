
#include <stdio.h>
#include "mnemonic.h"

#define A(f) strcpy(buf, f)
#define I(f) sprintf(buf, f, decoded->immediate)

char *mnemonic(const decode_s *decoded, char *buf)
{
  switch(decoded->opcode)
  {
    default:
      sprintf(buf, "%02x is unhandled", decoded->opcode);
      break;

    case 0x00: A("NOP"); break;
    case 0x01: I("LD BC, %02X"); break;
    case 0x02: A("LD (BC), A"); break;
    case 0x03: A("INC BC"); break;
    case 0x04: A("INC B"); break;
    case 0x05: A("DEC B"); break;
    case 0x06: I("LD B, %X"); break;
    case 0x07: A("RLOA"); break;
    case 0x08: A("EX AF, AF'"); break;
    case 0x09: A("ADD HL, BC"); break;
    case 0x0A: A("LD A, (BC)"); break;
    case 0x0B: A("DEC BC"); break;
    case 0x0C: A("INC C"); break;
    case 0x0D: A("DEC C"); break;
    case 0x0E: I("LD C, %X"); break;
    case 0x0F: A("RROA"); break;

    case 0x10: I("DJNZ %0X"); break;
    case 0x11: I("LD DE, %04X"); break;
    case 0x12: A("LD (DE), A"); break;
    case 0x13: A("INC DE"); break;
    case 0x14: A("INC D"); break;
    case 0x15: A("DEC D"); break;
    case 0x16: I("LD D, %0X"); break;
    case 0x17: A("RLA"); break;
    case 0x18: I("JR %0X"); break;
    case 0x19: A("ADD HL, DE"); break;
    case 0x1A: A("LD A, (DE)"); break;
    case 0x1B: A("DEC DE"); break;
    case 0x1C: A("INC E"); break;
    case 0x1D: A("DEC E"); break;
    case 0x1E: I("LD E, %0X"); break;
    case 0x1F: A("RRA"); break;

    case 0x20: I("JR NZ, %0X"); break;
    case 0x21: I("LD HL, %04X"); break;
    case 0x22: I("LD (%04X), HL"); break;
    case 0x23: A("INC HL"); break;
    case 0x24: A("INC H"); break;
    case 0x25: A("DEC H"); break;
    case 0x26: I("LD H, %0X"); break;
    case 0x27: A("DAA"); break;
    case 0x28: I("JR Z, %0X"); break;
    case 0x29: A("ADD HL, HL"); break;
    case 0x2A: I("LD HL, (%04X)"); break;
    case 0x2B: A("DEC HL"); break;
    case 0x2C: A("INC L"); break;
    case 0x2D: A("DEC L"); break;
    case 0x2E: I("LD L, %0X"); break;
    case 0x2F: A("CPL"); break;

    case 0x30: I("JR NC, %X"); break;
    case 0x31: I("LD SP, %04X"); break;
    case 0x32: I("LD (%04X), A"); break;
    case 0x33: A("INC SP"); break;
    case 0x34: A("INC (HL)"); break;
    case 0x35: A("DEC (HL)"); break;
    case 0x36: I("LD (HL), %X"); break;
    case 0x37: A("SCF"); break;
    case 0x38: I("JR C, %X"); break;
    case 0x39: A("ADD HL, SP"); break;
    case 0x3A: I("LD A, (%04X)"); break;
    case 0x3B: A("DEC SP"); break;
    case 0x3C: A("INC A"); break;
    case 0x3D: A("DEC A"); break;
    case 0x3E: I("LD A, %0X"); break;
    case 0x3F: A("CCF"); break;

    case 0x40: A("LD B, B"); break;
    case 0x41: A("LD B, C"); break;
    case 0x42: A("LD B, D"); break;
    case 0x43: A("LD B, E"); break;
    case 0x44: A("LD B, H"); break;
    case 0x45: A("LD B, L"); break;
    case 0x46: A("LD B, (HL)"); break;
    case 0x47: A("LD B, B"); break;
    case 0x48: A("LD C, B"); break;
    case 0x49: A("LD C, C"); break;
    case 0x4A: A("LD C, D"); break;
    case 0x4B: A("LD C, E"); break;
    case 0x4C: A("LD C, H"); break;
    case 0x4D: A("LD C, L"); break;
    case 0x4E: A("LD C, (HL)"); break;
    case 0x4F: A("LD C, A"); break;

    case 0x50: A("LD D, B"); break;
    case 0x51: A("LD D, C"); break;
    case 0x52: A("LD D, D"); break;
    case 0x53: A("LD D, E"); break;
    case 0x54: A("LD D, H"); break;
    case 0x55: A("LD D, L"); break;
    case 0x56: A("LD D, (HL)"); break;
    case 0x57: A("LD D, A"); break;
    case 0x58: A("LD E, B"); break;
    case 0x59: A("LD E, C"); break;
    case 0x5A: A("LD E, D"); break;
    case 0x5B: A("LD E, E"); break;
    case 0x5C: A("LD E, H"); break;
    case 0x5D: A("LD E, L"); break;
    case 0x5E: A("LD E, (HL)"); break;
    case 0x5F: A("LD E, A"); break;

    case 0x60: A("LD H, B"); break;
    case 0x61: A("LD H, C"); break;
    case 0x62: A("LD H, D"); break;
    case 0x63: A("LD H, E"); break;
    case 0x64: A("LD H, H"); break;
    case 0x65: A("LD H, L"); break;
    case 0x66: A("LD H, (HL)"); break;
    case 0x67: A("LD H, A"); break;
    case 0x68: A("LD L, B"); break;
    case 0x69: A("LD L, C"); break;
    case 0x6A: A("LD L, D"); break;
    case 0x6B: A("LD L, E"); break;
    case 0x6C: A("LD L, H"); break;
    case 0x6D: A("LD L, L"); break;
    case 0x6E: A("LD L, (HL)"); break;
    case 0x6F: A("LD L, A"); break;

    case 0x70: A("LD (HL), B"); break;
    case 0x71: A("LD (HL), C"); break;
    case 0x72: A("LD (HL), D"); break;
    case 0x73: A("LD (HL), E"); break;
    case 0x74: A("LD (HL), H"); break;
    case 0x75: A("LD (HL), L"); break;
    case 0x76: A("HALT"); break;
    case 0x77: A("LD (HL), A"); break;
    case 0x78: A("LD A, B"); break;
    case 0x79: A("LD A, C"); break;
    case 0x7A: A("LD A, D"); break;
    case 0x7B: A("LD A, E"); break;
    case 0x7C: A("LD A, H"); break;
    case 0x7D: A("LD A, L"); break;
    case 0x7E: A("LD A, (HL)"); break;
    case 0x7F: A("LD A, A"); break;

    case 0x80: A("ADD A, B"); break;
    case 0x81: A("ADD A, C"); break;
    case 0x82: A("ADD A, D"); break;
    case 0x83: A("ADD A, E"); break;
    case 0x84: A("ADD A, H"); break;
    case 0x85: A("ADD A, L"); break;
    case 0x86: A("ADD A, (HL)"); break;
    case 0x87: A("ADD A, A"); break;
    case 0x88: A("ADC A, B"); break;
    case 0x89: A("ADC A, C"); break;
    case 0x8A: A("ADC A, D"); break;
    case 0x8B: A("ADC A, E"); break;
    case 0x8C: A("ADC A, H"); break;
    case 0x8D: A("ADC A, L"); break;
    case 0x8E: A("ADC A, (HL)"); break;
    case 0x8F: A("ADC A, A"); break;

    case 0x90: A("SUB B"); break;
    case 0x91: A("SUB C"); break;
    case 0x92: A("SUB D"); break;
    case 0x93: A("SUB E"); break;
    case 0x94: A("SUB H"); break;
    case 0x95: A("SUB L"); break;
    case 0x96: A("SUB (HL)"); break;
    case 0x97: A("SUB A"); break;
    case 0x98: A("SBC A, B"); break;
    case 0x99: A("SBC A, C"); break;
    case 0x9A: A("SBC A, D"); break;
    case 0x9B: A("SBC A, E"); break;
    case 0x9C: A("SBC A, H"); break;
    case 0x9D: A("SBC A, L"); break;
    case 0x9E: A("SBC A, (HL)"); break;
    case 0x9F: A("SBC A, A"); break;

    case 0xA0: A("AND B"); break;
    case 0xA1: A("AND C"); break;
    case 0xA2: A("AND D"); break;
    case 0xA3: A("AND E"); break;
    case 0xA4: A("AND H"); break;
    case 0xA5: A("AND L"); break;
    case 0xA6: A("AND (HL)"); break;
    case 0xA7: A("AND A"); break;
    case 0xA8: A("XOR B"); break;
    case 0xA9: A("XOR C"); break;
    case 0xAA: A("XOR D"); break;
    case 0xAB: A("XOR E"); break;
    case 0xAC: A("XOR H"); break;
    case 0xAD: A("XOR L"); break;
    case 0xAE: A("XOR (HL)"); break;
    case 0xAF: A("XOR A"); break;

    case 0xB0: A("OR B"); break;
    case 0xB1: A("OR C"); break;
    case 0xB2: A("OR D"); break;
    case 0xB3: A("OR E"); break;
    case 0xB4: A("OR H"); break;
    case 0xB5: A("OR L"); break;
    case 0xB6: A("OR (HL)"); break;
    case 0xB7: A("OR A"); break;
    case 0xB8: A("CP B"); break;
    case 0xB9: A("CP C"); break;
    case 0xBA: A("CP D"); break;
    case 0xBB: A("CP E"); break;
    case 0xBC: A("CP H"); break;
    case 0xBD: A("CP L"); break;
    case 0xBE: A("CP (HL)"); break;
    case 0xBF: A("CP A"); break;

    case 0xC0: A("RET NC"); break;
    case 0xC1: A("POP BC"); break;
    case 0xC2: I("JP NC, %04X"); break;
    case 0xC3: I("JP %04X"); break;
    case 0xC4: I("CALL NZ, %04X"); break;
    case 0xC5: A("PUSH BC"); break;
    case 0xC6: I("ADD A, %X"); break;
    case 0xC7: A("RST 00h"); break;
    case 0xC8: A("RET Z"); break;
    case 0xC9: A("RET"); break;
    case 0xCA: I("JP Z, %04X"); break;
    case 0xCB: break;
    case 0xCC: I("CALL Z, %04X"); break;
    case 0xCD: I("CALL %04X"); break;
    case 0xCE: I("ADC A, %0X"); break;
    case 0xCF: A("RST 08h"); break;

    case 0xD0: A("RET NC"); break;
    case 0xD1: A("POP DE"); break;
    case 0xD2: I("JP NC, %04X"); break;
    case 0xD3: I("OUT (%X), A"); break;
    case 0xD4: I("CALL NC, %04X"); break;
    case 0xD5: A("PUSH DE"); break;
    case 0xD6: I("SUB %0X"); break;
    case 0xD7: A("RST 10h"); break;
    case 0xD8: A("RET C"); break;
    case 0xD9: A("EN"); break;
    case 0xDA: I("JP C, %04X"); break;
    case 0xDB: I("IN A, (%0X)"); break;
    case 0xDC: I("CALL C, %04X"); break;
    case 0xDD: break;
    case 0xDE: I("ABC A, %0X"); break;
    case 0xDF: A("RST 18h"); break;

    case 0xE0: A("RET PO"); break;
    case 0xE1: A("POP HL"); break;
    case 0xE2: I("JP PO, %04X");
    case 0xE3: A("EX (SP), HL"); break;
    case 0xE4: I("CALL PO, %04X"); break;
    case 0xE5: A("PUSH HL"); break;
    case 0xE6: I("AND %X"); break;
    case 0xE7: A("RST 20h"); break;
    case 0xE8: A("RET PE"); break;
    case 0xE9: A("JP (HL)"); break;
    case 0xEA: I("JP PE, %04X"); break;
    case 0xEB: A("EX DE, HL"); break;
    case 0xEC: I("CALL PE, %04X"); break;
    case 0xED: break;
    case 0xEE: I("XOR %X"); break;
    case 0xEF: A("RST 28h"); break;

    case 0xF0: A("RET P"); break;
    case 0xF1: A("POP AF"); break;
    case 0xF2: I("JP P, %04X"); break;
    case 0xF3: A("DI"); break;
    case 0xF4: I("CALL P, %04X"); break;
    case 0xF5: A("PUSH AF"); break;
    case 0xF6: I("OR %X"); break;
    case 0xF7: A("RST 30h"); break;
    case 0xF8: A("RET M"); break;
    case 0xF9: A("LD SP, HL"); break;
    case 0xFA: I("JP M, %04X"); break;
    case 0xFB: A("EI"); break;
    case 0xFC: I("CALL M, %04X"); break;
    case 0xFD: break;
    case 0xFE: I("CP %X"); break;
    case 0xFF: A("RST 38h"); break;

  }

  return buf;
}
