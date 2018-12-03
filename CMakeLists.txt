cmake_minimum_required(VERSION 3.0)   # CMake version check
project(AI_homework)               # Create project "simple_example"
set(CMAKE_CXX_STANDARD 11)            # Enable c++11 standard

set(SOURCE_FILES week_6/main.cpp)            # Add main.cpp file of project root directory as source file
add_executable(week_6 "week_6/main.cpp" week_6/main.cpp)