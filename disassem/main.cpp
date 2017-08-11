
#include <stdio.h>
#include "sms.h"
#include "decode.h"
#include "mnemonic.h"

int main(int argc, char *argv[])
{
  if(argc != 2){
    fprintf(stderr, "Usage: %s <path to rom>\n", argv[0]);
    return -1;
  }

  SMS sms;

  if(sms.load(argv[1])){
    return -1;
  }

  size_t pc = 0;
  while(pc < sms.bytes ()) {
    
    decode_s decoded;
    char buf[32];

    pc += decode (&sms, pc, &decoded);
    printf ("%04llx  %04x  %s\n", pc, decoded.opcode, mnemonic(&decoded, buf));
  }

  return 0;
}
