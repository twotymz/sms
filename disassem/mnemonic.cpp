
#include <stdio.h>
#include "mnemonic.h"

char *mnemonic(const decode_s *decoded, char *buf)
{
  switch(decoded->opcode)
  {
    default:
      sprintf(buf, "%02x is unhandled", decoded->opcode);
      break;
  }

  return buf;
}
