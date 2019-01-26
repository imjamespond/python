#ifndef PYTEST_H
#define PYTEST_H

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*callback_func)(detection *, int); 
detection *predict_image(callback_func, network *, image, int , int , float , float , int *, int , int *); 
void test(callback_func, network *, const char *, float , float , int *, int); 

#ifdef __cplusplus
}
#endif

#endif