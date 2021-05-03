set(SPEEX_DIR ${CMAKE_SOURCE_DIR}/thirdparty/speexdsp)
set(SPEEX_BINARY_DIR ${CMAKE_BINARY_DIR}/speex-prefix)

ExternalProject_Add(speex
	SOURCE_DIR "${SPEEX_DIR}"
	DOWNLOAD_COMMAND cd ${SPEEX_DIR} && ${SPEEX_DIR}/autogen.sh
	CONFIGURE_COMMAND ${SPEEX_DIR}/configure --prefix=<INSTALL_DIR> --enable-static=yes --disable-shared
    BUILD_COMMAND make
	INSTALL_COMMAND make install
)

file(MAKE_DIRECTORY ${SPEEX_BINARY_DIR}/include)

add_library(speex::speex STATIC IMPORTED GLOBAL)
target_include_directories(speex::speex INTERFACE ${SPEEX_BINARY_DIR}/include)
#target_link_libraries(speex::speex INTERFACE "${speex_LIBRARIES}")
set_target_properties (speex::speex PROPERTIES
	IMPORTED_LOCATION ${SPEEX_BINARY_DIR}/lib/libspeexdsp.a
	INTERFACE_INCLUDE_DIRECTORIES ${SPEEX_BINARY_DIR}/include)
add_library(PkgConfig::SPEEX ALIAS speex::speex )
add_dependencies(speex::speex speex)
