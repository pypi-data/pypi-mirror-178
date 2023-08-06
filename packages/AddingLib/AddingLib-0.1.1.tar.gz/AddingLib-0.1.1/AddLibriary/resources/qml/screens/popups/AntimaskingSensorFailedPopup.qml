import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup

    width: 362
    height: closeItem.height + column.height + buttonGroup.height + 48

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        radius: 10
        color: ui.colors.dark3
        anchors.fill: parent

        focus: true

        Keys.onEnterPressed: {
            save.clicked(true)
        }

        Keys.onReturnPressed: {
            save.clicked(true)
        }

        Custom.PopupHeader {
            id: closeItem
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.information
            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }

            Rectangle {
                width: parent.width
                height: 1
                color: ui.colors.middle1
                opacity: 0.1
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }

        Column {
            id: column

            width: parent.width
            spacing: 16

            anchors {
                top: closeItem.bottom
                topMargin: 24
            }

            Text {
                id: textLabel

                width: parent.width - 32

                anchors.horizontalCenter: parent.horizontalCenter

                text: tr.malfunction_5
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 16
            }
        }

        Item {
            id: buttonGroup
            width: parent.width
            height: 88
            anchors {
                top: column.bottom
                topMargin: 24
            }

            Custom.Button {
                width: parent.width - 64
                text: tr.ok
                color: ui.colors.light3
                transparent: true
                anchors.centerIn: parent

                onClicked: {
                    popup.close()
                }
            }
        }
    }
}