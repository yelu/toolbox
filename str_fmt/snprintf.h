#include <locale>
#include <codecvt>
#include <string>
#include <cstdio>

void print_char_array(const char* arr, int n)
{
    for (auto i = 0; i < n; ++i)
    {
        std::bitset<8> x(arr[i]);
        printf("%02x ", x.to_ulong());
    }
    printf("\n");
    printf("%s\n", arr);
}

// test snprintf always terminates buffer even when source str
// is longer than buffer size.
// From C11 standard, snprintf():
// The snprintf function is equivalent to fprintf, except that 
// the output is written into an array (speciﬁed by argument s) 
// rather than to a stream. If n is zero, nothing is written, 
// and s may be a null pointer. Otherwise, output characters beyond 
// the n-1st are discarded rather than being written to the array, 
// and a null character is written at the end of the characters 
// actually written into the array. If copying takes place between
// objects that overlap, the behavior is undefined.
void snprintf_null_terminate()
{
    const int BUFFER_SIZE = 5;
    char buffer[BUFFER_SIZE] = {'x', 'x', 'x', 'x', 'x'};
    print_char_array(buffer, BUFFER_SIZE);
    snprintf(buffer, BUFFER_SIZE, "%s", "hello");   
    print_char_array(buffer, BUFFER_SIZE);

    return;
}
