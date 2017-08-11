#ifndef SMS_INCLUDED
#define SMS_INCLUDED

#include "sms_types.h"

class SMS {

  public:

    SMS() {
      m_rom = 0;
      m_bytes = 0;
    }

    ~SMS();

    size_t bytes() const {
      return m_bytes;
    }

    int load(const char *path);

    byte_t readByte(word_t pc) const {
      return m_rom[pc];
    }

    word_t readWord(word_t pc) const {
      return m_rom[pc] | m_rom[pc+1] << 8;
    }

  private:

    unsigned char *m_rom;
    size_t m_bytes;
};

#endif
