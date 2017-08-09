
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "sms_types.h"

static unsigned char *s_rom = 0;
static size_t s_rom_bytes = 0;


size_t smsRomBytes()
{
  return s_rom_bytes;
}


byte_t smsReadByte(word_t pc)
{
  return s_rom[pc];
}


word_t smsReadWord(word_t pc)
{
  return s_rom[pc] | s_rom[pc+1] << 8;
}


int smsReadRom(const char *path)
{
  FILE *fptr = fopen(path, "rb");
  size_t rom_size = 0;
  int error = 0;

  if(!fptr){
    fprintf(stderr, "Failed opening %s for reading.\n", path);
    return -1;
  }

  s_rom_bytes = 0;

  while(true){

    rom_size += 32 * 1024;
    s_rom = (unsigned char *)realloc(s_rom, sizeof(unsigned char) * rom_size);

    if(!s_rom){
      fprintf(stderr, "Failed allocating memory for rom. (%s).\n", strerror(errno));
      error = 1;
      break;
    }

    size_t nbytes = fread(s_rom + s_rom_bytes, 1, 32 * 1024, fptr);
    s_rom_bytes += nbytes;

    if(nbytes < 32 * 1024){

      if(feof(fptr)){
        break;
      }

      fprintf(stderr, "Failed reading ROM into memory. (%s)\n", strerror(ferror(fptr)));
      error = 1;
      break;
    }
  }

  fclose(fptr);
  return error;
}
