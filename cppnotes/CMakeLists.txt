cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(cppnotes)

file(GLOB CPPNOTES_SOURCES
     *.cpp)

file(GLOB CPPNOTES_HEADERS
     *.h)

add_executable(cppnotes ${CPPNOTES_SOURCES} ${CPPNOTES_HEADERS})
target_include_directories(cppnotes PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
