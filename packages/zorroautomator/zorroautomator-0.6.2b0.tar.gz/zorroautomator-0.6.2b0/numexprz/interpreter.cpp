/*********************************************************************
  Numexpr - Fast numerical array expression evaluator for NumPy.

      License: MIT
      Author:  See AUTHORS.txt

  See LICENSE.txt for details about copyright and rights to use.
**********************************************************************/

#include "module.hpp"
#include <numpy/npy_cpu.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#include <vector>

#include "numexpr_config.hpp"
#include "complex_functions.hpp"
#include "complexf_functions.hpp"
#include "interpreter.hpp"
#include "numexpr_object.hpp"


#ifndef SIZE_MAX
#define SIZE_MAX ((size_t)-1)
#endif

#define RETURN_TYPE char*

// AVAILABLE(Haystack, Haystack_Len, J, Needle_Len)
//     A macro that returns nonzero if there are at least Needle_Len
//     bytes left starting at Haystack[J].
//     Haystack is 'unsigned char *', Haystack_Len, J, and Needle_Len
//     are 'size_t'; Haystack_Len is an lvalue.  For NUL-terminated
//     searches, Haystack_Len can be modified each iteration to avoid
//     having to compute the end of Haystack up front.

#define AVAILABLE(Haystack, Haystack_Len, J, Needle_Len)   \
  ((Haystack_Len) >= (J) + (Needle_Len))

#include "str-two-way.hpp"

#ifdef DEBUG
#define DEBUG_TEST 1
#else
#define DEBUG_TEST 0
#endif



using namespace std;

// Global state
thread_data th_params;

/* This file and interp_body should really be generated from a description of
   the opcodes -- there's too much repetition here for manually editing */


/* bit of a misnomer; includes the return value. */
#define NUMEXPR_MAX_ARGS 4

static char op_signature_table[][NUMEXPR_MAX_ARGS] = {
#define Tb 'b'
#define Ti 'i'
#define Tl 'l'
#define Tf 'f'
#define Td 'd'
#define Tc 'c'
#define Ts 's'
#define Tn 'n'
#define Tx 'x'
#define T0 0
#define OPCODE(n, e, ex, rt, a1, a2, a3) {rt, a1, a2, a3},
#include "opcodes.hpp"
#undef OPCODE
#undef Tb
#undef Ti
#undef Tl
#undef Tf
#undef Td
#undef Tc
#undef Ts
#undef Tn
#undef Tx
#undef T0
};

/* returns the sig of the nth op, '\0' if no more ops -1 on failure */
static int
op_signature(int op, unsigned int n) {
    if (n >= NUMEXPR_MAX_ARGS) {
        return 0;
    }
    if (op < 0 || op > OP_END) {
        return -1;
    }
    return op_signature_table[op][n];
}



/*
   To add a function to the lookup table, add to FUNC_CODES (first
   group is 1-arg functions, second is 2-arg functions), also to
   functions_f or functions_ff as appropriate. Finally, use add_func
   down below to add to funccodes. Functions with more arguments
   aren't implemented at present, but should be easy; just copy the 1-
   or 2-arg case.

   Some functions (for example, sqrt) are repeated in this table that
   are opcodes, but there's no problem with that as the compiler
   selects opcodes over functions, and this makes it easier to compare
   opcode vs. function speeds.
*/


typedef float (*FuncFFPtr)(float);

//RAM do we need something similar for XX?
#ifdef _WIN32
FuncFFPtr functions_ff[] = {
#define FUNC_FF(fop, s, f, f_win32, ...) f_win32,
#include "functions.hpp"
#undef FUNC_FF
};
#else
FuncFFPtr functions_ff[] = {
#define FUNC_FF(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_FF
};
#endif

#ifdef USE_VML
/* Fake vsConj function just for casting purposes inside numexpr */
static void vsConj(MKL_INT n, const float* x1, float* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
        dest[j] = x1[j];
    };
};
#endif

#ifdef USE_VML
typedef void (*FuncFFPtr_vml)(MKL_INT, const float*, float*);
FuncFFPtr_vml functions_ff_vml[] = {
#define FUNC_FF(fop, s, f, f_win32, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_FF
};
#endif

typedef float (*FuncFFFPtr)(float, float);

#ifdef _WIN32
FuncFFFPtr functions_fff[] = {
#define FUNC_FFF(fop, s, f, f_win32, ...) f_win32,
#include "functions.hpp"
#undef FUNC_FFF
};
#else
FuncFFFPtr functions_fff[] = {
#define FUNC_FFF(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_FFF
};
#endif

#ifdef USE_VML
/* fmod not available in VML */
static void vsfmod(MKL_INT n, const float* x1, const float* x2, float* dest)
{
    MKL_INT j;
    for(j=0; j < n; j++) {
    dest[j] = fmod(x1[j], x2[j]);
    };
};

typedef void (*FuncFFFPtr_vml)(MKL_INT, const float*, const float*, float*);
FuncFFFPtr_vml functions_fff_vml[] = {
#define FUNC_FFF(fop, s, f, f_win32, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_FFF
};
#endif

typedef double (*FuncDDPtr)(double);

FuncDDPtr functions_dd[] = {
#define FUNC_DD(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_DD
};

#ifdef USE_VML
/* Fake vdConj function just for casting purposes inside numexpr */
static void vdConj(MKL_INT n, const double* x1, double* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
        dest[j] = x1[j];
    };
};
#endif

#ifdef USE_VML
typedef void (*FuncDDPtr_vml)(MKL_INT, const double*, double*);
FuncDDPtr_vml functions_dd_vml[] = {
#define FUNC_DD(fop, s, f, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_DD
};
#endif

typedef double (*FuncDDDPtr)(double, double);

FuncDDDPtr functions_ddd[] = {
#define FUNC_DDD(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_DDD
};

#ifdef USE_VML
/* fmod not available in VML */
static void vdfmod(MKL_INT n, const double* x1, const double* x2, double* dest)
{
    MKL_INT j;
    for(j=0; j < n; j++) {
    dest[j] = fmod(x1[j], x2[j]);
    };
};

typedef void (*FuncDDDPtr_vml)(MKL_INT, const double*, const double*, double*);
FuncDDDPtr_vml functions_ddd_vml[] = {
#define FUNC_DDD(fop, s, f, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_DDD
};
#endif



typedef void (*FuncCCPtr)(npy_cdouble*, npy_cdouble*);

FuncCCPtr functions_cc[] = {
#define FUNC_CC(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_CC
};

#ifdef USE_VML
/* complex expm1 not available in VML */
static void vzExpm1(MKL_INT n, const MKL_Complex16* x1, MKL_Complex16* dest)
{
    MKL_INT j;
    vzExp(n, x1, dest);
    for (j=0; j<n; j++) {
    dest[j].real -= 1.0;
    };
};

static void vzLog1p(MKL_INT n, const MKL_Complex16* x1, MKL_Complex16* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
    dest[j].real = x1[j].real + 1;
    dest[j].imag = x1[j].imag;
    };
    vzLn(n, dest, dest);
};

/* Use this instead of native vzAbs in VML as it seems to work badly */
static void vzAbs_(MKL_INT n, const MKL_Complex16* x1, MKL_Complex16* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
        dest[j].real = sqrt(x1[j].real*x1[j].real + x1[j].imag*x1[j].imag);
    dest[j].imag = 0;
    };
};

typedef void (*FuncCCPtr_vml)(MKL_INT, const MKL_Complex16[], MKL_Complex16[]);

FuncCCPtr_vml functions_cc_vml[] = {
#define FUNC_CC(fop, s, f, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_CC
};
#endif


typedef void (*FuncCCCPtr)(npy_cdouble*, npy_cdouble*, npy_cdouble*);

FuncCCCPtr functions_ccc[] = {
#define FUNC_CCC(fop, s, f) f,
#include "functions.hpp"
#undef FUNC_CCC
};

typedef void (*FuncXXPtr)(npy_cfloat*, npy_cfloat*);

FuncXXPtr functions_xx[] = {
#define FUNC_XX(fop, s, f, ...) f,
#include "functions.hpp"
#undef FUNC_XX
};

#ifdef USE_VML
/* complex expm1 not available in VML */
static void vcExpm1(MKL_INT n, const MKL_Complex8* x1, MKL_Complex8* dest)
{
    MKL_INT j;
    vcExp(n, x1, dest);
    for (j=0; j<n; j++) {
    dest[j].real -= 1.0;
    };
};

static void vcLog1p(MKL_INT n, const MKL_Complex8* x1, MKL_Complex8* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
    dest[j].real = x1[j].real + 1;
    dest[j].imag = x1[j].imag;
    };
    vcLn(n, dest, dest);
};

/* Use this instead of native vcAbs in VML as it seems to work badly */
static void vcAbs_(MKL_INT n, const MKL_Complex8* x1, MKL_Complex8* dest)
{
    MKL_INT j;
    for (j=0; j<n; j++) {
        dest[j].real = sqrt(x1[j].real*x1[j].real + x1[j].imag*x1[j].imag);
    dest[j].imag = 0;
    };
};

typedef void (*FuncXXPtr_vml)(MKL_INT, const MKL_Complex8[], MKL_Complex8[]);

FuncXXPtr_vml functions_xx_vml[] = {
#define FUNC_XX(fop, s, f, f_vml) f_vml,
#include "functions.hpp"
#undef FUNC_XX
};
#endif

typedef void (*FuncXXXPtr)(npy_cfloat*, npy_cfloat*, npy_cfloat*);

FuncXXXPtr functions_xxx[] = {
#define FUNC_XXX(fop, s, f) f,
#include "functions.hpp"
#undef FUNC_XXX
};

char
get_return_sig(PyObject* program)
{
    int sig;
    char last_opcode;
    Py_ssize_t end = PyBytes_Size(program);
    char *program_str = PyBytes_AS_STRING(program);

    do {
        end -= 4;
        if (end < 0) return 'X';
        last_opcode = program_str[end];
    }
    while (last_opcode == OP_NOOP);

    sig = op_signature(last_opcode, 0);
    // RAM: debug of signature codes
    //char buffer[256];
    //sprintf( buffer, "print(' interpreter::get_return_sig, sig = %d')", sig);
    //PyRun_SimpleString( buffer );
    // Wow it's annoying to print decimal representation of a string in Python...
    //sprintf( buffer, "print(' interpreter::get_return_sig, program = ' + ord(%s))", PyString_AsString( PyObject_Str(program)) );
    //PyRun_SimpleString( buffer );
    if (sig <= 0) {
        return 'X';
    } else {
        return (char)sig;
    }
}

static int
typecode_from_char(char c)
{
    switch (c) {
        case 'b': return NPY_BOOL;
        case 'i': return NPY_INT;
        case 'l': return NPY_LONGLONG;
        case 'f': return NPY_FLOAT;
        case 'd': return NPY_DOUBLE;
        case 'c': return NPY_CDOUBLE;
        case 'x': return NPY_CFLOAT;
        case 's': return NPY_STRING;
        default:
            PyErr_SetString(PyExc_TypeError, "signature value not in 'bilfdcxs'");
            return -1;
    }
}

static int
last_opcode(PyObject *program_object) {
    Py_ssize_t n;
    unsigned char *program;
    PyBytes_AsStringAndSize(program_object, (char **)&program, &n);
    return program[n-4];
}

static int
get_reduction_axis(PyObject* program) {
    Py_ssize_t end = PyBytes_Size(program);
    int axis = ((unsigned char *)PyBytes_AS_STRING(program))[end-1];
    if (axis != 255 && axis >= NPY_MAXDIMS)
        axis = NPY_MAXDIMS - axis;
    return axis;
}



int
check_program(NumExprObject *self)
{
    unsigned char *program;
    Py_ssize_t prog_len, n_buffers, n_inputs;
    int pc, arg, argloc, argno, sig;
    char *fullsig, *signature;

    if (PyBytes_AsStringAndSize(self->program, (char **)&program,
                                &prog_len) < 0) {
        PyErr_Format(PyExc_RuntimeError, "invalid program: can't read program");
        return -1;
    }
    if (prog_len % 4 != 0) {
        PyErr_Format(PyExc_RuntimeError, "invalid program: prog_len mod 4 != 0");
        return -1;
    }
    if (PyBytes_AsStringAndSize(self->fullsig, (char **)&fullsig,
                                &n_buffers) < 0) {
        PyErr_Format(PyExc_RuntimeError, "invalid program: can't read fullsig");
        return -1;
    }
    if (PyBytes_AsStringAndSize(self->signature, (char **)&signature,
                                &n_inputs) < 0) {
        PyErr_Format(PyExc_RuntimeError, "invalid program: can't read signature");
        return -1;
    }
    if (n_buffers > 255) {
        PyErr_Format(PyExc_RuntimeError, "invalid program: too many buffers");
        return -1;
    }
    for (pc = 0; pc < prog_len; pc += 4) {
        unsigned int op = program[pc];
        if (op == OP_NOOP) {
            continue;
        }
        if ((op >= OP_REDUCTION) && pc != prog_len-4) {
                PyErr_Format(PyExc_RuntimeError,
                    "invalid program: reduction operations must occur last");
                return -1;
        }
        for (argno = 0; ; argno++) {
            sig = op_signature(op, argno);
            if (sig == -1) {
                PyErr_Format(PyExc_RuntimeError, "invalid program: illegal opcode at %i (%d)", pc, op);
                return -1;
            }
            if (sig == 0) break;
            if (argno < 3) {
                argloc = pc+argno+1;
            }
            if (argno >= 3) {
                if (pc + 1 >= prog_len) {
                    PyErr_Format(PyExc_RuntimeError, "invalid program: double opcode (%c) at end (%i)", pc, sig);
                    return -1;
                }
                argloc = pc+argno+2;
            }
            arg = program[argloc];

            if (sig != 'n' && ((arg >= n_buffers) || (arg < 0))) {
                PyErr_Format(PyExc_RuntimeError, "invalid program: buffer out of range (%i) at %i", arg, argloc);
                return -1;
            }
            if (sig == 'n') {
                if (op == OP_FUNC_FFN) {
                    if (arg < 0 || arg >= FUNC_FF_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_FFFN) {
                    if (arg < 0 || arg >= FUNC_FFF_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_DDN) {
                    if (arg < 0 || arg >= FUNC_DD_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_DDDN) {
                    if (arg < 0 || arg >= FUNC_DDD_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_CCN) {
                    if (arg < 0 || arg >= FUNC_CC_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_CCCN) {
                    if (arg < 0 || arg >= FUNC_CCC_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_XXN) {
                    if (arg < 0 || arg >= FUNC_XX_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op == OP_FUNC_XXXN) {
                    if (arg < 0 || arg >= FUNC_XXX_LAST) {
                        PyErr_Format(PyExc_RuntimeError, "invalid program: funccode out of range (%i) at %i", arg, argloc);
                        return -1;
                    }
                } else if (op >= OP_REDUCTION) {
                    ;
                } else {
                    PyErr_Format(PyExc_RuntimeError, "invalid program: internal checker errror processing %i", argloc);
                    return -1;
                }
            /* The next is to avoid problems with the ('i','l') duality,
               specially in 64-bit platforms */
            } else if (((sig == 'l') && (fullsig[arg] == 'i')) ||
                       ((sig == 'i') && (fullsig[arg] == 'l'))) {
              ;
            } else if (sig != fullsig[arg]) {
                PyErr_Format(PyExc_RuntimeError,
                "invalid : opcode signature doesn't match buffer (%c vs %c) at %i", sig, fullsig[arg], argloc);
                return -1;
            }
        }
    }
    return 0;
}




struct index_data {
    int count;
    int size;
    int findex;
    npy_intp *shape;
    npy_intp *strides;
    int *index;
    char *buffer;
};

// BOUNDS_CHECK is used in interp_body.cpp
#define DO_BOUNDS_CHECK 1

#if DO_BOUNDS_CHECK
#define BOUNDS_CHECK(arg) if ((arg) >= params.r_end) { \
        *pc_error = pc;                                                 \
        return -2;                                                      \
    }
#else
#define BOUNDS_CHECK(arg)
#endif

int
stringcmp(const char *s1, const char *s2, npy_intp maxlen1, npy_intp maxlen2)
{
    npy_intp maxlen, nextpos;
    /* Point to this when the end of a string is found,
       to simulate infinte trailing NULL characters. */
    const char null = 0;

    // First check if some of the operands is the empty string and if so,		
    // just check that the first char of the other is the NULL one.		
    // Fixes #121		
    if (maxlen2 == 0) return *s1 != null;		
    if (maxlen1 == 0) return *s2 != null;

    maxlen = (maxlen1 > maxlen2) ? maxlen1 : maxlen2;
    for (nextpos = 1;  nextpos <= maxlen;  nextpos++) {
        if (*s1 < *s2)
            return -1;
        if (*s1 > *s2)
            return +1;
        s1 = (nextpos >= maxlen1) ? &null : s1+1;
        s2 = (nextpos >= maxlen2) ? &null : s2+1;
    }
    return 0;
}


/* contains(str1, str2) function for string columns.

   Based on Newlib/strstr.c.                        */

int
stringcontains(const char *haystack_start, const char *needle_start,  npy_intp max_haystack_len, npy_intp max_needle_len)
{
    // needle_len - Length of needle.
    // haystack_len - Known minimum length of haystack.
    size_t needle_len = min((size_t)max_needle_len, strlen(needle_start));
    size_t haystack_len = min((size_t)max_haystack_len, strlen(haystack_start));

    const char *haystack = haystack_start;
    const char *needle = needle_start;
    bool ok = true; /* needle is prefix of haystack. */

    if(haystack_len<needle_len)
        return 0;

    size_t si = 0;
    while (*haystack && *needle && si < needle_len)
    {
      ok &= *haystack++ == *needle++;
      si++;
    }
    if (ok)
    {
      return 1;
    }

    if (needle_len < LONG_NEEDLE_THRESHOLD)
    {
        char *res = two_way_short_needle ((const unsigned char *) haystack_start,
                                     haystack_len,
                                     (const unsigned char *) needle_start, needle_len) ;
        int ptrcomp = res != NULL;
        return ptrcomp;
    }

    char* res = two_way_long_needle ((const unsigned char *) haystack, haystack_len,
                              (const unsigned char *) needle, needle_len);
    int ptrcomp2 = res != NULL ? 1 : 0;
    return ptrcomp2;
}


/* Get space for VM temporary registers */
int get_temps_space(const vm_params& params, char **mem, size_t block_size)
{
    int r, k = 1 + params.n_inputs + params.n_constants;

    for (r = k; r < k + params.n_temps; r++) {
        mem[r] = (char *)malloc(block_size * params.memsizes[r]);
        if (mem[r] == NULL) {
            return -1;
        }
    }
    return 0;
}

/* Free space for VM temporary registers */
void free_temps_space(const vm_params& params, char **mem)
{
    int r, k = 1 + params.n_inputs + params.n_constants;

    for (r = k; r < k + params.n_temps; r++) {
        free(mem[r]);
    }
}

/* Serial/parallel task iterator version of the VM engine */
int vm_engine_iter_task(NpyIter *iter, npy_intp *memsteps,
                    const vm_params& params,
                    int *pc_error, char **errmsg)
{
    char **mem = params.mem;
    NpyIter_IterNextFunc *iternext;
    npy_intp block_size, *size_ptr;
    char **iter_dataptr;
    npy_intp *iter_strides;

    iternext = NpyIter_GetIterNext(iter, errmsg);
    if (iternext == NULL) {
        return -1;
    }

    size_ptr = NpyIter_GetInnerLoopSizePtr(iter);
    iter_dataptr = NpyIter_GetDataPtrArray(iter);
    iter_strides = NpyIter_GetInnerStrideArray(iter);

    /*
     * First do all the blocks with a compile-time fixed size.
     * This makes a big difference (30-50% on some tests).
     */
    block_size = *size_ptr;
    while (block_size == BLOCK_SIZE1) {
#define REDUCTION_INNER_LOOP
#define BLOCK_SIZE BLOCK_SIZE1
#include "interp_body.cpp"
#undef BLOCK_SIZE
#undef REDUCTION_INNER_LOOP
        iternext(iter);
        block_size = *size_ptr;
    }

    /* Then finish off the rest */
    if (block_size > 0) do {
#define REDUCTION_INNER_LOOP
#define BLOCK_SIZE block_size
#include "interp_body.cpp"
#undef BLOCK_SIZE
#undef REDUCTION_INNER_LOOP
    } while (iternext(iter));

    return 0;
}

static int
vm_engine_iter_outer_reduce_task(NpyIter *iter, npy_intp *memsteps,
                const vm_params& params, int *pc_error, char **errmsg)
{
    char **mem = params.mem;
    NpyIter_IterNextFunc *iternext;
    npy_intp block_size, *size_ptr;
    char **iter_dataptr;
    npy_intp *iter_strides;

    iternext = NpyIter_GetIterNext(iter, errmsg);
    if (iternext == NULL) {
        return -1;
    }

    size_ptr = NpyIter_GetInnerLoopSizePtr(iter);
    iter_dataptr = NpyIter_GetDataPtrArray(iter);
    iter_strides = NpyIter_GetInnerStrideArray(iter);

    /*
     * First do all the blocks with a compile-time fixed size.
     * This makes a big difference (30-50% on some tests).
     */
    block_size = *size_ptr;
    while (block_size == BLOCK_SIZE1) {
#define BLOCK_SIZE BLOCK_SIZE1
#define NO_OUTPUT_BUFFERING // Because it's a reduction
#include "interp_body.cpp"
#undef NO_OUTPUT_BUFFERING
#undef BLOCK_SIZE
        iternext(iter);
        block_size = *size_ptr;
    }

    /* Then finish off the rest */
    if (block_size > 0) do {
#define BLOCK_SIZE block_size
#define NO_OUTPUT_BUFFERING // Because it's a reduction
#include "interp_body.cpp"
#undef NO_OUTPUT_BUFFERING
#undef BLOCK_SIZE
    } while (iternext(iter));

    return 0;
}

/* Parallel iterator version of VM engine */
static int
vm_engine_iter_parallel(NpyIter *iter, const vm_params& params,
                        bool need_output_buffering, int *pc_error,
                        char **errmsg)
{
    int i;
    npy_intp numblocks, taskfactor;

    if (errmsg == NULL) {
        return -1;
    }

    /* Populate parameters for worker threads */
    NpyIter_GetIterIndexRange(iter, &th_params.start, &th_params.vlen);
    /*
     * Try to make it so each thread gets 16 tasks.  This is a compromise
     * between 1 task per thread and one block per task.
     */
    taskfactor = 16*BLOCK_SIZE1*gs.nthreads;
    numblocks = (th_params.vlen - th_params.start + taskfactor - 1) /
                            taskfactor;
    th_params.block_size = numblocks * BLOCK_SIZE1;

    th_params.params = params;
    th_params.need_output_buffering = need_output_buffering;
    th_params.ret_code = 0;
    th_params.pc_error = pc_error;
    th_params.errmsg = errmsg;
    th_params.iter[0] = iter;
    /* Make one copy for each additional thread */
    for (i = 1; i < gs.nthreads; ++i) {
        th_params.iter[i] = NpyIter_Copy(iter);
        if (th_params.iter[i] == NULL) {
            --i;
            for (; i > 0; --i) {
                NpyIter_Deallocate(th_params.iter[i]);
            }
            return -1;
        }
    }
    th_params.memsteps[0] = params.memsteps;
    /* Make one copy of memsteps for each additional thread */
    for (i = 1; i < gs.nthreads; ++i) {
        th_params.memsteps[i] = PyMem_New(npy_intp,
                    1 + params.n_inputs + params.n_constants + params.n_temps);
        if (th_params.memsteps[i] == NULL) {
            --i;
            for (; i > 0; --i) {
                PyMem_Del(th_params.memsteps[i]);
            }
            for (i = 0; i < gs.nthreads; ++i) {
                NpyIter_Deallocate(th_params.iter[i]);
            }
            return -1;
        }
        memcpy(th_params.memsteps[i], th_params.memsteps[0],
                sizeof(npy_intp) *
                (1 + params.n_inputs + params.n_constants + params.n_temps));
    }

    Py_BEGIN_ALLOW_THREADS;

    /* Synchronization point for all threads (wait for initialization) */
    pthread_mutex_lock(&gs.count_threads_mutex);
    if (gs.count_threads < gs.nthreads) {
        gs.count_threads++;
        pthread_cond_wait(&gs.count_threads_cv, &gs.count_threads_mutex);
    }
    else {
        pthread_cond_broadcast(&gs.count_threads_cv);
    }
    pthread_mutex_unlock(&gs.count_threads_mutex);

    /* Synchronization point for all threads (wait for finalization) */
    pthread_mutex_lock(&gs.count_threads_mutex);
    if (gs.count_threads > 0) {
        gs.count_threads--;
        pthread_cond_wait(&gs.count_threads_cv, &gs.count_threads_mutex);
    }
    else {
        pthread_cond_broadcast(&gs.count_threads_cv);
    }
    pthread_mutex_unlock(&gs.count_threads_mutex);

    Py_END_ALLOW_THREADS;

    /* Deallocate all the iterator and memsteps copies */
    for (i = 1; i < gs.nthreads; ++i) {
        NpyIter_Deallocate(th_params.iter[i]);
        PyMem_Del(th_params.memsteps[i]);
    }

    return th_params.ret_code;
}

static int
run_interpreter(NumExprObject *self, NpyIter *iter, NpyIter *reduce_iter,
                     bool reduction_outer_loop, bool need_output_buffering,
                     int *pc_error)
{
    int r;
    Py_ssize_t plen;
    vm_params params;
    char *errmsg = NULL;

    *pc_error = -1;
    if (PyBytes_AsStringAndSize(self->program, (char **)&(params.program),
                                &plen) < 0) {
        return -1;
    }

    params.prog_len = (int)plen;
    params.output = NULL;
    params.inputs = NULL;
    params.index_data = NULL;
    params.n_inputs = self->n_inputs;
    params.n_constants = self->n_constants;
    params.n_temps = self->n_temps;
    params.mem = self->mem;
    params.memsteps = self->memsteps;
    params.memsizes = self->memsizes;
    params.r_end = (int)PyBytes_Size(self->fullsig);
    params.out_buffer = NULL;

    if ((gs.nthreads == 1) || gs.force_serial) {
        // Can do it as one "task"
        if (reduce_iter == NULL) {
            // Allocate memory for output buffering if needed
            vector<char> out_buffer(need_output_buffering ?
                                (self->memsizes[0] * BLOCK_SIZE1) : 0);
            params.out_buffer = need_output_buffering ? &out_buffer[0] : NULL;
            // Reset the iterator to allocate its buffers
            if(NpyIter_Reset(iter, NULL) != NPY_SUCCEED) {
                return -1;
            }
            get_temps_space(params, params.mem, BLOCK_SIZE1);
            Py_BEGIN_ALLOW_THREADS;
            r = vm_engine_iter_task(iter, params.memsteps,
                                        params, pc_error, &errmsg);
            Py_END_ALLOW_THREADS;
            free_temps_space(params, params.mem);
        }
        else {
            if (reduction_outer_loop) {
                char **dataptr;
                NpyIter_IterNextFunc *iternext;

                dataptr = NpyIter_GetDataPtrArray(reduce_iter);
                iternext = NpyIter_GetIterNext(reduce_iter, NULL);
                if (iternext == NULL) {
                    return -1;
                }

                get_temps_space(params, params.mem, BLOCK_SIZE1);
                Py_BEGIN_ALLOW_THREADS;
                do {
                    r = NpyIter_ResetBasePointers(iter, dataptr, &errmsg);
                    if (r >= 0) {
                        r = vm_engine_iter_outer_reduce_task(iter,
                                                params.memsteps, params,
                                                pc_error, &errmsg);
                    }
                    if (r < 0) {
                        break;
                    }
                } while (iternext(reduce_iter));
                Py_END_ALLOW_THREADS;
                free_temps_space(params, params.mem);
            }
            else {
                char **dataptr;
                NpyIter_IterNextFunc *iternext;

                dataptr = NpyIter_GetDataPtrArray(iter);
                iternext = NpyIter_GetIterNext(iter, NULL);
                if (iternext == NULL) {
                    return -1;
                }

                get_temps_space(params, params.mem, BLOCK_SIZE1);
                Py_BEGIN_ALLOW_THREADS;
                do {
                    r = NpyIter_ResetBasePointers(reduce_iter, dataptr,
                                                                    &errmsg);
                    if (r >= 0) {
                        r = vm_engine_iter_task(reduce_iter, params.memsteps,
                                                params, pc_error, &errmsg);
                    }
                    if (r < 0) {
                        break;
                    }
                } while (iternext(iter));
                Py_END_ALLOW_THREADS;
                free_temps_space(params, params.mem);
            }
        }
    }
    else {
        if (reduce_iter == NULL) {
            r = vm_engine_iter_parallel(iter, params, need_output_buffering,
                        pc_error, &errmsg);
        }
        else {
            errmsg = "Parallel engine doesn't support reduction yet";
            r = -1;
        }
    }

    if (r < 0 && errmsg != NULL) {
        PyErr_SetString(PyExc_RuntimeError, errmsg);
    }

    return 0;
}

static int
run_interpreter_const(NumExprObject *self, char *output, int *pc_error)
{
    vm_params params;
    Py_ssize_t plen;
    char **mem;
    npy_intp *memsteps;

    *pc_error = -1;
    if (PyBytes_AsStringAndSize(self->program, (char **)&(params.program),
                                &plen) < 0) {
        return -1;
    }
    if (self->n_inputs != 0) {
        return -1;
    }
    params.prog_len = (int)plen;
    params.output = output;
    params.inputs = NULL;
    params.index_data = NULL;
    params.n_inputs = self->n_inputs;
    params.n_constants = self->n_constants;
    params.n_temps = self->n_temps;
    params.mem = self->mem;
    memsteps = self->memsteps;
    params.memsizes = self->memsizes;
    params.r_end = (int)PyBytes_Size(self->fullsig);

    mem = params.mem;
    get_temps_space(params, mem, 1);
#define SINGLE_ITEM_CONST_LOOP
#define BLOCK_SIZE 1
#define NO_OUTPUT_BUFFERING // Because it's constant
#include "interp_body.cpp"
#undef NO_OUTPUT_BUFFERING
#undef BLOCK_SIZE
#undef SINGLE_ITEM_CONST_LOOP
    free_temps_space(params, mem);

    return 0;
}

PyObject *
NumExpr_run(NumExprObject *self, PyObject *args, PyObject *kwds)
{
    PyArrayObject *operands[NPY_MAXARGS];
    PyArray_Descr *dtypes[NPY_MAXARGS], **dtypes_tmp;
    PyObject *tmp, *ret;
    npy_uint32 op_flags[NPY_MAXARGS];
    NPY_CASTING casting = NPY_SAFE_CASTING;
    NPY_ORDER order = NPY_KEEPORDER;
    unsigned int i, n_inputs;
    int r, pc_error = 0;
    int reduction_axis = -1;
    npy_intp reduction_size = 1;
    int ex_uses_vml = 0, is_reduction = 0;
    bool reduction_outer_loop = false, need_output_buffering = false;

    // To specify axes when doing a reduction
    int op_axes_values[NPY_MAXARGS][NPY_MAXDIMS],
         op_axes_reduction_values[NPY_MAXARGS];
    int *op_axes_ptrs[NPY_MAXDIMS];
    int oa_ndim = 0;
    int **op_axes = NULL;

    NpyIter *iter = NULL, *reduce_iter = NULL;

    // Check whether we need to restart threads
    if (!gs.init_threads_done || gs.pid != getpid()) {
        numexpr_set_nthreads(gs.nthreads);
    }

    // Don't force serial mode by default
    gs.force_serial = 0;

    // Check whether there's a reduction as the final step
    is_reduction = last_opcode(self->program) > OP_REDUCTION;

    n_inputs = (int)PyTuple_Size(args);
    if (PyBytes_Size(self->signature) != n_inputs) {
        return PyErr_Format(PyExc_ValueError,
                            "number of inputs doesn't match program");
    }
    else if (n_inputs+1 > NPY_MAXARGS) {
        return PyErr_Format(PyExc_ValueError,
                            "too many inputs");
    }

    memset(operands, 0, sizeof(operands));
    memset(dtypes, 0, sizeof(dtypes));

    if (kwds) {
        tmp = PyDict_GetItemString(kwds, "casting"); // borrowed ref
        if (tmp != NULL && !PyArray_CastingConverter(tmp, &casting)) {
            return NULL;
        }
        tmp = PyDict_GetItemString(kwds, "order"); // borrowed ref
        if (tmp != NULL && !PyArray_OrderConverter(tmp, &order)) {
            return NULL;
        }
        tmp = PyDict_GetItemString(kwds, "ex_uses_vml"); // borrowed ref
        if (tmp == NULL) {
            return PyErr_Format(PyExc_ValueError,
                                "ex_uses_vml parameter is required");
        }
        if (tmp == Py_True) {
            ex_uses_vml = 1;
        }
            // borrowed ref
        operands[0] = (PyArrayObject *)PyDict_GetItemString(kwds, "out");
        if (operands[0] != NULL) {
            if ((PyObject *)operands[0] == Py_None) {
                operands[0] = NULL;
            }
            else if (!PyArray_Check(operands[0])) {
                return PyErr_Format(PyExc_ValueError,
                                    "out keyword parameter is not an array");
            }
            else {
                Py_INCREF(operands[0]);
            }
        }
    }

    for (i = 0; i < n_inputs; i++) {
        PyObject *o = PyTuple_GET_ITEM(args, i); // borrowed ref
        PyObject *a;
        char c = PyBytes_AS_STRING(self->signature)[i];
        int typecode = typecode_from_char(c);
        // Convert it if it's not an array
        if (!PyArray_Check(o)) {
            if (typecode == -1) goto fail;
            a = PyArray_FROM_OTF(o, typecode, NPY_NOTSWAPPED);
        }
        else {
            Py_INCREF(o);
            a = o;
        }
        operands[i+1] = (PyArrayObject *)a;
        dtypes[i+1] = PyArray_DescrFromType(typecode);

        if (operands[0] != NULL) {
            // Check for the case where "out" is one of the inputs
            // TODO: Probably should deal with the general overlap case,
            //       but NumPy ufuncs don't do that yet either.
            if (PyArray_DATA(operands[0]) == PyArray_DATA(operands[i+1])) {
                need_output_buffering = true;
            }
        }

        if (operands[i+1] == NULL || dtypes[i+1] == NULL) {
            goto fail;
        }
        op_flags[i+1] = NPY_ITER_READONLY|
#ifdef USE_VML
                        (ex_uses_vml ? (NPY_ITER_CONTIG|NPY_ITER_ALIGNED) : 0)|
#endif
#ifndef USE_UNALIGNED_ACCESS
                        NPY_ITER_ALIGNED|
#endif
                        NPY_ITER_NBO
                        ;
    }

    if (is_reduction) {
        // A reduction can not result in a string,
        // so we don't need to worry about item sizes here.
        char retsig = get_return_sig(self->program);
        reduction_axis = get_reduction_axis(self->program);

        // Need to set up op_axes for the non-reduction part
        if (reduction_axis != 255) {
            // Get the number of broadcast dimensions
            for (i = 0; i < n_inputs; ++i) {
                int ndim = PyArray_NDIM(operands[i+1]);
                if (ndim > oa_ndim) {
                    oa_ndim = ndim;
                }
            }
            if (reduction_axis < 0 || reduction_axis >= oa_ndim) {
                PyErr_Format(PyExc_ValueError,
                        "reduction axis is out of bounds");
                goto fail;
            }
            // Fill in the op_axes
            op_axes_ptrs[0] = NULL;
            op_axes_reduction_values[0] = -1;
            for (i = 0; i < n_inputs; ++i) {
                int j = 0, idim, ndim = PyArray_NDIM(operands[i+1]);
                for (idim = 0; idim < oa_ndim-ndim; ++idim) {
                    if (idim != reduction_axis) {
                        op_axes_values[i+1][j++] = -1;
                    }
                    else {
                        op_axes_reduction_values[i+1] = -1;
                    }
                }
                for (idim = oa_ndim-ndim; idim < oa_ndim; ++idim) {
                    if (idim != reduction_axis) {
                        op_axes_values[i+1][j++] = idim-(oa_ndim-ndim);
                    }
                    else {
                        npy_intp size = PyArray_DIM(operands[i+1],
                                                    idim-(oa_ndim-ndim));
                        if (size > reduction_size) {
                            reduction_size = size;
                        }
                        op_axes_reduction_values[i+1] = idim-(oa_ndim-ndim);
                    }
                }
                op_axes_ptrs[i+1] = op_axes_values[i+1];
            }
            // op_axes has one less than the broadcast dimensions
            --oa_ndim;
            if (oa_ndim > 0) {
                op_axes = op_axes_ptrs;
            }
            else {
                reduction_size = 1;
            }
        }
        // A full reduction can be done without nested iteration
        if (oa_ndim == 0) {
            if (operands[0] == NULL) {
                npy_intp dim = 1;
                operands[0] = (PyArrayObject *)PyArray_SimpleNew(0, &dim,
                                            typecode_from_char(retsig));
                if (!operands[0])
                    goto fail;
            } else if (PyArray_SIZE(operands[0]) != 1) {
                PyErr_Format(PyExc_ValueError,
                        "out argument must have size 1 for a full reduction");
                goto fail;
            }
        }

        dtypes[0] = PyArray_DescrFromType(typecode_from_char(retsig));

        op_flags[0] = NPY_ITER_READWRITE|
                      NPY_ITER_ALLOCATE|
                      // Copy, because it can't buffer the reduction
                      NPY_ITER_UPDATEIFCOPY|
                      NPY_ITER_NBO|
#ifndef USE_UNALIGNED_ACCESS
                      NPY_ITER_ALIGNED|
#endif
                      (oa_ndim == 0 ? 0 : NPY_ITER_NO_BROADCAST);
    }
    else {
        char retsig = get_return_sig(self->program);
        if (retsig != 's') {
            dtypes[0] = PyArray_DescrFromType(typecode_from_char(retsig));
        } else {
            /* Since the *only* supported operation returning a string
             * is a copy, the size of returned strings
             * can be directly gotten from the first (and only)
             * input/constant/temporary. */
            if (n_inputs > 0) {  // input, like in 'a' where a -> 'foo'
                dtypes[0] = PyArray_DESCR(operands[1]);
                Py_INCREF(dtypes[0]);
            } else {  // constant, like in '"foo"'
                dtypes[0] = PyArray_DescrNewFromType(PyArray_STRING);
                dtypes[0]->elsize = (int)self->memsizes[1];
            }  // no string temporaries, so no third case
        }
        if (dtypes[0] == NULL) {
            goto fail;
        }
        op_flags[0] = NPY_ITER_WRITEONLY|
                      NPY_ITER_ALLOCATE|
                      NPY_ITER_CONTIG|
                      NPY_ITER_NBO|
#ifndef USE_UNALIGNED_ACCESS
                      NPY_ITER_ALIGNED|
#endif
                      NPY_ITER_NO_BROADCAST;
    }

    // Check for empty arrays in expression
    if (n_inputs > 0) {
        char retsig = get_return_sig(self->program);

        // Check length for all inputs
        int zeroi, zerolen = 0;
        for (i=0; i < n_inputs; i++) {
            if (PyArray_SIZE(operands[i+1]) == 0) {
                zerolen = 1;
                zeroi = i+1;
                break;
            }
        }

        if (zerolen != 0) {
            // Allocate the output
            int ndim = PyArray_NDIM(operands[zeroi]);
            npy_intp *dims = PyArray_DIMS(operands[zeroi]);
            operands[0] = (PyArrayObject *)PyArray_SimpleNew(ndim, dims,
                                              typecode_from_char(retsig));
            if (operands[0] == NULL) {
                goto fail;
            }

            ret = (PyObject *)operands[0];
            Py_INCREF(ret);
            goto cleanup_and_exit;
        }
    }


    /* A case with a single constant output */
    if (n_inputs == 0) {
        char retsig = get_return_sig(self->program);

        /* Allocate the output */
        if (operands[0] == NULL) {
            npy_intp dim = 1;
            operands[0] = (PyArrayObject *)PyArray_SimpleNew(0, &dim,
                                        typecode_from_char(retsig));
            if (operands[0] == NULL) {
                goto fail;
            }
        }
        else {
            PyArrayObject *a;
            if (PyArray_SIZE(operands[0]) != 1) {
                PyErr_SetString(PyExc_ValueError,
                        "output for a constant expression must have size 1");
                goto fail;
            }
            else if (!PyArray_ISWRITEABLE(operands[0])) {
                PyErr_SetString(PyExc_ValueError,
                        "output is not writeable");
                goto fail;
            }
            Py_INCREF(dtypes[0]);
            a = (PyArrayObject *)PyArray_FromArray(operands[0], dtypes[0],
                                        NPY_ALIGNED|NPY_UPDATEIFCOPY);
            if (a == NULL) {
                goto fail;
            }
            Py_DECREF(operands[0]);
            operands[0] = a;
        }

        r = run_interpreter_const(self, PyArray_BYTES(operands[0]), &pc_error);

        ret = (PyObject *)operands[0];
        Py_INCREF(ret);
        goto cleanup_and_exit;
    }


    /* Allocate the iterator or nested iterators */
    if (reduction_size == 1) {
        /* When there's no reduction, reduction_size is 1 as well */
        iter = NpyIter_AdvancedNew(n_inputs+1, operands,
                            NPY_ITER_BUFFERED|
                            NPY_ITER_REDUCE_OK|
                            NPY_ITER_RANGED|
                            NPY_ITER_DELAY_BUFALLOC|
                            NPY_ITER_EXTERNAL_LOOP,
                            order, casting,
                            op_flags, dtypes,
                            -1, NULL, NULL,
                            BLOCK_SIZE1);
        if (iter == NULL) {
            goto fail;
        }
    } else {
        npy_uint32 op_flags_outer[NPY_MAXDIMS];
        /* The outer loop is unbuffered */
        op_flags_outer[0] = NPY_ITER_READWRITE|
                            NPY_ITER_ALLOCATE|
                            NPY_ITER_NO_BROADCAST;
        for (i = 0; i < n_inputs; ++i) {
            op_flags_outer[i+1] = NPY_ITER_READONLY;
        }
        /* Arbitrary threshold for which is the inner loop...benchmark? */
        if (reduction_size < 64) {
            reduction_outer_loop = true;
            iter = NpyIter_AdvancedNew(n_inputs+1, operands,
                                NPY_ITER_BUFFERED|
                                NPY_ITER_RANGED|
                                NPY_ITER_DELAY_BUFALLOC|
                                NPY_ITER_EXTERNAL_LOOP,
                                order, casting,
                                op_flags, dtypes,
                                oa_ndim, op_axes, NULL,
                                BLOCK_SIZE1);
            if (iter == NULL) {
                goto fail;
            }

            /* If the output was allocated, get it for the second iterator */
            if (operands[0] == NULL) {
                operands[0] = NpyIter_GetOperandArray(iter)[0];
                Py_INCREF(operands[0]);
            }

            op_axes[0] = &op_axes_reduction_values[0];
            for (i = 0; i < n_inputs; ++i) {
                op_axes[i+1] = &op_axes_reduction_values[i+1];
            }
            op_flags_outer[0] &= ~NPY_ITER_NO_BROADCAST;
            reduce_iter = NpyIter_AdvancedNew(n_inputs+1, operands,
                                NPY_ITER_REDUCE_OK,
                                order, casting,
                                op_flags_outer, NULL,
                                1, op_axes, NULL,
                                0);
            if (reduce_iter == NULL) {
                goto fail;
            }
        }
        else {
            PyArray_Descr *dtypes_outer[NPY_MAXDIMS];

            /* If the output is being allocated, need to specify its dtype */
            dtypes_outer[0] = dtypes[0];
            for (i = 0; i < n_inputs; ++i) {
                dtypes_outer[i+1] = NULL;
            }
            iter = NpyIter_AdvancedNew(n_inputs+1, operands,
                                NPY_ITER_RANGED,
                                order, casting,
                                op_flags_outer, dtypes_outer,
                                oa_ndim, op_axes, NULL,
                                0);
            if (iter == NULL) {
                goto fail;
            }

            /* If the output was allocated, get it for the second iterator */
            if (operands[0] == NULL) {
                operands[0] = NpyIter_GetOperandArray(iter)[0];
                Py_INCREF(operands[0]);
            }

            op_axes[0] = &op_axes_reduction_values[0];
            for (i = 0; i < n_inputs; ++i) {
                op_axes[i+1] = &op_axes_reduction_values[i+1];
            }
            op_flags[0] &= ~NPY_ITER_NO_BROADCAST;
            reduce_iter = NpyIter_AdvancedNew(n_inputs+1, operands,
                                NPY_ITER_BUFFERED|
                                NPY_ITER_REDUCE_OK|
                                NPY_ITER_DELAY_BUFALLOC|
                                NPY_ITER_EXTERNAL_LOOP,
                                order, casting,
                                op_flags, dtypes,
                                1, op_axes, NULL,
                                BLOCK_SIZE1);
            if (reduce_iter == NULL) {
                goto fail;
            }
        }
    }

    /* Initialize the output to the reduction unit */
    if (is_reduction) {
        PyArrayObject *a = NpyIter_GetOperandArray(iter)[0];
        if (last_opcode(self->program) >= OP_SUM &&
            last_opcode(self->program) < OP_PROD) {
                PyObject *zero = PyLong_FromLong(0);
                PyArray_FillWithScalar(a, zero);
                Py_DECREF(zero);
        } else {
                PyObject *one = PyLong_FromLong(1);
                PyArray_FillWithScalar(a, one);
                Py_DECREF(one);
        }
    }

    /* Get the sizes of all the operands */
    dtypes_tmp = NpyIter_GetDescrArray(iter);
    for (i = 0; i < n_inputs+1; ++i) {
        self->memsizes[i] = dtypes_tmp[i]->elsize;
    }

    /* For small calculations, just use 1 thread */
    if (NpyIter_GetIterSize(iter) < 2*BLOCK_SIZE1) {
        gs.force_serial = 1;
    }

    /* Reductions do not support parallel execution yet */
    if (is_reduction) {
        gs.force_serial = 1;
    }

    r = run_interpreter(self, iter, reduce_iter,
                             reduction_outer_loop, need_output_buffering,
                             &pc_error);

    if (r < 0) {
        if (r == -1) {
            if (!PyErr_Occurred()) {
                PyErr_SetString(PyExc_RuntimeError,
                                "an error occurred while running the program");
            }
        } else if (r == -2) {
            PyErr_Format(PyExc_RuntimeError,
                         "bad argument at pc=%d", pc_error);
        } else if (r == -3) {
            PyErr_Format(PyExc_RuntimeError,
                         "bad opcode at pc=%d", pc_error);
        } else {
            PyErr_SetString(PyExc_RuntimeError,
                            "unknown error occurred while running the program");
        }
        goto fail;
    }

    /* Get the output from the iterator */
    ret = (PyObject *)NpyIter_GetOperandArray(iter)[0];
    Py_INCREF(ret);

    NpyIter_Deallocate(iter);
    if (reduce_iter != NULL) {
        NpyIter_Deallocate(reduce_iter);
    }
cleanup_and_exit:
    for (i = 0; i < n_inputs+1; i++) {
        Py_XDECREF(operands[i]);
        Py_XDECREF(dtypes[i]);
    }

    return ret;
fail:
    for (i = 0; i < n_inputs+1; i++) {
        Py_XDECREF(operands[i]);
        Py_XDECREF(dtypes[i]);
    }
    if (iter != NULL) {
        NpyIter_Deallocate(iter);
    }
    if (reduce_iter != NULL) {
        NpyIter_Deallocate(reduce_iter);
    }

    return NULL;
}

/*
Local Variables:
   c-basic-offset: 4
End:
*/
