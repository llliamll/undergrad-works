//
// Created by yuanyi on 9/12/21.
//
#ifndef TEST_MATRIX_H
#define TEST_MATRIX_H

typedef struct{
    float x;
    float y;
    float z;
    float w;
} vec4;
typedef struct{
    vec4 x;
    vec4 y;
    vec4 z;
    vec4 w;
} mat4;

//vector functions
float dot_production(vec4 v1, vec4 v2);
float find_magnitude(vec4 v);
void  print_vec(vec4);
vec4  scalar_vector_multiplication(float s, vec4 v);
vec4  vector_vector_addition(vec4 v1,vec4 v2);
vec4  vector_vector_subtraction(vec4 v1,vec4 v2);
vec4  normalize(vec4 v);
vec4  cross_production(vec4 v1, vec4 v2);
//vector functions

//matrix functions
void print_mat(mat4);
mat4 scalar_matrix_multiplication(float s, mat4 m);
mat4 matrix_matrix_addition(mat4 m1, mat4 m2);
mat4 matrix_matrix_subtraction(mat4 m1, mat4 m2);
mat4 matrix_matrix_multiplication(mat4 m1, mat4 m2);
vec4 matrix_vector_multiplication(mat4 m, vec4 v);
mat4 transpose(mat4 m);
//matrix functions

#endif //TEST_MATRIX_H
