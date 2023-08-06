import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS/" as DS


// Custom DS checkbox with checkmark box and title
CheckBox {
    id: checkbox

//  Maximum width of the checkbox. The width of checkbox is calculated automatically.
//  When width is greater than maxWidth, text get wrapped.
    property var maxWidth: parent.width

    width: contentText.width + indicator.width + 10
    height: contentItem.height

    opacity: enabled ? 1 : 0.3
    padding: 0

    indicator: Rectangle {
        id: indicator

        implicitWidth: 22
        implicitHeight: 22
        radius: 2
        border.width: 1.5
        border.color: checkbox.checked ? ui.colors.interactive : ui.colors.secondary
        color: checkbox.checked ? ui.colors.interactive : ui.colors.transparent

        anchors.verticalCenter: parent.verticalCenter

        Item {
            width: 10
            height: 5

            anchors.centerIn: parent

            visible: checkbox.checked
            rotation: -45

            Rectangle {
                width: 2
                height: 5

                anchors.left: parent.left

                color: ui.colors.inverted
            }

            Rectangle {
                width: 10
                height: 2

                anchors.bottom: parent.bottom

                color: ui.colors.inverted
            }
        }

        DS.MouseArea {
            onClicked: checkbox.checked = !checkbox.checked
        }
    }

    contentItem: Item {
        height: contentText.contentHeight

        anchors {
            left: parent.left
            leftMargin: indicator.width + 10
        }

        DS.Text {
            id: contentText

            text: checkbox.text
            size: 16
            line: 24
            color: ui.colors.base

            onWidthChanged: {
                if (width > maxWidth - parent.anchors.leftMargin) width = maxWidth - parent.anchors.leftMargin
            }

            DS.MouseArea {
                onClicked: checkbox.checked = !checkbox.checked
            }
        }
    }
}
