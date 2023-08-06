import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/"

AjaxPopup {
    id: popup
    width: 360
    height: closeItem.height + 16 + contentItem.height + buttonGroup.height

    property var contentText: null
    property var todo: null
    property var cancelTodo: null
    property var closeTodo: null
    property var labelText: null

    property var confirmText: null
    property var exitText: null
    property var saveColor: null

    Rectangle {
        anchors.fill: parent
        color: "#212121"
        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        focus: true

        Keys.onEnterPressed: {
            save.clicked(true)
        }

        Keys.onReturnPressed: {
            save.clicked(true)
        }

        AjaxPopupCloseHeader {
            id: closeItem
            label: labelText

            icoCloseArea.onClicked: {
                popup.close()
                if (popup.closeTodo) {
                    popup.closeTodo()
                }
            }
        }

        Item {
            id: contentItem

            width: parent.width
            height: contentTextItem.height + 32
//            color: "transparent"
//            border {
//                color: "red"
//                width: 1
//            }
            anchors {
                top: closeItem.bottom
//                topMargin: 16
            }

            Text {
                id: contentTextItem

                text: {
                    return contentText
                }
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

        AjaxSaveCancel {
            id: buttonGroup
            anchors.bottom: parent.bottom

            cancelText: exitText
            cancelArea.onClicked: {
                popup.close()
                if (popup.cancelTodo) {
                    popup.cancelTodo()
                }
            }

            saveAreaColor: saveColor
            saveText: confirmText
            saveArea.onClicked: {
                popup.todo()
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

//        onTfaState: {
//            popup.close()
//        }
    }

    Component.onCompleted: {
        popup.labelText = labelText ? labelText : tr.warning
        popup.confirmText = confirmText ? confirmText : tr.save
        popup.exitText = exitText ? exitText : tr.cancel
        popup.saveColor = saveColor ? saveColor : "#60e3ab"
    }
}
