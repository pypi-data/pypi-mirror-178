import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom

AjaxPopup {
    id: popup
    width: 320
    height: closeItem.height + 16 + contentItem.height + buttonGroup.height

    property var contentText: null
    property var todo: null
    property var labelText: null

    property var confirmText: null
    property var exitText: null
    property var saveColor: null

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

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
            height: 64
            radius: parent.radius
            title: labelText
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.top: closeItem.bottom
        }

        Item {
            id: contentItem

            width: parent.width
            height: contentTextItem.height + 32

            anchors.top: closeItem.bottom

            Text {
                id: contentTextItem

                text: contentText
                width: parent.width - 64
                height: contentHeight
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 14
                opacity: 0.8
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: parent.top
                    topMargin: 16
                    horizontalCenter: parent.horizontalCenter
                }
            }
        }

        Item {
            id: buttonGroup

            width: parent.width - 48
            height: 72

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }

            Custom.Button {
                id: cancelButton

                width: 130
                height: 40
                color: ui.colors.light3
                transparent: true

                text: exitText

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    popup.close()
                }
            }

            Custom.Button {
                id: nextButton

                width: 130
                height: 40
                color: saveColor
                transparent: true

                text: confirmText

                anchors {
                    left: cancelButton.right
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    popup.todo()
                }
            }
        }
    }

    Connections {
        target: app.security_module

//        onActionSuccess: {
//            popup.close()
//        }

        onTwoFaStateSignal: {
            popup.close()
        }
    }

    Component.onCompleted: {
        popup.labelText = labelText ? labelText : tr.warning
        popup.confirmText = confirmText ? confirmText : tr.save
        popup.exitText = exitText ? exitText : tr.cancel
        popup.saveColor = saveColor ? saveColor : "#60e3ab"
    }
}
