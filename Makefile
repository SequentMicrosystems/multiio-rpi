TARGET  = $(shell awk '/#define PROGRAM_NAME/ {print $$3}' src/data.h | tr -d '"')

DESTDIR ?= /usr/local

ifneq ($V,1)
Q = @
endif

CC	= gcc
CFLAGS	= $(DEBUG) -Wall -Wextra $(INCLUDE) -Winline -pipe
RELCFLAGS = -O3 -DNDEBUG
DBGCFLAGS = -g -DDEBUG
LDFLAGS	= -L$(DESTDIR)/lib
LIBS    = -lpthread -lrt -lm -lcrypt

SRC	= $(shell find src -type f -name '*.c' | sort)
#HDR	= $(shell find src -type f -name '*.h' | sort)
OBJ	= $(patsubst src/%.c,build/%.o,$(SRC))

.PHONY:	all clean debug install uninstall

all:	CFLAGS += $(RELCFLAGS)
all:	$(TARGET)

debug:	CFLAGS += $(DBGCFLAGS)
debug:	$(TARGET)

$(TARGET): $(OBJ)
	$Q echo "[Link] build/*.o -> $(TARGET)"
	$Q $(CC) -o $@ $(OBJ) $(LDFLAGS) $(LIBS)

build/%.o : src/%.c
	$Q mkdir -p $(@D)
	$Q echo "[Compile] $< -> $@"
	$Q $(CC) -c $(CFLAGS) $< -o $@

clean:
	$Q echo "[Clean]"
	$Q rm -f $(OBJ) $(TARGET) *~ core tags *.bak build/*

install: $(TARGET)
ifneq ($(shell id -u),0)
	$Q echo "Must be root! (sudo make install)"
	$Q exit 1
endif
	$Q echo "[Install] $(DESTDIR)/bin/$(TARGET)"
	$Q install -D -m 4755 -o root $(TARGET) $(DESTDIR)/bin

uninstall:
ifneq ($(shell id -u),0)
	$Q echo "Must be root! (sudo make uninstall)"
	$Q exit 1
endif
	$Q echo "[Uninstall]"
	$Q rm -f $(DESTDIR)/bin/$(TARGET)
