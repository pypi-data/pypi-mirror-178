import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Switch {
    id: control

//  Whether the mouse is over the switch
    readonly property bool containsMouse: area.containsMouse
//  Callback on toggle action
    property var onToggle: () => {}
//  Property which can change the active color of indicator
    property bool isDanger: false
//  Whether to cancel property binding
    property bool cancelBinding: true

    Component.onCompleted: if (cancelBinding) checked = checked

    width: indicator.width
    height: indicator.height

    opacity: enabled ? 1 : 0.3
    layer.enabled: true
    indicator: Rectangle {
        id: indicatorRectangle

        implicitWidth: 51
        implicitHeight: 30

        radius: implicitHeight / 2
        color: checked ? (isDanger ? ui.ds3.figure.attention : ui.ds3.bg.low) : ui.ds3.special.hole

        Rectangle {
            width: 26
            height: 26

            anchors.verticalCenter: parent.verticalCenter

            radius: width / 2
            x: control.checked ? parent.width - width - 2 : 2
            color: checked && !isDanger ? ui.ds3.figure.interactive : ui.ds3.special.knob

            Behavior on x {
                NumberAnimation {
                    duration: 100
                }
            }

            Behavior on color {
                ColorAnimation {
                    duration: 100
                }
            }
        }
    }

    DS3.MouseArea {
        id: area

        onClicked: onToggle()
        onDoubleClicked: {}
    }
}