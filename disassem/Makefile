CPPFLAGS=-g
LDFLAGS=-g
LDLIBS=

SRCS=$(wildcard *.cpp)
OBJS=$(subst .cpp,.o,$(SRCS))

TARGET=disassem

$(TARGET): $(OBJS)
	gcc $(LDFLAGS) -o $(TARGET) $(OBJS) $(LDLIBS)

.cpp.o:
	gcc $(CPPFLAGS) -c $<

clean:
	rm *.o $(TARGET)
