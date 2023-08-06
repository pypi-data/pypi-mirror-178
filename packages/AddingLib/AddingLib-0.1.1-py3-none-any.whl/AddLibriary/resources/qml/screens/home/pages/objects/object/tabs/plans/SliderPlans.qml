import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    property var tabs: null
    property var grid: null
    anchors.fill: parent
    color: ui.colors.dark4

    Image {
        id: fullImage
        width: parent.width - 16
        height: parent.height - 16
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit

        Connections {
            target: grid.model
            onDataChanged: {
                tabs.currentMediaIndexChanged(tabs.currentMediaIndex)
            }
        }

        source: {
            var url = grid.model.get_url(tabs.currentMediaIndex)["original"]
            if (typeof url == "undefined") return ""
            return url
        }
    }

    Item {
        width: 56
        height: 56
        anchors {
            top: parent.top
            right: parent.right
            rightMargin: planTab.isEditable ? 56 : 16
        }

        Rectangle {
            width: 30
            height: 30
            radius: height / 2
            color: ui.colors.dark1
            anchors.centerIn: parent

            Image {
                sourceSize.width: 40
                sourceSize.height: 40
                anchors.centerIn: parent
                source: "qrc:/resources/images/icons/a-search-icon.svg"
            }

            Custom.HandMouseArea {
                onClicked: {
                    Popups.plan_full_screen_popup(fullImage.source)
                }
            }
        }
    }

    IconContexMenu {
        width: 56
        height: 56
        visible: planTab.isEditable

        MouseArea {
            id: mouseIconEditMenu
            anchors.fill: parent
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            onClicked: {
                contextMenu.popup()
            }
            onPressAndHold: {
                if (mouse.source === Qt.MouseEventNotSynthesized)
                    contextMenu.popup()
            }
            EditMenu {
                id: contextMenu
                model: grid.model
                indexMenu: tabs.currentMediaIndex
            }
        }
    }
}