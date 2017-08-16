
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sms.h"
#include "decode.h"


static void ddcb_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
}


static void fdcb_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
}


static void cb_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
  unsigned char opcode = sms->readByte(pc);

  unsigned char x = (opcode & 0xC0) >> 6;
  unsigned char y = (opcode & 0x38) >> 3;
  unsigned char z = (opcode & 0x7);
  unsigned char p = y >> 1;
  unsigned char q = y & 0x1;

  decoded->bytes++;
  decoded->prefix = 0xCB;
  decoded->opcode = opcode;
  decoded->displacement = 0;
  decoded->immediate = 0;
}


static void dd_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
  byte_t next_byte = sms->readByte(pc + 1);
  if (next_byte == 0xDD || next_byte == 0xED || next_byte == 0xFD) {
    decoded->bytes++;
    decoded->prefix = 0xDD;
    decoded->displacement = 0;
    decoded->immediate = 0;
  }
  else if (next_byte == 0xCB) {
    ddcb_prefix(sms, pc + 1, decoded);
    decoded->prefix = 0xDD;
  }
  else {
    decode(sms, pc + 1, decoded);
  }

  decoded->bytes += 1;
}


static void ed_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
}


static void fd_prefix(SMS *sms, word_t pc, decode_s *decoded)
{
  byte_t next_byte = sms->readByte(pc + 1);
  if (next_byte == 0xDD || next_byte == 0xED || next_byte == 0xFD) {
    decoded->bytes++;
    decoded->prefix = 0xDD;
    decoded->displacement = 0;
    decoded->immediate = 0;
  }
  else if (next_byte == 0xCB) {
    fdcb_prefix(sms, pc + 1, decoded);
  }
  else {
    decode(sms, pc + 1, decoded);
    decoded->prefix = 0xFD;
  }

  decoded->bytes += 1;
}


byte_t decode(SMS *sms, word_t pc, decode_s *decoded)
{
  unsigned char opcode = sms->readByte(pc);

  unsigned char x = (opcode & 0xC0) >> 6;
  unsigned char y = (opcode & 0x38) >> 3;
  unsigned char z = (opcode & 0x7);
  unsigned char p = y >> 1;
  unsigned char q = y & 0x1;

  decoded->bytes = 1;
  decoded->prefix = 0;
  decoded->opcode = opcode;
  decoded->displacement = 0;
  decoded->immediate = 0;

  if (x == 0) {
    if (y >= 2 && y <= 7) {
        decoded->displacement = sms->readByte(pc + decoded->bytes);
        decoded->bytes++;
    }
    else if (z == 1) {
      if (q == 0) {
        decoded->immediate = sms->readWord(pc + decoded->bytes);
        decoded->bytes += 2;
      }
    }
    else if (z == 2) {
      if (p == 2) {
        decoded->immediate = sms->readWord(pc + decoded->bytes);
        decoded->bytes += 2;
      }
      else if (p == 3) {
        decoded->immediate = sms->readByte(pc + decoded->bytes);
        decoded->bytes += 2;
      }
    }
    else if (z == 6) {
      decoded->immediate = sms->readByte(pc + decoded->bytes);
      decoded->bytes++;
    }
  }
  else if (x == 3) {
    if (z == 2) {
      decoded->immediate = sms->readWord(pc + decoded->bytes);
      decoded->bytes += 2;
    }
    else if (z == 3) {
      if (y == 0) {
        decoded->immediate = sms->readWord(pc + decoded->bytes);
        decoded->bytes += 2;
      }
      else if (y == 1) {
        cb_prefix(sms, pc + decoded->bytes, decoded);
      }
      else if (y == 2 || y == 3) {
        decoded->immediate = sms->readByte(pc + decoded->bytes);
        decoded->bytes++;
      }
    }
    else if (z == 4) {
      decoded->immediate = sms->readWord(pc + decoded->bytes);
      decoded->bytes += 2;
    }
    else if (z == 5) {
      if (q == 1) {
        if (p == 0) {
          decoded->immediate = sms->readWord(pc + decoded->bytes);
          decoded->bytes += 2;
        }
        else if (p == 1) {
          dd_prefix(sms, pc + decoded->bytes, decoded);
        }
        else if (p == 2) {
          ed_prefix(sms, pc + decoded->bytes, decoded);
        }
        else if (p == 3) {
          fd_prefix(sms, pc + decoded->bytes, decoded);
        }
      }
    }
    else if (z == 6) {
      decoded->immediate = sms->readByte(pc + decoded->bytes);
      decoded->bytes++;
    }
  }

  return decoded->bytes;
}
