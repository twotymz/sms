

class CPU :

    def __init__ (self) :

        self.regs = {
                'af' : [0, 0],
                'bc' : [0, 0],
                'de' : [0, 0],
                'hl' : [0, 0]
            }

        self.ix = 0
        self.iy = 0
        self.sp = 0     # stack pointer
        self.pc = 0     # program counter
        self.im = 0     # interrupt mode 0, 1, 2

    ##
    # Run the CPU for 'cycles'.
    def run (self, cycles, mapper) :

        while True :
            self.step (mapper)
            cycles -= 1
            if cycles < 0 : break

    ##
    # Step the CPU.
    def step (self, mapper) :

        pc = self.pc
        op = mapper.read (self.pc)
        self.pc += 1

        if op == 0x00 :
            self._debug (pc, op, 'NOP')

        elif op == 0x06 :
            self._reg_write_hi ('bc', mapper.read (self.pc))
            self.pc += 1
            self._debug (pc, op, 'LD B, *')
        
        else :
            print 'Unhandled op code %02X' % op
            exit (1)

    ##
    # Write to the hi 8 bytes of a register.
    def _reg_write_hi (self, reg, value) :
        v = (self.regs[reg] & 0xFF) & value

    ##
    # Print debug information on the state of the CPU to standard out.
    def _debug (self, pc, op, desc) :

        print '-[%06d]------------------------------------------------' % pc
        print '%04X %s' % (op, desc)
        print 'AF %04X BC %04X DE %04X HL %04X IX %04X IY %04X' % \
              (self.af[0],
               self.bc[0],
               self.de[0],
               self.hl[0],
               self.ix,
               self.iy)
        print 'AF %04X BC %04X DE %04X HL %04X' % \
              (self.af[1],
               self.bc[1],
               self.de[1],
               self.hl[1])
        print 'SP %04X PC %06d IM %d' % \
              (self.sp,
               self.pc,
               self.im)
        print
