
#include <stdio.h>
#include "sms.h"
#include "decode.h"

int main(int argc, char *argv[])
{
  if(argc != 2){
    fprintf(stderr, "Usage: %s <path to rom>\n", argv[0]);
    return -1;
  }

  if(smsReadRom(argv[1])){
    return -1;
  }

  decode(0);

  return 0;
}
