#ifndef SMS_INCLUDED
#define SMS_INCLUDED

#include <stdlib.h>
#include "sms_types.h"

extern size_t smsRomBytes();
extern int smsReadRom(const char *path);
extern byte_t smsReadByte(word_t pc);
extern word_t smsReadWord(word_t pc);

#endif
