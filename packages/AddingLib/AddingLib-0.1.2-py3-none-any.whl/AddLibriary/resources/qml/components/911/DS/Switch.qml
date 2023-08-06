import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS/" as DS


Switch {
    id: control

    readonly property bool containsMouse: area.containsMouse

    width: indicator.width
    height: indicator.height

    indicator: Rectangle {
        implicitWidth: 40
        implicitHeight: 24
        radius: 12
        color: ui.backgrounds.low

        Rectangle {
            width: 16
            height: 16

            anchors.verticalCenter: parent.verticalCenter

            x: control.checked ? parent.width - width - 4 : 4
            radius: 8
            color: control.checked ? ui.colors.interactive : ui.colors.secondary

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

    DS.MouseArea {
        id: area

        onClicked: toggled()
    }
}
