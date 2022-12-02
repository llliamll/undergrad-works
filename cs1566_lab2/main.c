#include <stdio.h>
#include "matrix.h"
int main()
{
    vec4 v = {1,2,3,4};
    vec4 v2 = {5,6,7,8};
    mat4 m = {{1,-5,9,13},{2,6,-10,14},{3,7,11,15},{4,8,12,-16}};
    mat4 m2 = {{4,8,12,16},{3,7,11,15},{2,6,10,14},{1,5,9,13}};

//    mat4 i = {{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}};
//    print_mat(matrix_matrix_multiplication(m,i));
    printf("Print Vector V:\n");
    print_vec(v);

    printf("Scalar Multiplication of Vector V with 3.0:\n");
    print_vec(scalar_vector_multiplication(3,v));

    printf("Vector Addition of Vector V with Vector V2\n");
    print_vec(vector_vector_addition(v,v2));

    printf("Vector Subtraction of Vector V1 - Vector V2:\n");
    print_vec(vector_vector_subtraction(v,v2));

    printf("Magnitude of Vector V:\n");
    printf("%.4f", find_magnitude(v));

    printf("\nNormalize Vector V:\n");
    print_vec(normalize(v));

    printf("Dot Product of Vector V and V2:\n");
    printf("%.4f\n",dot_production(v,v2));

    printf("Cross Product of Vector V and V2:\n");
    print_vec(cross_production(v,v2));

    printf("Print Matrix M:\n");
    print_mat(m);

    printf("Scalar Multiplication of Matrix M with 3.0:\n");
    print_mat(scalar_matrix_multiplication(3,m));

    printf("Matrix Addition of Matrix M with Matrix M2:\n");
    print_mat(matrix_matrix_addition(m,m2));

    printf("Matrix Subtraction of Matrix M - Matrix M2:\n");
    print_mat(matrix_matrix_subtraction(m,m2));

    printf("Matrix Transpose of Matrix M:\n");
    print_mat(transpose(m));

    printf("Matrix Multiplication of Matrix M and Matrix M2:\n");
    print_mat(matrix_matrix_multiplication(m,m2));

    printf("Matrix Scalar Multiplication with Vector V and Matrix M:\n");
    print_vec(matrix_vector_multiplication(m,v));

    printf("\nInverse of Matrix M: working\n");

    printf("Checking Inverse of Matrix M: working");



}

