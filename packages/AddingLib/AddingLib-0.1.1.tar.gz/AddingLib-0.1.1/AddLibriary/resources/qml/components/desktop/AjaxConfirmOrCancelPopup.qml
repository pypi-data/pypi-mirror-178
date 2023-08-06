import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup

    width: 320
    height: closeItem.height + contentText.height + 60

    property var todo: null
    property var headerText: tr.information
    property var confirmText: ""
    property var actionText: null

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
            label: popup.headerText
        }

        Text {
            id: contentText

            width: parent.width - 32
            height: contentHeight + 16

            text: confirmText
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 14
            textFormat: Text.RichText
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
            anchors.top: closeItem.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        AjaxSaveCancel {
            id: saveCancel

            width: parent.width
            height: 48

            saveText: popup.actionText ? popup.actionText : tr.ok
            anchors.bottom: parent.bottom

            saveArea.onClicked: {
                popup.todo()
            }

            cancelArea.onClicked: {
                popup.close()
            }
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            popup.close()
        }

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            popup.close()
        }
    }
}
