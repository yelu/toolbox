cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(protobuf_dym_compile)

include(FetchContent)
FetchContent_Declare(
  protobuf
  GIT_REPOSITORY https://github.com/protocolbuffers/protobuf.git
  GIT_TAG        v3.12.0
  SOURCE_SUBDIR  cmake
)
set(protobuf_BUILD_TESTS OFF CACHE BOOL "")
set(protobuf_BUILD_SHARED_LIBS OFF CACHE BOOL "")
set(protobuf_MSVC_STATIC_RUNTIME OFF CACHE BOOL "")
FetchContent_MakeAvailable(protobuf)

add_executable(compile_proto "main.cpp")
target_compile_definitions(compile_proto PUBLIC -DNOMINMAX -D_SCL_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_WARNINGS)
target_link_libraries(compile_proto 
    PUBLIC protobuf::libprotobuf protobuf::libprotoc)
