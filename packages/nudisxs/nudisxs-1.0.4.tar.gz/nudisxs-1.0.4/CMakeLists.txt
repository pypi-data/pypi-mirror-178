cmake_minimum_required(VERSION 3.17.0)

project(nudisxs LANGUAGES C CXX Fortran)

option(SKBUILD "Should be ON of being build by skbuild,
and OFF of being build by regular cmake" OFF)

if (NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
endif()

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/")
find_package(PythonExtensions REQUIRED)
find_package(NumPy)
find_package(F2PY REQUIRED)
find_package(LHAPDF REQUIRED)

message(STATUS "F2PY included from: ${F2PY_INCLUDE_DIR}")
message(STATUS "LHAPDF_LIBRARIES included from: ${LHAPDF_LIBRARIES}")
message(STATUS "NumPy included from: ${NumPy_INCLUDE_DIR}")

set(LIBNAME DISxs)
set(SOURCES
  nudisxs/f_sources/d2sDISCC_dxdy.f
  nudisxs/f_sources/d2sDISNC_dxdy.f
  nudisxs/f_sources/NucleonStructureFunctions.f
  nudisxs/f_sources/PhysMathConstants.f
  nudisxs/f_sources/xDIS.f
  nudisxs/f_sources/yDIS.f
  nudisxs/f_sources/DISkinematics.f
  nudisxs/f_sources/FunGeM.f
  nudisxs/f_sources/Routines.f
  nudisxs/f_sources/FQCD_L.f
  nudisxs/f_sources/F_L.f
  nudisxs/f_sources/R.f
  nudisxs/f_sources/R_Liang.f
  nudisxs/f_sources/R_WBA.f
  nudisxs/f_sources/InpOutUnits.f
  nudisxs/f_sources/BendFactor.f
  nudisxs/f_sources/Spline2.f
  nudisxs/f_sources/GeM.f
  nudisxs/f_sources/R_E143.f
  nudisxs/f_sources/SF_Liang.f
  )

#execute_process(COMMAND lhapdf-config --ldflags RESULT_VARIABLE LHAPDF_RESULT OUTPUT_VARIABLE LHAPDF_LDFLAGS OUTPUT_STRIP_TRAILING_WHITESPACE)
#set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} ${LHAPDF_LDFLAGS} -lstdc++")

set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -fPIC -freal-4-real-8  -lstdc++")

add_library(${LIBNAME} SHARED ${SOURCES})
target_link_libraries(${LIBNAME} ${LHAPDF_LIBRARIES})

set(f2py_module_name "_nudisxs")
set(generated_module_file ${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_name}${PYTHON_EXTENSION_MODULE_SUFFIX})

add_custom_target(${f2py_module_name} ALL
  DEPENDS ${generated_module_file}
)

add_custom_command(
  OUTPUT ${generated_module_file}
  COMMAND ${F2PY_EXECUTABLE}
    -m ${f2py_module_name}
    -c
    --f90flags='-fPIC -freal-4-real-8'
    -L${CMAKE_CURRENT_BINARY_DIR}
    -lDISxs
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/BendFactor.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/d2sDISCC_dxdy.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/d2sDISNC_dxdy.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/DISkinematics.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/F_L.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/NucleonStructureFunctions.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/PhysMathConstants.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R_E143.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R_Liang.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/R.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/SF_Liang.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/xDIS.f
    ${CMAKE_SOURCE_DIR}/nudisxs/f_sources/yDIS.f
#    ${LHAPDF_LIBRARIES}
#    ${CMAKE_Fortran_FLAGS}
    --quiet
    --lower
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  DEPENDS ${sources} ${LHAPDF_LIBRARIES}
  )



if (SKBUILD)
  install(FILES ${generated_module_file} DESTINATION nudisxs)
  install(TARGETS DISxs DESTINATION nudisxs)
else()
  install(FILES ${generated_module_file} DESTINATION ${CMAKE_SOURCE_DIR}/nudisxs)
  install(TARGETS DISxs  DESTINATION ${CMAKE_SOURCE_DIR}/nudisxs)
endif()
