import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup
    objectName: "facilityVersioningPopup"
    width: 400
    height: 120 + continueText.height

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape

    anchors.centerIn: parent

    property var text: ""
    property var continue_saving: null

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.FontText {
            id: continueText
            text: popup.text
            width: parent.width - 64
            height: contentHeight
            color: ui.colors.light3
            font.pixelSize: 16
            wrapMode: Text.WordWrap
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
                width: 156
                height: 40
                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
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
                width: 156
                height: 40
                visible: popup.enabled
                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Custom.Button {
                    width: parent.width
                    text: tr.continue_android
                    color: ui.colors.green1
                    transparent: true
                    anchors.centerIn: parent

                    onClicked: {
                        popup.close()
                        popup.continue_saving()
                    }
                }
            }
        }
    }
}