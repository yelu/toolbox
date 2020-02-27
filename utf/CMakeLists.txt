cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(utf)

file(GLOB UTF_SOURCES
     *.cpp)

file(GLOB UTF_HEADERS
     *.h)

add_executable(utf ${UTF_SOURCES} ${UTF_HEADERS})
target_include_directories(utf PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
