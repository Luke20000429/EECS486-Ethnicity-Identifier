#include<string.h>
// gcc -shared -fPIC prepostfix.c -o prepostfix.so
int prepostsqr(char* str1, char* str2) {
    // printf("st1= %s, str2 = %s\n", str1, str2);
    unsigned common_prefix_len = 0;
    unsigned common_postfix_len = 0;
    unsigned i = 0;
    unsigned lenstr1 = strlen(str1);
    unsigned lenstr2 = strlen(str2);
    unsigned minlen12 = (lenstr1 < lenstr2 ? lenstr1 : lenstr2);
    unsigned i1 = lenstr1;
    unsigned i2 = lenstr2;
    for (; common_prefix_len < minlen12 && str1[common_prefix_len] == str2[common_prefix_len]; ++common_prefix_len);
    for (; --minlen12 + 1 != 0 && str1[--i1] == str2[--i2]; ++common_postfix_len);
    return (4096 * (common_prefix_len * common_prefix_len + common_postfix_len * common_postfix_len) / (lenstr1 * lenstr1 + lenstr2 * lenstr2));
}