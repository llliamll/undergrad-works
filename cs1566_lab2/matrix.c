//
// Created by yuanyi on 9/12/21.
//
#include "matrix.h"
#include <stdio.h>
#include "math.h"

//vector functions
void print_vec(vec4 v)
{
    printf("[%7.4f ",v.x);
    printf("%7.4f ",v.y);
    printf("%7.4f ",v.z);
    printf("%7.4f]\n",v.w);
}

vec4 scalar_vector_multiplication(float s, vec4 v)
{
    v.x = s * v.x;
    v.y = s * v.y;
    v.z = s * v.z;
    v.w = s * v.w;

    return v;
}

vec4 vector_vector_addition(vec4 v1,vec4 v2)
{
    vec4 sum;
    sum.x = v1.x+v2.x;
    sum.y = v1.y+v2.y;
    sum.z = v1.z+v2.z;
    sum.w = v1.w+v2.w;

    return sum;
}

vec4 vector_vector_subtraction(vec4 v1,vec4 v2)
{
    vec4 difference;
    difference.x = v1.x-v2.x;
    difference.y = v1.y-v2.y;
    difference.z = v1.z-v2.z;
    difference.w = v1.w-v2.w;

    return difference;
}

float find_magnitude(vec4 v)
{
    float magnitude;
    float x_value;
    float y_value;
    float z_value;
    float w_value;

    x_value   = v.x*v.x;
    y_value   = v.y*v.y;
    z_value   = v.z*v.z;
    w_value   = v.w*v.w;
    magnitude = sqrtf((x_value+y_value+z_value+w_value));

    return magnitude;
}

vec4 normalize(vec4 v)
{
    vec4 normalized;
    float magnitude;
    magnitude  = find_magnitude(v);
    normalized = scalar_vector_multiplication((1/magnitude),v);

    return normalized;
}

float dot_production(vec4 v1, vec4 v2)
{
    float x;
    float y;
    float z;
    float w;
    float sum;

    x = (v1.x * v2.x);
    y = (v1.y * v2.y);
    z = (v1.z * v2.z);
    w = (v1.w * v2.w);
    sum = x+y+z+w;

    return sum;
}

vec4 cross_production(vec4 v1, vec4 v2)
{
    vec4 result;
    result.x = (v1.y*v2.z) - (v1.z*v2.y);
    result.y = (v1.z*v2.x) - (v1.x*v2.z);
    result.z = (v1.x*v2.y) - (v1.y*v2.x);
    result.w = 0;

    return result;
}
//end vector functions
//matrix functions
void print_mat(mat4 m)
{
    printf("%10.4f %10.4f %10.4f %10.4f\n", m.x.x, m.y.x, m.z.x, m.w.x);
    printf("%10.4f %10.4f %10.4f %10.4f\n", m.x.y, m.y.y, m.z.y, m.w.y);
    printf("%10.4f %10.4f %10.4f %10.4f\n", m.x.z, m.y.z, m.z.z, m.w.z);
    printf("%10.4f %10.4f %10.4f %10.4f\n", m.x.w, m.y.w, m.z.w, m.w.w);
}

mat4 scalar_matrix_multiplication(float s, mat4 m)
{
    m.x = scalar_vector_multiplication(s,m.x);
    m.y = scalar_vector_multiplication(s,m.y);
    m.z = scalar_vector_multiplication(s,m.z);
    m.w = scalar_vector_multiplication(s,m.w);

    return m;
}

mat4 matrix_matrix_addition(mat4 m1, mat4 m2)
{
    mat4 sum;
    sum.x = vector_vector_addition(m1.x,m2.x);
    sum.y = vector_vector_addition(m1.y,m2.y);
    sum.z = vector_vector_addition(m1.z,m2.z);
    sum.w = vector_vector_addition(m1.w,m2.w);

    return sum;
}

mat4 matrix_matrix_subtraction(mat4 m1, mat4 m2)
{
    mat4 difference;
    difference.x = vector_vector_subtraction(m1.x,m2.x);
    difference.y = vector_vector_subtraction(m1.y,m2.y);
    difference.z = vector_vector_subtraction(m1.z,m2.z);
    difference.w = vector_vector_subtraction(m1.w,m2.w);

    return difference;
}

mat4 matrix_matrix_multiplication(mat4 m1, mat4 m2)
{
    mat4 product;
    //column x
    product.x.x = (m1.x.x*m2.x.x) + (m1.y.x*m2.x.y) + (m1.z.x*m2.x.z) + (m1.w.x*m2.x.w);
    product.x.y = (m1.x.y*m2.x.x) + (m1.y.y*m2.x.y) + (m1.z.y*m2.x.z) + (m1.w.y*m2.x.w);
    product.x.z = (m1.x.z*m2.x.x) + (m1.y.z*m2.x.y) + (m1.z.z*m2.x.z) + (m1.w.z*m2.x.w);
    product.x.w = (m1.x.w*m2.x.x) + (m1.y.w*m2.x.y) + (m1.z.w*m2.x.z) + (m1.w.w*m2.x.w);
    //column y
    product.y.x = (m1.x.x*m2.y.x) + (m1.y.x*m2.y.y) + (m1.z.x*m2.y.z) + (m1.w.x*m2.y.w);
    product.y.y = (m1.x.y*m2.y.x) + (m1.y.y*m2.y.y) + (m1.z.y*m2.y.z) + (m1.w.y*m2.y.w);
    product.y.z = (m1.x.z*m2.y.x) + (m1.y.z*m2.y.y) + (m1.z.z*m2.y.z) + (m1.w.z*m2.y.w);
    product.y.w = (m1.x.w*m2.y.x) + (m1.y.w*m2.y.y) + (m1.z.w*m2.y.z) + (m1.w.w*m2.y.w);
    //column z
    product.z.x = (m1.x.x*m2.z.x) + (m1.y.x*m2.z.y) + (m1.z.x*m2.z.z) + (m1.w.x*m2.z.w);
    product.z.y = (m1.x.y*m2.z.x) + (m1.y.y*m2.z.y) + (m1.z.y*m2.z.z) + (m1.w.y*m2.z.w);
    product.z.z = (m1.x.z*m2.z.x) + (m1.y.z*m2.z.y) + (m1.z.z*m2.z.z) + (m1.w.z*m2.z.w);
    product.z.w = (m1.x.w*m2.z.x) + (m1.y.w*m2.z.y) + (m1.z.w*m2.z.z) + (m1.w.w*m2.z.w);
    //column w
    product.w.x = (m1.x.x*m2.w.x) + (m1.y.x*m2.w.y) + (m1.z.x*m2.w.z) + (m1.w.x*m2.w.w);
    product.w.y = (m1.x.y*m2.w.x) + (m1.y.y*m2.w.y) + (m1.z.y*m2.w.z) + (m1.w.y*m2.w.w);
    product.w.z = (m1.x.z*m2.w.x) + (m1.y.z*m2.w.y) + (m1.z.z*m2.w.z) + (m1.w.z*m2.w.w);
    product.w.w = (m1.x.w*m2.w.x) + (m1.y.w*m2.w.y) + (m1.z.w*m2.w.z) + (m1.w.w*m2.w.w);

    return product;
}

vec4 matrix_vector_multiplication(mat4 m, vec4 v)
{
    vec4 result;
    result.x = (m.x.x*v.x) + (m.y.x*v.y) + (m.z.x*v.z) + (m.w.x*v.w);
    result.y = (m.x.y*v.x) + (m.y.y*v.y) + (m.z.y*v.z) + (m.w.y*v.w);
    result.z = (m.x.z*v.x) + (m.y.z*v.y) + (m.z.z*v.z) + (m.w.z*v.w);
    result.w = (m.x.w*v.x) + (m.y.w*v.y) + (m.z.w*v.z) + (m.w.w*v.w);

    return result;
}

//mat4 inverse(mat4 m)
//{
//
//
//}

mat4 find_minor(mat4 m)
{
    
}


mat4 transpose(mat4 m)
{
    mat4 trans_mat;
    trans_mat.x.x = m.x.x;
    trans_mat.x.y = m.y.x;
    trans_mat.x.z = m.z.x;
    trans_mat.x.w = m.w.x;

    trans_mat.y.x = m.x.y;
    trans_mat.y.y = m.y.y;
    trans_mat.y.z = m.z.y;
    trans_mat.y.w = m.w.y;

    trans_mat.z.x = m.x.z;
    trans_mat.z.y = m.y.z;
    trans_mat.z.z = m.z.z;
    trans_mat.z.w = m.w.z;

    trans_mat.w.x = m.x.w;
    trans_mat.w.y = m.y.w;
    trans_mat.w.z = m.z.w;
    trans_mat.w.w = m.w.w;

    return trans_mat;
}
