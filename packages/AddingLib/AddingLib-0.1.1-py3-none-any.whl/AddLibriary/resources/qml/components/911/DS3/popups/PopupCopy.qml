import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Popup {
    id: popupCopy

    property var text: tr.copied

    width: 300
    height: 54

    parent: ApplicationWindow.contentItem
    x: Math.round(parent.width - width - 24)
    y: Math.round(parent.height - height - 24)

    background: Rectangle {
        width: parent.width
        height: parent.height

        color: ui.colors.black
        radius: 8

        border {
            width: 1

            color: ui.ds3.bg.high
        }

        DS3.Text {
            id: miniNofication

            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            text: popupCopy.text
            style: ui.ds3.text.body.MRegular
        }

        Image {
            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            source: "qrc:/resources/images/icons/a-delete-button.svg"
            sourceSize.width: 24
            sourceSize.height: 24

            DS3.MouseArea {
                onClicked: {
                    popupCopy.close()
                }
            }
        }
    }

    onOpened: {
        timer.start()
    }

    Timer {
        id: timer

        interval: 3000 // milliseconds
        running: true
        repeat: false

        onTriggered: {
            popupCopy.close()
        }
    }
}
