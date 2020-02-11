#include <locale>
#include <codecvt>
#include <string>

std::string utf32_to_utf8(std::wstring& input)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> converter;

    // throws std::range_error if the conversion fails
    std::string result = converter.to_bytes(input);
    return result;
}

std::wstring utf8_to_utf32(std::string& input)
{
	std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> converter;

	// throws std::range_error if the conversion fails
	std::wstring result = converter.from_bytes(input);
	return result;
}