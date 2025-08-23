/*
+--------------------------------------------------------------------------+
| CHStone : a suite of benchmark programs for C-based High-Level Synthesis |
| ======================================================================== |
|                                                                          |
| * Collected and Modified : Y. Hara, H. Tomiyama, S. Honda,               |
|                            H. Takada and K. Ishii                        |
|                            Nagoya University, Japan                      |
|                                                                          |
| * Remark :                                                               |
|    1. This source code is modified to unify the formats of the benchmark |
|       programs in CHStone.                                               |
|    2. Test vectors are added for CHStone.                                |
|    3. If "main_result" is 0 at the end of the program, the program is    |
|       correctly executed.                                                |
|    4. Please follow the copyright of each benchmark program.             |
+--------------------------------------------------------------------------+
*/
/* NIST Secure Hash Algorithm */
/* heavily modified by Uwe Hollerbach uh@alumni.caltech edu */
/* from Peter C. Gutmann's implementation as found in */
/* Applied Cryptography by Bruce Schneier */

/* NIST's proposed modification to SHA of 7/11/94 may be */
/* activated by defining USE_MODIFIED_SHA */

#include "sha.h"

/* SHA f()-functions */
#define f1(x,y,z)	((x & y) | (~x & z))
#define f2(x,y,z)	(x ^ y ^ z)
#define f3(x,y,z)	((x & y) | (x & z) | (y & z))
#define f4(x,y,z)	(x ^ y ^ z)

/* SHA constants */
#define CONST1		0x5a827999L
#define CONST2		0x6ed9eba1L
#define CONST3		0x8f1bbcdcL
#define CONST4		0xca62c1d6L

/* 32-bit rotate */
#define ROT32(x,n)	((x << n) | (x >> (32 - n)))

#define FUNC(n,i)						\
    temp = ROT32(A,5) + f##n(B,C,D) + E + W[i] + CONST##n;	\
    E = D; D = C; C = ROT32(B,30); B = A; A = temp

unsigned int sha_info_count_lo, sha_info_count_hi;	/* 64-bit bit count */
unsigned int sha_info_data[16];
unsigned int sha_info_digest[DIGEST_SIZE];

unsigned char local_indata[NUM_BLOCKS][BLOCK_SIZE];

/* Local memory set function */
void local_memset(unsigned int *s, int c, int n, int e) {
    unsigned int uc = c;
    unsigned int *p = (unsigned int *)s;
    int m = n / 4;

    local_memset_label0:
    while (e-- > 0) {
        #pragma HLS LOOP_TRIPCOUNT max=63
        p++;
    }
    local_memset_label1:
    while (m-- > 0) {
        #pragma HLS LOOP_TRIPCOUNT max=16
        *p++ = uc;
    }
}

/* Local memory copy function */
void local_memcpy(unsigned int *s1, const unsigned char *s2, int n) {
    unsigned int *p1 = (unsigned int *)s1;
    unsigned char *p2 = (unsigned char *)s2;
    unsigned int tmp;
    int m = n / 4;

    local_memcpy_label3:
    while (m-- > 0) {
        #pragma HLS LOOP_TRIPCOUNT max=16
        tmp = 0;
        tmp |= 0xFF & *p2++;
        tmp |= (0xFF & *p2++) << 8;
        tmp |= (0xFF & *p2++) << 16;
        tmp |= (0xFF & *p2++) << 24;
        *p1 = tmp;
        p1++;
    }
}

/* Perform SHA transformation */
static void sha_transform() {
    int i;
    unsigned int temp, A, B, C, D, E, W[80];

    /* Prepare message schedule */
    sha_transform_label1:
    for (i = 0; i < 16; ++i) {
        #pragma HLS LOOP_TRIPCOUNT min=16 max=16 avg=16
        W[i] = sha_info_data[i];
    }

    sha_transform_label2:
    for (i = 16; i < 80; ++i) {
        #pragma HLS LOOP_TRIPCOUNT min=64 max=64 avg=64
        W[i] = W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16];
    }

    /* Initialize working variables */
    A = sha_info_digest[0];
    B = sha_info_digest[1];
    C = sha_info_digest[2];
    D = sha_info_digest[3];
    E = sha_info_digest[4];

    /* Main computation loop */
    sha_transform_label3: for (i = 0; i < 20; ++i) {
        FUNC(1, i);
    }
    sha_transform_label4: for (i = 20; i < 40; ++i) {
        FUNC(2, i);
    }
    sha_transform_label5: for (i = 40; i < 60; ++i) {
        FUNC(3, i);
    }
    sha_transform_label6: for (i = 60; i < 80; ++i) {
        FUNC(4, i);
    }

    /* Update digest values */
    sha_info_digest[0] += A;
    sha_info_digest[1] += B;
    sha_info_digest[2] += C;
    sha_info_digest[3] += D;
    sha_info_digest[4] += E;
}

/* Initialize SHA digest */
void sha_init() {
    sha_info_digest[0] = 0x67452301L;
    sha_info_digest[1] = 0xefcdab89L;
    sha_info_digest[2] = 0x98badcfeL;
    sha_info_digest[3] = 0x10325476L;
    sha_info_digest[4] = 0xc3d2e1f0L;
    sha_info_count_lo = 0L;
    sha_info_count_hi = 0L;
}

/* Update SHA digest with new data */
void sha_update(const unsigned char *buffer, int count) {
    if ((sha_info_count_lo + ((unsigned int)count << 3)) < sha_info_count_lo) {
        ++sha_info_count_hi;
    }
    sha_info_count_lo += (unsigned int)count << 3;
    sha_info_count_hi += (unsigned int)count >> 29;

    sha_update_label4:
    while (count >= SHA_BUFFER_SIZE) {
        #pragma HLS LOOP_TRIPCOUNT min=127 max=128
        local_memcpy(sha_info_data, buffer, SHA_BUFFER_SIZE);
        sha_transform();
        buffer += SHA_BUFFER_SIZE;
        count -= SHA_BUFFER_SIZE;
    }
    local_memcpy(sha_info_data, buffer, count);
}

/* Finalize SHA digest computation */
void sha_final() {
    int count;
    unsigned int lo_bit_count = sha_info_count_lo;
    unsigned int hi_bit_count = sha_info_count_hi;

    count = (int)((lo_bit_count >> 3) & 0x3f);
    sha_info_data[count++] = 0x80;

    if (count > 56) {
        local_memset(sha_info_data, 0, 64 - count, count);
        sha_transform();
        local_memset(sha_info_data, 0, 56, 0);
    } else {
        local_memset(sha_info_data, 0, 56 - count, count);
    }

    sha_info_data[14] = hi_bit_count;
    sha_info_data[15] = lo_bit_count;
    sha_transform();
}

/* top-level function */
/* Compute SHA digest from input stream */
void sha_stream(
    const unsigned char indata[NUM_BLOCKS][BLOCK_SIZE], 
    const int in_i[NUM_BLOCKS],
    unsigned int outdata[DIGEST_SIZE]
) {
    int i, j;
    const unsigned char *p;

    sha_stream_label0:for (i = 0; i < NUM_BLOCKS; i++) {
        sha_stream_label1:for (j = 0; j < BLOCK_SIZE; j++) {
            local_indata[i][j] = indata[i][j];
        }
    }

    sha_init();

    sha_stream_label2:
    for (j = 0; j < NUM_BLOCKS; j++) {
        #pragma HLS LOOP_TRIPCOUNT min=2 max=2 avg=2
        i = in_i[j];
        p = &local_indata[j][0];
        sha_update(p, i);
    }

    sha_final();

    sha_stream_label3:for (i = 0; i < DIGEST_SIZE; i++) {
        outdata[i] = sha_info_digest[i];
    }
}
