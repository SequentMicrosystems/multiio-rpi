#ifndef CLI_H
#define CLI_H

typedef struct {
	const char *name;
	const int namePos;
	int (*pFunc)(int, char*[]);
	const char *help;
	const char *usage;
	const char *example;
} CliCmdType;

extern const CliCmdType *gCmdArray[];

#endif /* CLI_H */

// vi:fdm=marker
