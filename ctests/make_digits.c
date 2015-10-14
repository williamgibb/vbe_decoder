#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int digits[0x7a];

void makedigits (void)
{
	int i;

	for (i=0; i<26; i++)
	{
		digits['A'+i] = i;
		digits['a'+i] = i+26;
	}
	for (i=0; i<10; i++)
		digits['0'+i] = i+52;
	digits[0x2b] = 62;
	digits[0x2f] = 63;

}

int main( int argc, const char* argv[] )
{
    int i;
    char v;
	printf("JSON makedigits() representation!\n");
	makedigits();
    printf("{\n");
    for (i=0; i<=0x7a; i++)
    {
        v = digits[i];
        if (i == 0x7a)
        {
            printf("  \"%d\":%d\n", i, v);
        }
        else
        {
            printf("  \"%d\":%d,\n", i, v);
        }
        //printf("i:%d\td:%d\n", i, v);
    }
    printf("}\n");
}
