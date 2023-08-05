#pragma once

struct FormatNode {
	unsigned type;
	int count;
	int size;
};

struct FormatInfo {
	bool valid;
	int nodes;
	int size;
};

struct FormatIterator {
	const char * ptr;
	FormatNode node;

	FormatIterator(const char * str);

	FormatInfo info();
	FormatNode * next();
};

extern FormatNode * InvalidFormat;
