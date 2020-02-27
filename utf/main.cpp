#include "utf.h"
#include <iostream>
#include <bitset>

int main()
{
    std::wstring input = L"Hello, World, 你好";
    std::string utf8 = utf32_to_utf8(input);

    // 48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 2c 20 e4 bd a0 e5 a5 bd
    for (size_t i = 0; i < utf8.size(); ++i)
    {
        std::bitset<8> x(utf8[i]);
        printf("%02x ", x.to_ulong());
    }
        //printf("%02x ", utf8[i]);
    std::cout << std::endl;
    std::cout << utf8 << std::endl;

	// u+00000048u+00000065u+0000006cu+0000006cu+0000006f u+00000057
	// u+0000006fu+00000072u+0000006cu+00000064
	std::wstring utf32 = utf8_to_utf32(utf8);
}