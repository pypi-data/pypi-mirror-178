import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "timeSyncPopup"
    width: 328
    height: firstText.height + secondText.height + thirdText.height + fourthText.height + 240
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    anchors.centerIn: parent

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 10

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.attention_time_synchronization_911
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Custom.FontText {
            id: firstText
            text: tr.automatic_date_time_911
            color: ui.colors.middle1
            font.pixelSize: 14
            width: parent.width - 64
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: header.bottom
                topMargin: -8
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.FontText {
            id: secondText
            text: tr.enable_automatic_date_time_911
            color: ui.colors.light3
            font.pixelSize: 14
            width: parent.width - 64
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: firstText.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.FontText {
            id: thirdNumText
            text: "1."
            color: ui.colors.middle1
            font.pixelSize: 14
            width: 16
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: secondText.bottom
                topMargin: 8
                left: parent.left
                leftMargin: 32
            }
        }

        Custom.FontText {
            id: thirdText
            text: tr.automatic_date_time_step_1_911
            color: ui.colors.middle1
            font.pixelSize: 14
            width: parent.width - 88
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: secondText.bottom
                topMargin: 8
                left: parent.left
                leftMargin: 56
            }
        }

        Custom.FontText {
            id: fourthNumText
            text: "2."
            color: ui.colors.middle1
            font.pixelSize: 14
            width: 16
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: thirdText.bottom
                topMargin: 8
                left: parent.left
                leftMargin: 32
            }
        }

        Custom.FontText {
            id: fourthText
            text: tr.automatic_date_time_step_2_911
            color: ui.colors.middle1
            font.pixelSize: 14
            width: parent.width - 88
            height: contentHeight
            lineHeight: 1.2
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter
            anchors {
                top: thirdText.bottom
                topMargin: 8
                left: parent.left
                leftMargin: 56
            }
        }

        Item {
            id: buttonItem
            width: parent.width
            height: 88
            anchors.bottom: parent.bottom

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors.right: parent.right
            }

            Item {
                width: parent.width - 64
                height: 48
                anchors.centerIn: parent

                Custom.Button {
                    width: parent.width
                    text: tr.ok
                    transparent: false
                    anchors.centerIn: parent
                    onClicked: {
                        popup.close()
                    }
                }
            }
        }
    }
}