#ifndef TEST_H
#define TEST_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <Python.h>

    typedef void (*callback_func)(const char*);
    void test_callback(callback_func );

#ifdef __cplusplus
}
#endif

#endif