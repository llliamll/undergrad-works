cmake_minimum_required(VERSION 3.17.3)
project(cs1566_lab2 C)

set(CMAKE_C_STANDARD 99)

add_executable(cs1566_lab2 main.c matrix.c matrix.h)
target_link_libraries(cs1566_lab2 m)
