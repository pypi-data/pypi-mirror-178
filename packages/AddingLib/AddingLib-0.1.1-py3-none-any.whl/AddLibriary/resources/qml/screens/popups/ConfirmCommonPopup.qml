import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 360
    height: contentText.height + 128
    closePolicy: Popup.CloseOnEscape

    property var todo: null
    property var text: ""

    property var buttonText: tr.confirm
    property var buttonColor: ui.colors.red1

    modal: true
    focus: true

    anchors.centerIn: parent

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        clip: true
        color: ui.colors.dark3
        radius: 10
        anchors.fill: parent

        Custom.FontText {
            id: contentText
            text: popup.text
            width: parent.width - 64
            height: contentHeight
            color: ui.colors.white
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            anchors {
                top: parent.top
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Item {
            width: parent.width
            height: 80
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    right: parent.right
                }
            }

            Item {
                width: parent.width / 2 - 44
                height: parent.height - 36
                anchors {
                    top: parent.top
                    topMargin: 16
                    left: parent.left
                    leftMargin: 32
                }

                Custom.Button {
                    width: parent.width
                    text: tr.cancel
                    color: ui.colors.white
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.close()
                    }
                }
            }

            Item {
                width: parent.width / 2 - 44
                height: parent.height - 36
                anchors {
                    top: parent.top
                    topMargin: 16
                    right: parent.right
                    rightMargin: 32
                }

                Custom.Button {
                    width: parent.width
                    text: popup.buttonText
                    color: popup.buttonColor
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        if (popup.todo) popup.todo()
                        popup.close()
                    }
                }
            }
        }
    }
}
