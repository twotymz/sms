
#include <stdio.h>
#include <stdlib.h>
#include "sms_types.h"
#include "sms.h"

word_t decode(word_t pc)
{
  unsigned char opcode = smsReadByte(pc);

  unsigned char x = (opcode & 0xC0) >> 6;
  unsigned char y = (opcode & 0x38) >> 3;
  unsigned char z = (opcode & 0x7);
  unsigned char p = y >> 1;
  unsigned char q = y & 0x1;



  return 1;
}
