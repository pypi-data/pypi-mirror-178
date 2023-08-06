import QtQuick 2.12
import QtQuick.Controls 2.13


Loader {
    id: loader
    z: 99
    property var file_path: null
    source: file_path

    Component.onCompleted: {
        __watcher__.add_file(file_path)
    }

    onLoaded: {}

    Connections {
        target: __watcher__

        onTimeToReload: {
            if (file_path == path) {
                loader.source = ""
                loader.source = path
            }
        }
    }
}