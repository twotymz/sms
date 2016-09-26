;----------------------------------------------------------------------------
; SMS POWER !
; by Omar Cornut / Zoop (c) in 1998
;----------------------------------------------------------------------------

.org  $0000

RAM = $C000
MAP_AREA = $3800
SPRITES_AREA = $3F00
STOP_SPRITES = 208
RES_X = 255

LEN_STRING = 12

P1_UP = 1
P1_DOWN = 2
P1_LEFT = 4
P1_RIGHT = 8
P1_B1 = 16
P1_B2 = 32

NUM_GFX = 11 + 22
GFX_SKY = 9
GFX_NULL = 10
GFX_HEART = 11
GFX_SMSPOWER = 12

VAR_string_space = RAM + 2
VAR_vscroll = RAM + 5

;--- INITIALIZATIONS --------------------------------------------------------
  di             ; Disable Interrupts
  im 1           ; Interrupt Mode 1
;----------------------------------------------------------------------------

;--- SETUP DEFAULT FRAMES VALUES --------------------------------------------
  ld a, 0
  ld ($FFFC), a
  ld ($FFFD), a
  ld ($FFFE), a
  ld ($FFFF), a

;--- CLEAR VIDEO RAM --------------------------------------------------------
  ld hl, $0000
  call Goto_VDP
  ld a, 0
  ld bc, MAP_AREA
ClearLoop:
  sub a
  out ($be), a
  dec bc
  ld a, b
  or c
  jr nz, ClearLoop
  ld bc, 32*28
ClearLoop_2:
  ld a, GFX_SKY
  out ($be), a
  ld a, $00
  out ($be), a
  dec bc
  ld a, b
  or c
  jr nz, ClearLoop_2

;--- MAP TILES IN VIDEO RAM -------------------------------------------------
  ld hl, MAP_AREA
  call Goto_VDP
  ld a, GFX_SMSPOWER
  ld b, 2
  ld c, 11
  ld d, 0
  call Draw_Image
  ld hl, MAP_AREA + 60
  call Goto_VDP
  call Draw_Image
;----------------------------------------------------------------------------

  ld hl, MAP_AREA + (32*11*2)
  call Goto_VDP
  ld bc, 32*(28-11)/2
Map_Loop:
  ld a, $01
  out ($be), a
  ld a, $00
  out ($be), a
  out ($be), a
  out ($be), a
  dec bc
  ld a, b
  or c
  jr nz, Map_Loop

;--- SET VDP REGISTERS TO THEIR DEFAULT VALUES ------------------------------
Set_VDP_Regs:
  ld hl, VDPRegsTable   ; Sets hl to point to VDP register values.
  ld b, $0f             ; Sets all 16 VDP registers. Starting at 0.
  ld c, $80             ; High byte is register number + 80h
VDPRegsLoop:
  ld a, (hl)
  inc hl
  out ($bf), a          ; Write register value to VDP
  ld a, c
  inc c
  out ($bf), a          ; Write register number + 80h to VDP
  dec b
  jr nz, VDPRegsLoop    ; Loop until b <> 0

;--- DISABLE SPRITES --------------------------------------------------------
  ld hl, $3F00
  call Goto_VDP
  ld a, 208
  out ($BE), a

;--- SET DEFAULT VARIABLES --------------------------------------------------
  ld hl, RAM
  ld (hl), 0
  ld hl, RAM + 1
  ld (hl), 0
  ld hl, VAR_string_space
  ld (hl), 8
  ld hl, RAM + 3
  ld (hl), 0
  ld hl, RAM + 4
  ld (hl), 0
  ld hl, VAR_vscroll
  ld (hl), 0

.include setpal

;--- WRITE GFX INTO TILE AREA -----------------------------------------------
  ld hl, 64
  call Goto_VDP
  ld hl, GFX_Table
  ld bc, 32 * NUM_GFX
Write_Font_Loop:
  ld a, (hl)
  out ($be), a
  inc hl
  dec bc
  ld a, b
  or c
  jr nz, Write_Font_Loop

;--- MAIN LOOP --------------------------------------------------------------
Loop:
  ld a, 5 * 8
  ld b, 20
  call Check_Inputs
  call Write_Zoop
  call Update_Tile
  call Update_Sound
  call Wait_VBL
  call Wait_VBL
  jp Loop
;----------------------------------------------------------------------------

Check_Inputs:
  push af
  push hl
  ld hl, VAR_string_space

  in a, ($dc)
  and P1_RIGHT
  jr z, Check_Inputs_1
  in a, ($dc)
  and P1_B1
  jr z, Check_Inputs_1

  in a, ($dc)
  and P1_LEFT
  jr z, Check_Inputs_2
  in a, ($dc)
  and P1_B2
  jr z, Check_Inputs_2

  pop hl
  pop af
  ret

Check_Inputs_1:
  ld a, (hl)
  push af
    sub 15
    jr z, Check_Inputs_3
  pop af
  inc a
  ld (hl), a
  pop hl
  pop af
  ret

Check_Inputs_2:
  ld a, (hl)
  push af
    sub 1
    jr z, Check_Inputs_3
  pop af
  dec a
  ld (hl), a
  pop hl
  pop af
  ret

Check_Inputs_3:
  pop af
  pop hl
  pop af
  ret

Update_Tile:
  ld hl, RAM + 4
  ld a, (hl)
  and $FF
  jr nz, Update_Tile_Dec

Update_Tile_Inc:
  ld hl, RAM + 3
  ld a, (hl)
  sub 6
  jr z, Update_Tile_Inc_2
  ld a, (hl)
  inc a
  ld (hl), a
  jp Update_Tile_2
Update_Tile_Inc_2:
  ld hl, RAM + 4
  ld a, 1
  ld (hl), a
  jp Update_Tile_2

Update_Tile_Dec:
  ld hl, RAM + 3
  ld a, (hl)
  and $FF
  jr z, Update_Tile_Dec_2
  ld a, (hl)
  dec a
  ld (hl), a
  jp Update_Tile_2
Update_Tile_Dec_2:
  ld hl, RAM + 4
  ld a, 0
  ld (hl), a
  jp Update_Tile_2

Update_Tile_2:
  ld hl, RAM
  ld a, (hl)
  inc a
  and $7
  ld (hl), a

  ld hl, $0000
  call Goto_VDP

  ld hl, Bar_GFX_Table
  ld b, 0
  ld c, a
  add hl, bc
  ld b, (hl)
  push bc
  ld bc, 8
  add hl, bc
  pop bc
  ld c, (hl)

  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1
  call Write_One_Tile_Line_1

  ld hl, Bar_GFX_Table
  ld b, 0
  ld c, a
  ld b, (hl)
  push bc
  ld bc, 8
  add hl, bc
  pop bc
  ld c, (hl)

  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  call Write_One_Tile_Line_2
  ret

Write_One_Tile_Line_1:
  push af
  ld a, b
  out ($be), a                
  ld a, c
  out ($be), a                
  ld a, 00000000b
  out ($be), a
  out ($be), a
  pop af
  rrc b
  ret

Write_One_Tile_Line_2:
  push af
  ld a, b
  out ($be), a                
  ld a, c
  out ($be), a                
  ld a, 11111111b 
  out ($be), a
  ld a, 00000000b
  out ($be), a
  pop af
  rlc b
  ret

Update_Sound:
  ld hl, RAM
  push af
  push bc
  ld a, 0
  ld b, (hl)
;  ld b, 2
  call Set_Frequency

  ld b, (hl)
  ld a, 3
  sub b
  ld b, a
;  rlc b

  ld a, 0
  call Set_Volume
  pop bc
  pop af
  ret

;--- SET A PALETTE ENTRY ----------------------------------------------------
;--- A: VALUE - B: INDEX ----------------------------------------------------
SetPal:
  push af
  ld a, b
  out ($BF), a
  ld a, $C0
  out ($BF), a
  pop af
  and $3F
  out ($BE), a
  ret

;--- SET VOLUME OF A CHANNEL ------------------------------------------------
;--- A: CHANNEL - B: VOLUME -------------------------------------------------
Set_Volume:
  push af       ; ......aa
  rlc a         ; .....aa.
  rlc a         ; ....aa..
  rlc a         ; ...aa...
  rlc a         ; ..aa....
  rlc a         ; .aa.....
  or 146        ; 1aa1....
  and 240       ; 1aa10000
  or b          ; 1aa1bbbb
  out ($7F), a  ; write value to PSG
  pop af
  ret

;--- SET FREQUENCY OF A CHANNEL ---------------------------------------------
;--- A: CHANNEL - B: FREQ (0->3) --------------------------------------------
Set_Frequency:
  push af
  rlc a         ; .....aa.
  rlc a         ; ....aa..
  rlc a         ; ...aa...
  rlc a         ; ..aa....
  rlc a         ; .aa.....
  or 128        ; 1aa.....
  and 224       ; 1aa00000
  out ($7F), a
  ld a, b
  rlc a         ; 00000bb0
  rlc a         ; 0000bb00
  or b          ; 0000bb**
  rlc a         ; 000bb**0
  rlc a         ; 00bb**00
  or b          ; 00bb****
;  and 48
;  and 112
  and 127
  out ($7F), a
  pop af
  ret

;--- SET A PALETTE ENTRY ----------------------------------------------------
;--- A: INDEX - B: RED - C: GREEN - D: BLUE ---------------------------------
SetPalRGB:
  push af
  out ($BF), a
  ld a, $C0
  out ($BF), a
  ld a, d             ; ......bb
  rlc a               ; .....bb.
  rlc a               ; ....bb..
  or c                ; ....bbgg
  rlc a               ; ...bbgg.
  rlc a               ; ..bbgg..
  or b                ; ..bbgg..
  and 255-128-64      ; 00bbgg..
  out ($BE), a
  pop af
  ret

; Wait for next VBlank
Wait_VBL:
  push af
Wait_VBL2:
  in a,($BF)
  and $80
  jp z, Wait_VBL2
  pop af
  ret

; Wait for five VBlank (slowdown)
Wait_5_VBL:
  call Wait_VBL
  call Wait_VBL
  call Wait_VBL
  call Wait_VBL
  call Wait_VBL
  ret

;--- FUNCTION: GOTO VDP ADDRESS ---------------------------------------------
;--- PARAMETERS: HL = address -----------------------------------------------
Goto_VDP:
  push af
   push hl
    push bc
     ld bc, $4000
     add hl, bc
    pop bc
   ld a, l
   out ($BF), a
   ld a, h
   out ($BF), a
   pop hl
  pop af
  ret
;----------------------------------------------------------------------------

; Write value "a" to VDP register "b"
VDP_Write:
  out ($bf), a
  push af
  ld a, b
  add a, $80
  out ($bf), a
  pop af
  ret

;--- WRITE "ZOOP IT UP !" STRING USING SPRITES ------------------------------
Write_Zoop:
  push af
  push bc

; --- Y Positions -----------------------------------------------------------
  ld hl, SPRITES_AREA
  call Goto_VDP
  ld hl, RAM + 3
  ld b, LEN_STRING
Zoop_Loop_1:

  add a, (hl)
  sub 3
  out ($be), a
  out ($be), a

  dec b
  jr nz, Zoop_Loop_1
  ld a, STOP_SPRITES
  out ($be), a

  pop bc ; b = start_x
  push bc

; --- X Positions & Tile Number ---------------------------------------------
  ld hl, SPRITES_AREA + 128
  call Goto_VDP
  ld a, b
  ld d, b
  ld b, LEN_STRING
  ld hl, String_Zoop
Zoop_Loop_2:
  out ($be), a  ; X (left)
    push af
    ld a, (hl)
    out ($be), a  ; Tile_N (left)
    pop af
    push af
      push bc
        ld b, d
        ld a, RES_X
        sub 8
        sub b
        out ($be), a  ; 256 - X (right)
        ld a, (hl)
        out ($be), a  ; Tile_N (right)
      pop bc
    pop af
  inc hl
  push hl
    ld hl, VAR_string_space
    add a, (hl)
    push af
      push bc
      ld hl, VAR_string_space
      ld a, 16
      ld b, (hl)
      sub b
      ld b, a
      ld a, d
      add a, b
      ld d, a
      pop bc
    pop af
  pop hl
  dec b
  jr nz, Zoop_Loop_2

; --- end of function -------------------------------------------------------
  pop bc
  pop af
  ret

;--- DRAW AN IMAGE INTO STANDARD TILE MAP -----------------------------------
;--- A: first tile_n - B: width - C: height - D: attribute ------------------
Draw_Image:
  push af
  push bc

Draw_Image_Loop_Y:
  push bc

Draw_Image_Loop_X:
    out ($be), a
    push af
      ld a, d
      out ($be), a
    pop af
    inc a
    dec b
    jr nz, Draw_Image_Loop_X

    ld bc, 64
    add hl, bc
    call Goto_VDP

  pop bc
  dec c
  jr nz, Draw_Image_Loop_Y

  pop bc
  pop af
  ret

.include data

.org $8000
.end
