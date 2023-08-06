cmake_minimum_required(VERSION 3.15)

set(CMAKE_OSX_DEPLOYMENT_TARGET "12.0" CACHE STRING "Minimum OS X deployment version")

project(pyftdc)

set(CMAKE_CXX_STANDARD 17)

# Get version from file
file(READ "version.txt" file_version)

message( "---------------------- library ${PROJECT_NAME} version: " ${file_version}  "----------------------------")

add_subdirectory(extern)
add_subdirectory(pybind11)
#add_subdirectory(Boost_tests)

pybind11_add_module(${PROJECT_NAME}
        src/python.cpp
        src/Chunk.cpp
        src/ConstDataRangeCursor.cpp
        src/Dataset.cpp
        src/FTDCParser.cpp
        src/MetricsToWTMap.cpp
        src/ParserTasksList.cpp
        src/SampleLocation.cpp
        src/WriterTaskList.cpp
        src/ChunkMetric.cpp
        src/CSVWriter.cpp
        src/FileParsedData.cpp
        src/JSONWriter.cpp
        src/ParserTask.cpp
        src/WriterTask.cpp
        )

target_link_libraries(${PROJECT_NAME} PRIVATE bson_static)

target_include_directories(${PROJECT_NAME} PUBLIC
        ${CMAKE_BINARY_DIR}/_deps/spdlog-src/include
        ${CMAKE_SOURCE_DIR}/src/include

        )
target_link_libraries(${PROJECT_NAME}  PUBLIC
        ${CMAKE_DL_LIBS}
        bson_static
        z)

