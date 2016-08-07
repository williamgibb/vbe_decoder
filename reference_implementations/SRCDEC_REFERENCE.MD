# srcdec reference

Taken from http://web.archive.org/web/20050605234251/http://www.klaphek.nl/nr6/scrdec.html

# Breaking the Windows Script Encoder
by Mr Brownstone


The Windows Script Encoder (screnc.exe) is a Microsoft tool that can be used to encode your scripts (i.e. JScript, ASP pages, VBScript). Yes: encode, not encrypt. The use of this tool is to be able to prevent people from looking at, or modifying, your scripts. Microsoft recommends using the Script Encoder to obfuscate your ASP pages, so in case your server is compromised the hacker would be unable to find out how your ASP applications work.

You can download the Windows Script Encoder at http://msdn.microsoft.com/scripting/default.htm?/scripting/vbscript/download/vbsdown.htm

The documentation already says the following:

Note that this encoding only prevents casual viewing of your code; it will not prevent the determined hacker from seeing what you've done and how.

(By the way, because of this text, I did not deem it necessary to inform Microsoft of this article).

Also, an encoded script is protected against tampering and modifications:

After encoding, if you change even one character in the encoded text, the integrity of the entire script is lost and it can no longer be used.

So we can make the following observations:

1. We are a "determined hacker". *grins*
2. If it's about "preventing casual viewing", what's wrong with encoding mechanisms like a simple XOR or even uuencode, base64, and URL-encoding?
3. Anyone using this tool will be convinced that it's safe to hard-code all usernames, passwords, and "secret" algorithms into their ASP-pages. And any "determined hacker" will be able to get to them anyway.

Okay. So even Microsoft says this can be broken. Can't be difficult then. It wasn't. Writing this article took me at least twice the time I needed for breaking it. But I think this can be a very nice exercise for anyone who wants to learn more about analysing codes like this, with known plaintext, known cypertext, and unknown key and algorithm. (Actually, a COM object that can do the encoding is shipped with IE 5.0, so reverse engineering this will reveal the algorithm, but that's no fun, is it?)

## So, how does this work?

The Script Encoder works in a very simple way. It takes two parameters: the filename of the file containing the script, and the name of the output file, containing the encoded script.

What part of the file will be encoded depends on the filename extension, as well as on the presence of a so-called "encoding marker". This encoding marker allows you to exclude part of your script from being encoded. This can be very handy for JavaScripts, because the encoded scripts will only work on MSIE 5.0 or higher.... (of course this is not an issue for ASP and VB scripts that run on a web server!).

Say, you've got this HTML page with a script you want to hide from prying eyes:

```
<HTML>
<HEAD>
<TITLE>Page with secret information</TITLE>
<SCRIPT LANGUAGE="JScript">
<!--//
//**Start Encode**
   alert ("this code should be kept secret!!!!");
//-->
</SCRIPT>
</HEAD>
<BODY>
 This page contains secret information.
</BODY>
</HTML>
```

This is what it looks like after running Windows Script Encoder:

```
<HTML>
<HEAD>
<TITLE>Page with secret information</TITLE>
<SCRIPT LANGUAGE="JScript.Encode">
<!--//
//**Start Encode**#@~^QwAAAA==@#@&P~,l^+DDPvEY4kdP1W[n,/tK;V9P4
~V+aY,/nm.nD"Z"eE#p@#@&&JOO@*@#@&qhAAAA==^#~@&
lt;/SCRIPT>
</HEAD>
<BODY>
 This page contains secret information.
</BODY>
</HTML>
```


As you can see, the ```<script language="...">``` has been changed into "JScript.Encode". The Script Encoder uses the Scripting.Encoder COM-object to do the actual encoding. The decoding will be done by the script interpreter itself (so we cannot simply call a Scripting.Decoder, because that doesn't exist).

## Okay, let's play!

| Plaintext | Encoded |
| --------- |------- |
| Hoi | #@~^FQAAAA==@#@&CGb@#@&zz O@*@#@&WwIAAA==^#~@ |
| Hai | #@~^FQAAAA==@#@&CCb@#@&zz O@*@#@&TQIAAA==^#~@ |
| HaiHai<br>HaiHai | #@~^IgAAAA==@#@&CCbCmk@#@&CmrCmk@#@&JzRR@*@#@&mgUAAA==^#~@ |

Cute. As you can see, @#@& appears to be a newline (@# = CR, @& = LF), and the position of a character does (sometimes...) matter (the first time HaiHai becomes CCbCmk and the second time it's CmrCmk). Let's just encode a line with a lot of A's:

```
//**Start Encode**#@~^lgAAAA==@#@&b)zbzbbzbz)bzb)bzb))zbbz)bzbbz))bzbzb)b))zb)bz)bzb))zbb))zb)bz
)zb)zbzbbzbz)bzb)bzb))zbbz)bzbbz))bzbzb)b))zb)bz)bzb))zbb))zb)bz)zb)zb@#@&zJO @*@#@&vyIAAA==^#~@
```


## The algorithm


After staring at this for some time, I discovered that the bold part was repeating (actually, the entire string is repeating itself after 64 characters). Also, it seems to be that the character 'A' has three different representations: b, z, and ). If you encode a string of B's you'll see the same pattern, but with different characters.

This means the encoding will look something like this:

```
int pick_encoding[64] = {....};
int lookuptable[96][3] = {....};

char encode_char (char c, int pos)
{
   if (!specialchar (c))
      return lookuptable [c-32][pick_encoding[pos%64]];   
   else
      return escapedchar (c);
}
```

I assumed that only the ASCII codes 32 to 126 inclusive, and 9 (TAB) are encoded. The rest is being escaped in a similar fashion as CR and LF.

What's left is the stuff before and after the encoded string. I did not look into this (yet). It will probably contain a checksum and some information about the length of the encoded script.

The encoding tables

So now we'll have to find out those tables for the encoding. The pick_encoding table is very simple to discover by just looking at the pattern that was the result of encoding all those A's.

```
int pick_encoding[64] = 
{
   1, 2, 0, 1, 2, 0, 2, 0, 0, 2, 0, 2, 1, 0, 2, 0, 
   1, 0, 2, 0, 1, 1, 2, 0, 0, 2, 1, 0, 2, 0, 0, 2, 
   1, 1, 0, 2, 0, 2, 0, 1, 0, 1, 1, 2, 0, 1, 0, 2, 
   1, 0, 2, 0, 1, 1, 2, 0, 0, 1, 1, 2, 0, 1, 0, 2
};
```

The string of A's had a CR and LF in front of them, so after skipping the first two digits, you'll see that 0, 1, 2, 0, 2, 0, 0, 2 perfectly matches b, ), z, b, z, b, b, z , having b=0, )=1 and z=2.

The other table is a matrix that holds three different representations for each character. Which one will be used, depends on the pick_encoding table. To find out this matrix, just make a file that will cause every character to be encoded three times. Make sure the algorithm is 'reset' by padding the lines so each group will start on a 64-byte boundary.

```
   aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
!!!aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
"""aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
###aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
$$$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Etcetera. Note that there is only 59 bytes of padding a's because the CR and LF at the end of the line are counting too! (59 + 2 + 3 = 64).

After encoding this you can remove the encoded a's again, as well as the @#@& for the CR and LF. This is what remains:

```
d7i P~, "Ze JEr a:[ ^yf ]Yu ['L BvE `cv #b* eMC _Q3 ~SB OR  R c z&J !TZ Fq8  +y &f2 c*W *Xl 
v+ G{F %0R ,1O )l= iIp @!@!@! 'x{ @*@*@* g_Q @$@$@$ b)z A$~ Z/; f9G 23A sow M!V Cu_ q(& 9Bx |Fn SJd H\t 1Hg r6} nKh p}5 I]" ?j
U KP: ji` .#j   q (po 5eI }t\ $,] -w' TDY 7?% {m| =|# lCm 48( m^1 N[9 +n 0W6 oLT t44 krb L%N 3V0 Vs^ :hs xU      WGK w2a ;5$ D
.M /dk YOD E;! \-7 hAS 6aX XzH y".      `P uk- 8N) U=? 
```

So what is this? It's the encoded representation of the ASCII characters 9, and 32 through 126. Every character has got three different representations, so this sums up to 3*(127-32 + 1) = 288 characters.

You'll see that the < , > and @ characters are escaped too, resulting in the following table:

| Esc | Org |
| --- | --- |
| @# | \r |
| @& | \n |
| @! | < |
| @* | > |
| @$ | @ |

I've removed the @!, @* and @$ from the encoded text too and replaced them with question marks, so the table will stay nice. This is what you get as a hex dump:

```
unsigned char encoding[288] = {
        0x64,0x37,0x69, 0x50,0x7E,0x2C, 0x22,0x5A,0x65, 0x4A,0x45,0x72, 
        0x61,0x3A,0x5B, 0x5E,0x79,0x66, 0x5D,0x59,0x75, 0x5B,0x27,0x4C, 
        0x42,0x76,0x45, 0x60,0x63,0x76, 0x23,0x62,0x2A, 0x65,0x4D,0x43, 
        0x5F,0x51,0x33, 0x7E,0x53,0x42, 0x4F,0x52,0x20, 0x52,0x20,0x63, 
        0x7A,0x26,0x4A, 0x21,0x54,0x5A, 0x46,0x71,0x38, 0x20,0x2B,0x79, 
        0x26,0x66,0x32, 0x63,0x2A,0x57, 0x2A,0x58,0x6C, 0x76,0x7F,0x2B, 
        0x47,0x7B,0x46, 0x25,0x30,0x52, 0x2C,0x31,0x4F, 0x29,0x6C,0x3D, 
        0x69,0x49,0x70, 0x3F,0x3F,0x3F, 0x27,0x78,0x7B, 0x3F,0x3F,0x3F, 
        0x67,0x5F,0x51, 0x3F,0x3F,0x3F, 0x62,0x29,0x7A, 0x41,0x24,0x7E, 
        0x5A,0x2F,0x3B, 0x66,0x39,0x47, 0x32,0x33,0x41, 0x73,0x6F,0x77, 
        0x4D,0x21,0x56, 0x43,0x75,0x5F, 0x71,0x28,0x26, 0x39,0x42,0x78, 
        0x7C,0x46,0x6E, 0x53,0x4A,0x64, 0x48,0x5C,0x74, 0x31,0x48,0x67, 
        0x72,0x36,0x7D, 0x6E,0x4B,0x68, 0x70,0x7D,0x35, 0x49,0x5D,0x22, 
        0x3F,0x6A,0x55, 0x4B,0x50,0x3A, 0x6A,0x69,0x60, 0x2E,0x23,0x6A, 
        0x7F,0x09,0x71, 0x28,0x70,0x6F, 0x35,0x65,0x49, 0x7D,0x74,0x5C, 
        0x24,0x2C,0x5D, 0x2D,0x77,0x27, 0x54,0x44,0x59, 0x37,0x3F,0x25, 
        0x7B,0x6D,0x7C, 0x3D,0x7C,0x23, 0x6C,0x43,0x6D, 0x34,0x38,0x28, 
        0x6D,0x5E,0x31, 0x4E,0x5B,0x39, 0x2B,0x6E,0x7F, 0x30,0x57,0x36, 
        0x6F,0x4C,0x54, 0x74,0x34,0x34, 0x6B,0x72,0x62, 0x4C,0x25,0x4E, 
        0x33,0x56,0x30, 0x56,0x73,0x5E, 0x3A,0x68,0x73, 0x78,0x55,0x09, 
        0x57,0x47,0x4B, 0x77,0x32,0x61, 0x3B,0x35,0x24, 0x44,0x2E,0x4D, 
        0x2F,0x64,0x6B, 0x59,0x4F,0x44, 0x45,0x3B,0x21, 0x5C,0x2D,0x37, 
        0x68,0x41,0x53, 0x36,0x61,0x58, 0x58,0x7A,0x48, 0x79,0x22,0x2E, 
        0x09,0x60,0x50, 0x75,0x6B,0x2D, 0x38,0x4E,0x29, 0x55,0x3D,0x3F 
} ;
```

So, encoding character c at position i goes as follows:

1. look up which representation to use (the first, second or third): pick_encoding[i mod 64]
2. find the representations in the huge table: encoding[c * 3]
3. encoded character = encoding[c*3 + pick_encoding[i%64]];

Because the table starts at 9 and then goes to 32, you'll have to do some corrections. But we'll get to that later, as we are not really interested in encoding after all. We want to be able to do some decoding!

## The decoding tables

The pick_encoding table will stay the same. This is because each character (except for the escaped ones, of course) will be in the same place as the original. Then, we could just look up the encoded character in the table. For instance, an 'A' in encoded text (hex 0x41), occurs on these places in the 'encoding' table:

1. row 9, group 4, representation 1 = 'F'
2. row 10, group 3, representation 3 = 'I'
3. row 23, group 1, representation 2 = '{'

So an 'A' in the encoded text is an F, I or {, depending on it's position. Where there is a 0 in the pick_encoding table, it's an F, for 1 it's an I, and for 2 it's a {.
You don't want to go looking through the encoding table each time, trying to find those numbers. By transforming the encoding table into another table, you can just go to position 0x41 (actually, 0x41 - 31 to correct it skipping everything below space except for TAB), and pick the correct representation.

```
unsigned char transformed[3][126];

void maketrans (void)
{
    int i, j;
    for (i=31; i<=126; i++)
        for (j=0; j<3; j++)
            transformed[j][encoding[(i-31)*3 + j]] = (i==31) ? 9 : i;
}
```

With this matrix, it's very simple to look up the original character by simply looking it up in our table. Assume i is the position of the character and c is the character again. Then:

```
decoded = transformed[pick_encoding[i%64]][c];
```

## The encoding of the length-field

So what's left is to find out how many characters there are to decode. If we just keep decoding stuff, we will decode part of the HTML that's behind the encoded script. This can be avoided by stopping when a '<' is encountered ('<' will never appear in an encoded stream), but even in the case we are looking at a 'pure' script file (*.js or *.vbs), there is some checksum stuff behind the actual data, which we should not decode.

I created a number of files of different size. By giving them a *.js extension the entire file is encoded without the Script Encoder looking for a start marker. The results are below (only the first 12 bytes are displayed).

```
Length	First 12 bytes	ASCII
1	23 40 7E 5E 41 51 41 41-41 41 3D 3D	#@^EQAAAA==
2	23 40 7E 5E 41 67 41 41-41 41 3D 3D	#@^EgAAAA==
3	23 40 7E 5E 41 77 41 41-41 41 3D 3D	#@^EwAAAA==
4	23 40 7E 5E 42 41 41 41-41 41 3D 3D	#@^FAAAAA==
5	23 40 7E 5E 42 51 41 41-41 41 3D 3D	#@^FQAAAA==
6	23 40 7E 5E 42 67 41 41-41 41 3D 3D	#@^FgAAAA==
7	23 40 7E 5E 42 77 41 41-41 41 3D 3D	#@^FwAAAA==
8	23 40 7E 5E 43 41 41 41-41 41 3D 3D	#@^GAAAAA==
9	23 40 7E 5E 43 51 41 41-41 41 3D 3D	#@^GQAAAA==
32	23 40 7E 5E 49 41 41 41-41 41 3D 3D	#@^IAAAAA==
48	23 40 7E 5E 4D 41 41 41-41 41 3D 3D	#@^MAAAAA==
80	23 40 7E 5E 55 41 41 41-41 41 3D 3D	#@^UAAAAA==
96	23 40 7E 5E 59 41 41 41-41 41 3D 3D	#@^YAAAAA==
103	23 40 7E 5E 5A 77 41 41-41 41 3D 3D	#@^ZwAAAA==
104	23 40 7E 5E 61 41 41 41-41 41 3D 3D	#@^aAAAAA==
111	23 40 7E 5E 62 77 41 41-41 41 3D 3D	#@^bwAAAA==
116	23 40 7E 5E 64 41 41 41-41 41 3D 3D	#@^dAAAAA==
166	23 40 7E 5E 70 67 41 41-41 41 3D 3D	#@^pgAAAA==
216	23 40 7E 5E 32 41 41 41-41 41 3D 3D	#@^2AAAAA==
265	23 40 7E 5E 43 51 45 41-41 41 3D 3D	#@^CQEAAA==
451	23 40 7E 5E 77 77 45 41-41 41 3D 3D	#@^wwEAAA==
```

The length seems to be encoded in the 5th to 10th byte, and 41 appears to be representing zero. The first byte of the length seems to be increasing with one when the length increases with 4. Also, the second byte alternates between 41, 51, 67, and 77.

If you look at length 166, this value is 0x70, where it should be 0x41 + (166/4) = 0x6a. So something goes wrong, and it can be narrowed down to length 104, where it suddenly jumps from 0x5a to 0x61. This puzzled me for a long time, until I realised that 0x5a = 'Z' and 0x61 = 'a'. And yes, the length turns out to be Base64 encoded indeed :)

## The checksum

At the end of the encoded data is apparently some kind of checksum. I did not look into this any further.

## The decoder program

The further working of the decoder program, which can be downloaded from the scrdec home page, is left as an exercise to the reader. It's implemented as a "Turing-like" state machine. The decoder will treat .js and .vbs files as fully encoded, while .htm(l) and .asp files are seen as files that contain script amongst other things - like HTML code.

The decoder simply takes two arguments: input filename (encoded), and output filename (decoded).

There is one thing lacking in the decoder: the value of the <SCRIPT LANGUAGE="..."> attribute, is not changed back into the original form. You'd better use a tool like sed for that.

## Conclusion

It's not just sad that Microsoft made a tool like this. They've probably asked Bill Gates' little nephew to write this code. The really bad part is that Microsoft actually recommends people to use this piece of crap, and because of that, people will rely on it, even though the documentation hints that it's unsafe. (Nobody reads the docs anyway...)

Security by obscurity is a bad, bad idea. Instead of encouraging that approach, Microsoft should educate programmers to find other ways to store their passwords and sensitive data, and tell them that an algorithm or any other piece of code that needs to be 'hidden', is just bad design.