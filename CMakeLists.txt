cmake_minimum_required(VERSION 3.8)
project(k1_description)

find_package(ament_cmake REQUIRED)

if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/assets/robots/K1)
  message(FATAL_ERROR "assets/ submodule missing: run `git submodule update --init --recursive`")
endif()

install(DIRECTORY urdf config launch DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY assets/robots/K1 DESTINATION share/${PROJECT_NAME}/assets/robots)

install(PROGRAMS scripts/generate_k1_urdf.py
  DESTINATION share/${PROJECT_NAME}/scripts
)

ament_package()
