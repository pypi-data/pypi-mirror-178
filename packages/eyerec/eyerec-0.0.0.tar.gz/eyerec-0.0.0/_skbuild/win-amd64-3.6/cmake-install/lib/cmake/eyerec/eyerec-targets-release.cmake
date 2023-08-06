#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "eyerec::eyerec" for configuration "Release"
set_property(TARGET eyerec::eyerec APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(eyerec::eyerec PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/eyerec.lib"
  )

list(APPEND _cmake_import_check_targets eyerec::eyerec )
list(APPEND _cmake_import_check_files_for_eyerec::eyerec "${_IMPORT_PREFIX}/lib/eyerec.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
