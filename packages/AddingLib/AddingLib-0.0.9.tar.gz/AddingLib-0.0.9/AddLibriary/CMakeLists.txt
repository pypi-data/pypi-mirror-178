set(video_player_plugin "videoPlugin")

find_package (Python COMPONENTS Interpreter Development)

#set(CMAKE_SKIP_BUILD_RPATH TRUE)
#set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
#set(CMAKE_INSTALL_RPATH ${CMAKE_CURRENT_BINARY_DIR})
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
#set(CMAKE_SKIP_RPATH TRUE)

add_custom_target(
 run ALL
 COMMAND ${Python_EXECUTABLE} resources_collector.py
 COMMENT "Generating resources file"
 WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
 BYPRODUCTS plugin.qrc
)

set(CMAKE_AUTOMOC ON)

qt5_add_resources(PLUGIN_RESOURCES ${CMAKE_CURRENT_LIST_DIR}/plugin.qrc)

add_library(
    ${video_player_plugin}
    SHARED
    ${CMAKE_CURRENT_LIST_DIR}/VideoPlugin.h
    ${CMAKE_CURRENT_LIST_DIR}/VideoPlugin.cpp
    ${CMAKE_CURRENT_LIST_DIR}/qmldir
    ${PLUGIN_RESOURCES}
)

#set_target_properties(${video_player_plugin} PROPERTIES LINK_FLAGS "-Wl,-rpath")


add_dependencies(${video_player_plugin} run)

target_link_libraries(${video_player_plugin} PUBLIC
                        Qt5::Qml 
                        videoItem
)

# During plugin searching Qt will be looking for 'qmldir' file
# So we should place it next to our plugin lib.

add_custom_command(
    TARGET ${video_player_plugin}
    POST_BUILD
    COMMAND
        ${CMAKE_COMMAND} -E copy
        ${CMAKE_CURRENT_LIST_DIR}/qmldir
        $<TARGET_FILE_DIR:${video_player_plugin}>/qmldir
)

if(DEFINED DESKTOP_PLUGIN_PATH)
    add_custom_command(
        TARGET ${video_player_plugin}
        POST_BUILD
        COMMAND
            ${CMAKE_COMMAND} -E copy
            ${CMAKE_CURRENT_BINARY_DIR}/lib${video_player_plugin}.dylib
            ${DESKTOP_PLUGIN_PATH}
    )
    add_custom_command(
    TARGET  ${video_player_plugin}
    POST_BUILD
    COMMAND
        ${CMAKE_COMMAND} -E copy
        ${CMAKE_CURRENT_LIST_DIR}/qmldir
        ${DESKTOP_PLUGIN_PATH}
)
endif(DEFINED DESKTOP_PLUGIN_PATH)