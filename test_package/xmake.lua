
add_rules("mode.release") 

target("test_package")

    set_kind("binary")

    add_files("src/*.c") 

--[[
 TODO: Use whatever function xmake has to "include" another lua file
            and include conanbuildinfo.xmake.lua. Then use xmake's 
            equivalent of target_link_libraries() from cmake to have 
            test_package "depend on" the xmake "conan_zlib" target
            See CMakeLists.txt from our test_package template below.
--]]


--[[

cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_package test_package.cpp)

target_link_libraries(test_package CONAN_PKG::zlib)

--]]