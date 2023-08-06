import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 328
    height: 292
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true
    anchors.centerIn: parent

    property var duration: 200
    property var text;
    Timer {
        id: timer
        running: true
        repeat: false
        interval: 900
        onTriggered: {
            popup.close()
        }
    }
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
        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: ""

            closeArea.onClicked: {
                popup.close()
            }
        }
        Item {
            id: logo
            width: parent.width
            height: 28
            anchors {
                top: header.bottom
            }
            Image {
                source: "qrc:/resources/images/desktop/logo/logo-pants-white.svg"
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }

        }
        Item {

            anchors {
                top: parent.top
                topMargin: 132
                left: parent.left
                leftMargin: 32
                right: parent.right
                rightMargin: 32
                bottom: parent.bottom
            }
            Custom.FontText {
                width: parent.width
                text: popup.text
                wrapMode: Text.WordWrap
                color: ui.colors.light3
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 16
            }
        }
    }
}
