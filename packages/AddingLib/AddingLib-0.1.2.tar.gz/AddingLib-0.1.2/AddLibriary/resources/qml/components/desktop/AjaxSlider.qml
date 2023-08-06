import QtQuick 2.7
import QtQuick.Controls 2.1

Slider {
    id: control
    value: 0

    property alias circle: circle

    onValueChanged: {
        value = value
    }

    background: Rectangle {
        x: control.leftPadding
        y: control.topPadding + control.availableHeight / 2 - height / 2
        implicitWidth: 200
        implicitHeight: 4
        width: control.availableWidth
        height: implicitHeight
        radius: 2
        color: enabled ? "#bdbebf" : ui.colors.middle3

        Rectangle {
            width: control.visualPosition * parent.width
            height: parent.height
            color: enabled ? "#60e3ab" : ui.colors.middle3
            radius: 2
        }
    }

    handle: Rectangle {
        id: circle
        x: control.leftPadding + control.visualPosition * (control.availableWidth - width)
        y: control.topPadding + control.availableHeight / 2 - height / 2
        implicitWidth: 22
        implicitHeight: 22
        radius: 11

        color: {
            return control.pressed ? "#f0f0f0" : "#f6f6f6"
        }
        border.color: enabled ? "#bdbebf" : ui.colors.middle3
    }
}