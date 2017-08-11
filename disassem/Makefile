CPPFLAGS=-g
LDFLAGS=-g
LDLIBS=

SRCS=$(wildcard *.cpp)
OBJS=$(subst .cpp,.o,$(SRCS))

TARGET=disassem

$(TARGET): $(OBJS)
	g++ $(LDFLAGS) -o $(TARGET) $(OBJS) $(LDLIBS)

.cpp.o:
	g++ $(CPPFLAGS) -c $<

clean:
	rm *.o $(TARGET)
