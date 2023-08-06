import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Custom green cursor for input components
Rectangle {
    width: 2
    height: 24

    visible: parent.cursorVisible
    color: ui.colors.interactive

    onVisibleChanged: {
        if (visible) {
            opacity = 1
            timer.start()
        }
        else timer.stop()
    }

    Timer {
        id: timer

        interval: 700
        running: true
        repeat: true

        onTriggered: parent.opacity = !parent.opacity ? 1 : 0
    }

    Connections {
        target: parent

        onCursorPositionChanged: {
            opacity = 1
            timer.restart()
        }
    }
}
