
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "sms.h"


SMS::~SMS()
{
  if(m_rom) {
    free(m_rom);
  }
}


int SMS::load(const char *path)
{
  FILE *fptr = fopen(path, "rb");
  size_t rom_size = 0;
  int error = 0;

  if(!fptr) {
    fprintf(stderr, "Failed opening %s for reading.\n", path);
    return -1;
  }

  m_bytes = 0;

  if (m_rom) {
    free(m_rom);
    m_rom = 0;
  }

  while(true) {

    rom_size += 32 * 1024;
    m_rom = (unsigned char *)realloc(m_rom, sizeof(unsigned char) * rom_size);

    if(!m_rom) {
      fprintf(stderr, "Failed allocating memory for rom. (%s).\n", strerror(errno));
      error = 1;
      break;
    }

    size_t nbytes = fread(m_rom + m_bytes, 1, 32 * 1024, fptr);
    m_bytes += nbytes;

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
