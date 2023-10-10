TARGET  = multiio
V_MAJOR = 1
V_MINOR = 0
V_PATCH = 0
VERSION = $(V_MAJOR).$(V_MINOR).$(V_PATCH)

DESTDIR ?= /usr
PREFIX  ?= /local

ifneq ($V,1)
Q ?= @
endif

CC	= gcc
VFLAG   = -DVERSION=$(VERSION)
CFLAGS	= $(DEBUG) -Wall -Wextra $(INCLUDE) -Winline -pipe
RELCFLAGS = -O3 -DNDEBUG -DVERSION=\"$(VERSION)\"
DBGCFLAGS = -g -DDEBUG -DVERSION=\"$(VERSION)-debug\"

LDFLAGS	= -L$(DESTDIR)$(PREFIX)/lib
LIBS    = -lpthread -lrt -lm -lcrypt

SRC	= $(shell find src -type f -name '*.c' | sort)

OBJ	= $(patsubst src/%.c,build/%.o,$(SRC))

all:	CFLAGS += $(RELCFLAGS)
all:	$(TARGET)

debug:	CFLAGS += $(DBGCFLAGS)
debug:	$(TARGET)

$(TARGET): $(OBJ)
	$Q echo [Link]
	$Q $(CC) -o $@ $(OBJ) $(LDFLAGS) $(LIBS)
	$Q echo [Done]

build/%.o : src/%.c
	$Q echo [Compile] $<
	$Q $(CC) -c $(CFLAGS) $< -o $@

.PHONY:	clean instlal uninstall

clean:
	$Q echo "[Clean]"
	$Q rm -f $(OBJ) $(TARGET) *~ core tags *.bak build/*

install: $(TARGET)
	$Q echo "[Install]"
	$Q cp $(TARGET)		$(DESTDIR)$(PREFIX)/bin
ifneq ($(WIRINGPI_SUID),0)
	$Q chown root:root	$(DESTDIR)$(PREFIX)/bin/$(TARGET)
	$Q chmod 4755		$(DESTDIR)$(PREFIX)/bin/$(TARGET)
	$Q #install -D -m 4755 -o root $(TARGET) $(DESTDIR)$(PREFIX)/bin
endif

uninstall:
	$Q echo "[Uninstall]"
	$Q rm -f $(DESTDIR)$(PREFIX)/bin/$(TARGET)
