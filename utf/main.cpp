#include "utf.h"
#include <iostream>

int main()
{
    std::wstring input = L"Hello, World";
    std::string utf8 = utf32_to_utf8(input);
    std::cout << utf8 << std::endl;

	// u+00000048u+00000065u+0000006cu+0000006cu+0000006f u+00000057
	// u+0000006fu+00000072u+0000006cu+00000064
	std::wstring utf32 = utf8_to_utf32(utf8);
}