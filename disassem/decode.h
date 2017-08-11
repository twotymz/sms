#ifndef DECODE_INCLUDED
#define DECODE_INCLUDED

#include "sms.h"

struct decode_s {
  byte_t bytes;
  byte_t opcode;
  byte_t prefix;
  byte_t displacement;
  word_t immediate;
};

extern byte_t decode(SMS *sms, word_t pc, decode_s *decode);

#endif
