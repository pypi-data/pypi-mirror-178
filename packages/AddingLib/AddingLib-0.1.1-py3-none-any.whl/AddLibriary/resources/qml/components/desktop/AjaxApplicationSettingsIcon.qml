import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups

Item {
    width: 64
    height: 64

    MouseArea {
        id: mouseArea
        width: 16
        height: 16
        anchors.centerIn: parent

        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onEntered: {
            column.opacity = 1.0
        }

        onExited: {
            column.opacity = 0.0
        }

        onClicked: application_settings()
    }

    Column {
        anchors.centerIn: parent
        spacing: 5

        Repeater {
            model: 3
            Rectangle {
                height: 2
                width: 16
                color: "#a3a3a3"
            }
        }
    }

    Column {
        id: column
        anchors.centerIn: parent
        spacing: 5

        opacity: 0

        Behavior on opacity { NumberAnimation { duration: 200 } }

        Repeater {
            model: 3
            Rectangle {
                height: 2
                width: 16
                color: ui.colors.green1
            }
        }
    }

    function application_settings() {
        Popups.application_settings_popup()
    }
}