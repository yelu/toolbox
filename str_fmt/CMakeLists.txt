cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

project(str_fmt)

file(GLOB SOURCES
     *.cpp)

file(GLOB HEADERS
     *.h)

add_executable(str_fmt ${SOURCES} ${HEADERS})
target_include_directories(str_fmt PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
