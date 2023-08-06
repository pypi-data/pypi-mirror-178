import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/"

Switch {
    id: control

    property var color: ui.colors.green1
    property var background_color: ui.colors.dark4
    property alias mouseArea: mouseArea

    property var toggleWidth: 40
    property var toggleHeight: 20

    HandMouseArea {
        id: mouseArea
        onClicked: {
            control.focus = true
        }
    }

    indicator: Rectangle {
        implicitWidth: control.toggleWidth
        implicitHeight: control.toggleHeight
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: control.toggleHeight / 2
        color: background_color
        border.color: "transparent"  // control.activeFocus ? ui.colors.green3 : "transparent"

        Rectangle {
            x: control.checked ? parent.width - width - 3: 3
            y: parent.height / 2 - height / 2
            width: control.toggleHeight - 6
            height: width
            radius: height / 2
            color: {
                if (!enabled) opacity = 0.2
                if (enabled) opacity = 1.0
                return control.checked ? control.color : ui.colors.middle2
            }

        }
    }
}