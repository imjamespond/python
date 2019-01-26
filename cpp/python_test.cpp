#include "python_test.hpp"

#include <boost/python/call.hpp>

void test_callback(callback_func func)
{
    (*func)("hello");
}
