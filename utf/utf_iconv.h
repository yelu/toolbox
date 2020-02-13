#include <iconv.h> // iconv_open, iconv, iconv_close
#include <errno.h>

inline std::wstring string2wstring(const T& str, String2WstringBuffer& buffer)
{
    if(str.empty())
    {
        return std::wstring();
    }

    // count of wchar_t needed <= count of utf8 bytes
    buffer.resize(str.size() + 1, boost::container::default_init_t{});

    iconv_t cd = iconv_open ("wchar_t", "UTF-8");
    if (cd == (iconv_t) -1)
    {
        return std::wstring();
    }
    char* inptr = (char*)str.c_str();
    size_t insize = str.size();
    char* outptr = (char *) buff.data();
    size_t outsize = buffer.size() * sizeof(wchar_t);
    size_t nconv = iconv (cd, &inptr, &insize, &outptr, &outsize);
    if (nconv == (size_t) -1)
    {
        ThrowConversionError("string2wstring", "iconv call");
    }

    /* Terminate the output string.  */
    if (outsize >= sizeof (wchar_t)){ *((wchar_t *) outptr) = L'\0';}
    else {buffer[buffer.size() - 1] = L'\0';}

    if (iconv_close (cd) != 0) {ThrowConversionError("string2wstring", "iconv_close call");}
                
    return std::wstring(buffer.data());
    return res;
}