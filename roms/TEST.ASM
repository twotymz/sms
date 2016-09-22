;----------------------------------------------------------------------------
; Palette test program
;
; Emulator warning: if the border/overscan color isn't black, it's because
; I use an undocumented instruction 'out (c), 0' to clear CRAM.
;
; I figured this was simpler than having a table of zero data to use with
; OTIR. I'm sure there are other good ways to clear the palette.
;----------------------------------------------------------------------------

TILE_VAL                =       $FF

                        .org    $0000
                        di
                        im      1
                        ld      sp, $DFF0
                        jp      main

                        .org    $0010
                        ld      a, l
                        out     ($BF), a
                        ld      a, h
                        out     ($BF), a
                        ret

                        .org    $0018
                        ld      a, l
                        out     ($BE), a
                        ld      a, h
                        out     ($BE), a
                        ret

                        .org    $0038
                        in      a, ($BF)
                        call    irq_routine
                        ei
                        reti

                        .org    $0066
                        retn

;----------------------------------------------------------------------------
irq_routine:
                        ex      af, af'
                        exx

                        ; Set CRAM entries 08-0F to 00h
                        in      a, ($BF)
                        ld      hl, $C008
                        rst     10h
                        ld      bc, $08BE
clear_palette:          .db     $ED, $71                ; out (c), 0
                        djnz    clear_palette

                        exx
                        ex      af, af'
                        ret

;----------------------------------------------------------------------------
main:
                        call    vdp_init
                        call    conio_init

                        ; Make block tiles
                        call    make_block_tiles

                        ; Draw blocks
                        call    draw_blocks

                        ; Enable screen and line ints
                        ld      hl, $81E2
                        rst     10h

                        ; Clear any pending interrupts
                        in      a, ($BF)
                        ei

main_loop:
                        ld      d, $00  ; Line count
                        ld      c, $00  ; Color
                        ld      e, $08  ; # rows

                        ; Wait for row
wait_in:                in      a, ($7E)
                        cp      d
                        jr      nz, wait_in

                        ; Set CRAM address
                        ld      hl, $C008
                        rst     10h

                        ; Update palette for this line
                        ld      hl, xlat
                        ld      l, c
                        ld      bc, $08BE
                        otir
                        ld      c, l

                        ; Wait for 24 more lines
                        ld      a, d
                        add     a, 24
                        ld      d, a

                        ; Next row
                        dec     e
                        jr      nz, wait_in

                        ; Next frame
                        jp      main_loop

;----------------------------------------------------------------------------

draw_blocks:
                        ld      hl, $7800
                        rst     10h
                        ld      c, 24
make_col:               push    bc
                        ld      bc, $0807
make_row:               ld      a, c
                        out     ($BE), a
                        ld      a, $01
                        out     ($BE), a
                        ld      a, c
                        out     ($BE), a
                        ld      a, $01
                        out     ($BE), a
                        ld      a, c
                        out     ($BE), a
                        ld      a, $01
                        out     ($BE), a
                        ld      a, c
                        out     ($BE), a
                        ld      a, $01
                        out     ($BE), a
                        dec     c
                        djnz    make_row
                        pop     bc
                        dec     c
                        ld      a, c
                        jr      nz, make_col
                        ret

;----------------------------------------------------------------------------
make_block_tiles:
                        ld      hl, $6000
                        rst     10h
                        ld      c, $00
make_blocks:            ld      b, $08
make_block:             xor     a
                        bit     0, c
                        jr      nz, p0
                        ld      a, TILE_VAL
p0:                     out     ($BE), a
                        xor     a
                        bit     1, c
                        jr      nz, p1
                        ld      a, TILE_VAL
p1:                     out     ($BE), a
                        xor     a
                        bit     2, c
                        jr      nz, p2
                        ld      a, TILE_VAL
p2:                     out     ($BE), a
                        xor     a
                        bit     3, c
                        jr      nz, p3
                        ld      a, TILE_VAL
p3:                     out     ($BE), a
                        djnz    make_block
                        inc     c
                        ld      a, c
                        cp      $08
                        jr      nz, make_blocks
                        ret

;----------------------------------------------------------------------------

                        .include "vdp.inc"
                        .include "conio.inc"

                        .org    $3E00
; Color remap table
xlat                    .db     $00,$01,$02,$03, $10,$11,$12,$13,
                        .db     $04,$05,$06,$07, $14,$15,$16,$17,
                        .db     $08,$09,$0A,$0B, $18,$19,$1a,$1B,
                        .db     $0C,$0D,$0E,$0F, $1c,$1d,$1e,$1F,

                        .db     $20,$21,$22,$23, $30,$31,$32,$33,
                        .db     $24,$25,$26,$27, $34,$35,$36,$37,
                        .db     $28,$29,$2A,$2B, $38,$39,$3A,$3B,
                        .db     $2C,$2D,$2E,$2F, $3C,$3D,$3E,$3F,

sdsc_program_name:      .db     "64-Color Palette Test Program",0
sdsc_release_notes:     .db     "Author: Charles MacDonald",0

                        ; SDSC data

                        .org    $7FE0
                        .db     "SDSC"
                        .db     $01, $00
                        .db     $30
                        .db     $07
                        .db     $01, $20
                        .db     $00, $00
                        .dw     sdsc_program_name
                        .dw     sdsc_release_notes

                        ; SEGA data

                        .org    $7FF0
                        .db     "TMR SEGA"
                        .dw     $FFFF
                        .db     $00, $00
                        .db     $00, $00
                        .db     $00
                        .db     $00

                        .end

