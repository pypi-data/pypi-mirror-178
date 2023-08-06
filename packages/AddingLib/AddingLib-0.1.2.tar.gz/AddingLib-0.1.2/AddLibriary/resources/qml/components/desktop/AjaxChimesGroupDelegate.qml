import QtQuick 2.13
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: chimesGroupDelegate

    width: parent.width
    height: 72

    property var group: null
    property var enabled: group.chimes_status.startsWith("ALL_READY")
    property var checked: group.chimes_status.endsWith("ENABLED")

    objectName: "chimesGroupDelegate"
    opacity: enabled ? 1 : 0.5

    Custom.RoundImage {
        id: imageItem

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 24
        }

        imageWidthHeight: 64
        imageSource: group.small_image_link
    }

    Custom.FontText {
        anchors {
            verticalCenter: parent.verticalCenter
            left: imageItem.right
            leftMargin: 16
            right: checkBox.left
            rightMargin: 16
        }

        text: group.name
        color: ui.colors.light3
        wrapMode: Text.NoWrap
        elide: Text.ElideRight
        textFormat: Text.PlainText
    }

    AjaxCheckBox {
        id: checkBox

        checked: parent.checked

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 25
        }
    }

    Custom.HandMouseArea {
        onClicked: {
            if (chimesGroupDelegate.enabled) {
                checked = !checkBox.checked
                availableGroupsList.checkedCounter += checked ? 1 : -1
            }
        }
    }
}
