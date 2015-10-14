<?php
/******************************************************************
Author   : RainX(Jing Xu) rainx1982 at gmail.com
Date     : Sat Oct 14 2006
Version  : $Id: jsdecoder.php,v 1.1.1.1 2007-10-02 13:32:35 rainx Exp $
Usage    :

 - ScriptDecoder ($inbuf , $cp = 0, $urlencoded = 0,
        $htmlencoded = 0, $verbose = 0, $smart = 1)
 - $inbuf(required) : The original encoded string that you
                      wanna to decode it
 - $cp              : CodePage (default : 0)
 - $urldec          : To unescape %xx style encoding on the
                      fly (default : 0)
 - $htmldec         : To unescape &amp; style encoding (default : 0)
 - $verbose         : Extra information (default : 0)
 - $smart           : Smart HTMLGuardian defeation (default : 1)
 - return           : The decoded string

If you find any bugs of this script , you could email me :
rainx1982[at]gmail.com , or visit my blog http://www.rainx.cn/

Example  :
    <?php
        $str =  file_get_contents("http://www.xxxx.com/");
        echo ScriptDecoder($str);
    ?>

Note that this php script is migrated from MrBrownstone's C version
(ScrDec v1.8) ,So if you wanna get more informations about the usage
and algorithm, please visit his site :

http://www.virtualconspiracy.com/scrdec.html

http://solor.googlecode.com/svn/trunk/website/cn/solor/dig/jsdecoder.php

*******************************************************************/

$rawData = array(
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
        0x09,0x60,0x50, 0x75,0x6B,0x2D, 0x38,0x4E,0x29, 0x55,0x3D,0x3F,
		0x51,0x67,0x2f
    ) ;

$pick_encoding = array(
1, 2, 0, 1, 2, 0, 2, 0, 0, 2, 0, 2, 1, 0, 2, 0,
1, 0, 2, 0, 1, 1, 2, 0, 0, 2, 1, 0, 2, 0, 0, 2,
1, 1, 0, 2, 0, 2, 0, 1, 0, 1, 1, 2, 0, 1, 0, 2,
1, 0, 2, 0, 1, 1, 2, 0, 0, 1, 1, 2, 0, 1, 0, 2
);

$transformed = array();
$transformed[0] = array();
$transformed[1] = array();
$transformed[2] = array();

$digits = array();

$urlencoded = 0;
$htmlencoded = 0;
$verbose = 0;
$smart = 1;

function unescape ($c)
{
    $escapes = array('#', '&', '!', '*', '$');
	$escaped = array("\r", "\n", "<", ">", "@");
	$i=0;

	if (ord($c) > 127)
		return $c;
	while ($escapes[$i])
	{
		if ($escapes[$i] == $c)
			return $escaped[$i];
		$i++;
	}
	return '?';
}

function maketrans ()
{
    global $transformed, $rawData;
	// int $i, $j;

	for ($i=0; $i<32; $i++)
		for ($j=0; $j<3; $j++)
			$transformed[$j][$i] = $i;

	for ($i=31; $i<=127; $i++)
		for ($j=0; $j<3; $j++)
			$transformed[$j][$rawData[($i-31)*3 + $j]] = ($i==31) ? 9 : $i;
}

function makedigits ()
{
	// int i;
    global $digits;

	for ($i=0; $i<26; $i++)
	{
		$digits[65+$i] = $i;
		$digits[97+$i] = $i+26;
	}
	for ($i=0; $i<10; $i++)
		$digits[48+$i] = $i+52;
	$digits[0x2b] = 62;
	$digits[0x2f] = 63;
}


function decodeBase64 (/* string */ $p)
{
    global $digits;
	$val = 0;

	$val +=  ($digits[ord($p[0])] << 2);
	$val +=  ($digits[ord($p[1])] >> 4);
	$val +=  ($digits[ord($p[1])] & 0xf) << 12;
	$val += (($digits[ord($p[2])] >> 2) << 8);
	$val += (($digits[ord($p[2])] & 0x3) << 22);
	$val +=  ($digits[ord($p[3])] << 16);
	$val += (($digits[ord($p[4])] << 2) << 24);
	$val += (($digits[ord($p[5])] >> 4) << 24);

	/* 543210 543210 543210 543210 543210 543210

	   765432
	          10
	                 ba98
	            fedc
	                     76
	                        543210
                                   fedcba 98----
       |- LSB -||-     -||-     -| |- MSB -|
	*/
	return $val;
}

/*
 Char. number range  |        UTF-8 octet sequence
      (hexadecimal)    |              (binary)
   --------------------+---------------------------------------------
   0000 0000-0000 007F | 0xxxxxxx
   0000 0080-0000 07FF | 110xxxxx 10xxxxxx
   0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
   0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
*/

function isLeadByte (/*unsigned int*/ $cp, /*unsigned char*/ $ucByte)
{
	/* Code page 932 - Japanese Shift-JIS       - 0x81-0x9f
	                                              0xe0-0xfc
                 936 - Simplified Chinese GBK   - 0xa1-0xfe
	             949 - Korean Wansung           - 0x81-0xfe
				 950 - Traditional Chinese Big5 - 0x81-0xfe
	            1361 - Korean Johab             - 0x84-0xd3
												  0xd9-0xde
												  0xe0-0xf9 */
	switch ($cp)
	{
		case 932:
			if (($ucByte > 0x80) && ($ucByte < 0xa0))	return 1;
			if (($ucByte > 0xdf) && ($ucByte < 0xfd))	return 1;
			else return 0;
		case 936:
			if (($ucByte > 0xa0) && ($ucByte < 0xff)) return 1;
			else return 0;
		case 949:
		case 950:
			if (($ucByte > 0x80) && ($ucByte < 0xff)) return 1;
			else return 0;
		case 1361:
			if (($ucByte > 0x83) && ($ucByte < 0xd4)) return 1;
			if (($ucByte > 0xd8) && ($ucByte < 0xdf)) return 1;
			if (($ucByte > 0xdf) && ($ucByte < 0xfa)) return 1;
			else return 0;
		default:
			return 0;
	}

}

$entities =  array(
	array("entity" => "excl","mappedchar"=>33),array("entity" => "quot","mappedchar"=>34),array("entity" => "num","mappedchar"=>35),array("entity" => "dollar","mappedchar"=>36),array("entity" => "percent","mappedchar"=>37),
	array("entity" => "amp","mappedchar"=>38),array("entity" => "apos","mappedchar"=>39),array("entity" => "lpar","mappedchar"=>40),array("entity" => "rpar","mappedchar"=>41),array("entity" => "ast","mappedchar"=>42),
	array("entity" => "plus","mappedchar"=>43),array("entity" => "comma","mappedchar"=>44),array("entity" => "period","mappedchar"=>46),array("entity" => "colon","mappedchar"=>58),array("entity" => "semi","mappedchar"=>59),
	array("entity" => "lt","mappedchar"=>60),array("entity" => "equals","mappedchar"=>61),array("entity" => "gt","mappedchar"=>62),array("entity" => "quest","mappedchar"=>63),array("entity" => "commat","mappedchar"=>64),
	array("entity" => "lsqb","mappedchar"=>91),array("entity" => "rsqb","mappedchar"=>93),array("entity" => "lowbar","mappedchar"=>95),array("entity" => "lcub","mappedchar"=>123),array("entity" => "verbar","mappedchar"=>124),
	array("entity" => "rcub","mappedchar"=>125),array("entity" => "tilde","mappedchar"=>126), array("entity" => NULL, "mappedchar"=>0)
    );


function decodeMnemonic ( /*unsigned char*/ $mnemonic)
{
    global $entities;
	/*int*/ $i=0;
	while ($entities[$i]["entity"] != NULL)
	{
		if (strcmp($entities[$i][$entity], $mnemonic)==0)
			return chr($entities[$i][$mappedchar]);
		$i++;
	}
	printf ("Warning: did not recognize HTML entity '%s'\n", $mnemonic);
	return '?';
}


function ScriptDecoder ($inbuf , $cp = 0, $urlencoded = 0, $htmlencoded = 0, $verbose = 0, $smart = 1  /*unsigned char *inname, unsigned char *outname, unsigned int cp*/)
{

    global $transformed, $pick_encoding, $digits;

    $LEN_OUTBUF= 1048576;
    $LEN_INBUF= 1048576;

    $STATE_INIT_COPY=		100;
    $STATE_COPY_INPUT=	101;
    $STATE_SKIP_ML=		102;
    $STATE_CHECKSUM=		103;
    $STATE_READLEN=		104;
    $STATE_DECODE=		105;
    $STATE_UNESCAPE=		106;
    $STATE_FLUSHING=		107;
    $STATE_DBCS=			108;
    $STATE_INIT_READLEN=	109;
    $STATE_URLENCODE_1=	110;
    $STATE_URLENCODE_2=	111;
    $STATE_WAIT_FOR_CLOSE= 112;
    $STATE_WAIT_FOR_OPEN= 113;
    $STATE_HTMLENCODE=	114;


	$marker = array("#", "@", "~", "^");
	$state = 0;
    $hd = 0;
	$utf8 = 0;
	$csum = 0;
    $len = 0;
    $inbuf_len = strlen($inbuf);

	maketrans();
	makedigits();

	$outbuf = '';
	$lenbuf = '';

	$state = $STATE_INIT_COPY;
	$i = 0;
	$j = 0;

	while ($state)
	{
        if ($i == $inbuf_len) break;


		if (($urlencoded==1) && ($inbuf[$i]=='%'))
		{
			$ustate = $state;				/* save state */
			$state = $STATE_URLENCODE_1;	/* enter decoding state */
			$i++;						/* flush char */
			continue;
		}

		/* 2 means we do urldecoding but wanted to avoid decoding an
			already decoded % for the second time */

		if ($urlencoded==2)
			$urlencoded=1;

		if (($htmlencoded==1) && ($inbuf[$i]=='&'))
		{
			$ustate = $state;
			$state = $STATE_HTMLENCODE;
			$hd = 0;
			$i++;
			continue;
		}

		/* 2 means we do htmldecoding but wanted to avoid decoding an
			already decoded & for the second time */

		if ($htmlencoded==2)
			$htmlencoded=1;

		switch ($state)
		{
			case $STATE_INIT_COPY:
				$ml = count ($marker);
				$m = 0;
				$state = $STATE_COPY_INPUT;
				break;

			/* after decoding a block, we have to wait for the current
			   script block to be closed (>) */

			case $STATE_WAIT_FOR_CLOSE:
				if ($inbuf[$i] == '>')
					$state = $STATE_WAIT_FOR_OPEN;
				$outbuf .= $inbuf[$i++];
                $j++;
				break;

			/* and a new block to be opened again (<) */
			case $STATE_WAIT_FOR_OPEN:
				if ($inbuf[$i] == '<')
					$state = $STATE_INIT_COPY;
				$outbuf .= $inbuf[$i++];
                $j++;
				break;

			case $STATE_COPY_INPUT:
				if ($inbuf[$i] == $marker[$m])
				{
					$i++;
					$m++;
				}
				else
				{
					if ($m)
					{
						$k = 0;
						$state = $STATE_FLUSHING;
					}
					else
                    {
						$outbuf .= $inbuf[$i++];
                        $j++;
                    }

				}
				if ($m == $ml)
					$state = $STATE_INIT_READLEN;
				break;

			case $STATE_FLUSHING:
				$outbuf .= $marker[$k++];
                $j++;
				$m--;
				if ($m==0)
					$state = $STATE_COPY_INPUT;
				break;

			case $STATE_SKIP_ML:
				$i++;
				if (!(--$ml))
					$state = $nextstate;
				break;


			case $STATE_INIT_READLEN:
				$ml = 6;
				$state = $STATE_READLEN;
				break;

			case $STATE_READLEN:
				//$lenbuf[6-$ml] = $inbuf[$i++]; // TODO
                if ($ml == 6) $lenbuf = '';
				$lenbuf .= $inbuf[$i++]; // TODO
				if (!(--$ml))
				{
					$len = decodeBase64 ($lenbuf);
					if ($verbose)
						printf ("Msg: Found encoded block containing %d characters.\n", $len);
					$m = 0;
					$ml = 2;
					$state = $STATE_SKIP_ML;
					$nextstate = $STATE_DECODE;
				}
				break;

			case $STATE_DECODE:
				if (!$len)
				{
					$ml = 6;
					$state = $STATE_CHECKSUM;
					break;
				}
				if ($inbuf[$i] == '@')
					$state = $STATE_UNESCAPE;
				else
				{
					if ((ord($inbuf[$i]) & 0x80) == 0)
					{
						$outbuf .= $c = chr($transformed[$pick_encoding[$m%64]][ord($inbuf[$i])]);
                        $j++;
						$csum += ord($c);
						$m++;
					}
					else
					{
						if (!$cp && (ord($inbuf[$i]) & 0xc0)== 0x80)
						{
							// utf-8 but not a start byte
							$len++;
							$utf8=1;
						}
						$outbuf .= $inbuf[$i];
                        $j++;
						if (($cp) && (isLeadByte ($cp, ord($inbuf[$i]))))
							$state = $STATE_DBCS;
					}
				}
				$i++;
				$len--;
				break;

			case $STATE_DBCS:
				$outbuf .= $inbuf[$i++];
				$state = $STATE_DECODE;
				break;

			case $STATE_UNESCAPE:
				$outbuf .= $c = unescape ($inbuf[$i++]);
                $j++;
				$csum += ord($c);
				$len--;
				$m++;
				$state = $STATE_DECODE;
				break;

			case $STATE_CHECKSUM:
				//$csbuf[6-$ml] = $inbuf[$i++];
                if ($ml == 6) $csbuf = '';
				$csbuf .= $inbuf[$i++];
				if (!(--$ml))
				{
					$csum -= decodeBase64 ($csbuf);
					if ($csum)
					{
                        # printf ("Error: Incorrect checksum! (%lu) (%lu)\n", $csum, decodeBase64($csbuf));
						if ($cp)
                            ;#printf ("Tip: Maybe try another codepage.\n");
						else
						{
                            /*
							if ($utf8>0)
                                ;#printf ("Tip: The file seems to contain special characters, try the -cp option.\n");
							else
                                ;#printf ("Tip: the file may be corrupted.\n");
                            */
						}
						$csum=0;
					}
					else
					{
						if ($verbose)
							printf ("Msg: Checksum OK\n");
					}
					$m = 0;
					$ml = 6;
					$state = $STATE_SKIP_ML;
					if ($smart)
	 					$nextstate = $STATE_WAIT_FOR_CLOSE;
					else
						$nextstate = $STATE_INIT_COPY;
				}
				break;

			/* urlencoded, the first character */
			case $STATE_URLENCODE_1:
				$c1 = ord($inbuf[$i++]) - 0x30;
				if ($c1 > 0x9) $c1-= 0x07;
				if ($c1 > 0x10) $c1-= 0x20;
				$state = $STATE_URLENCODE_2;
				break;

			/* urlencoded, second character */
			case $STATE_URLENCODE_2:
				$c2 = ord($inbuf[$i]) - 0x30;
				if ($c2 > 0x9) $c2-= 0x07;
				if ($c2 > 0x10) $c2-= 0x20;
				$inbuf[$i] = chr($c2 + ($c1<<4));	/* copy decoded char back on input */
				$urlencoded=2;				/* avoid looping in case this was an % */
				$state = $ustate;				/* restore old state */
				break;

			/* htmlencoded */
			case $STATE_HTMLENCODE:
				$c1 = $inbuf[$i];
				if ($c1 != ';')
				{
					$i++;
                    if ($hd == 0) $htmldec = '';
					$htmldec .= $c1;
                    $hd++;
					if ($hd>7)
					{
						printf ("Error: HTML decode encountered a too long mnemonic (%s...)\n", $htmldec);
						exit(10);
					}
				}
				else /* ';' = end of mnemonic */
				{
					$inbuf[$i] = $decodeMnemonic ($htmldec); /* skip the & */
					$htmlencoded = 2;		/* avoid looping in case of & */
					$state = $ustate;
				}
				break;
			default:
				printf ("Internal Error: Invalid state: %d\n", $state);
				break;
		}
	}

    return $outbuf;
}

?>