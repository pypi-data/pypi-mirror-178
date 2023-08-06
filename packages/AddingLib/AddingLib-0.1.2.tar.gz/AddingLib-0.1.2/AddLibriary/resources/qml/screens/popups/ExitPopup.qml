import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


// tr.yes
// tr.no
// tr.Are_you_sure_you_want_to_exit_desktop


AjaxPopup {
    id: topLevel
    width: 400
    height: 100
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true

    property var action: null

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
        anchors.fill: parent
        color: ui.colors.dark3
        focus: true

        Keys.onReturnPressed: yesButton.clicked()
        Keys.onEnterPressed: yesButton.clicked()

        Item {
            id: closeIco
            width: parent.height
            height: parent.height

            Image {
                sourceSize.width: parent.height
                sourceSize.height: parent.height
                source: "qrc:/resources/images/icons/a-logo-pro.svg"
                anchors.centerIn: parent
                opacity: 0.9
            }
        }

        Custom.FontText {
            text: tr.Are_you_sure_you_want_to_exit_desktop
            opacity: 0.9
            width: parent.width - closeIco.width - 32
            height: contentHeight
            color: ui.colors.white
            font.pixelSize: 14
            font.letterSpacing: 1
            wrapMode: Text.WordWrap
            textFormat: Text.AutoText
            anchors {
                top: parent.top
                topMargin: 16
                left: closeIco.right
                leftMargin: 16
            }
        }

        Item {
            width: 64
            height: 48
            anchors {
                right: noButton.left
                rightMargin: 16
                bottom: parent.bottom
                bottomMargin: 8
            }

            Custom.Button {
                id: yesButton
                width: parent.width
                text: tr.yes
                transparent: false
                color: ui.colors.green1
                anchors.centerIn: parent
                backgroundItem.height: down ? 32 : 36

                onClicked: {
                    topLevel.action()
                }
            }
        }

        Item {
            id: noButton
            width: 64
            height: 48
            anchors {
                right: parent.right
                rightMargin: 24
                bottom: parent.bottom
                bottomMargin: 8
            }

            Custom.Button {
                width: parent.width
                text: tr.no
                transparent: true
                color: ui.colors.green1
                anchors.centerIn: parent
                backgroundItem.height: down ? 32 : 36

                onClicked: {
                    topLevel.close()
                }
            }
        }
    }
}
