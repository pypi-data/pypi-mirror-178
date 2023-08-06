import QtQuick 2.12
import QtQuick.Controls 2.13


// Custom mouse area with pointing hand cursor and hover enabled
//
// 6074 added debounce
MouseArea {
    property alias interval: timer.interval

    enabled: true
    anchors.fill: parent
    hoverEnabled: true
    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
    
    onClicked: {
        enabled = false
        timer.start()
    }

    Timer {
        id: timer

        interval: 200

        onTriggered: {
            parent.enabled = true
        }
    }
}