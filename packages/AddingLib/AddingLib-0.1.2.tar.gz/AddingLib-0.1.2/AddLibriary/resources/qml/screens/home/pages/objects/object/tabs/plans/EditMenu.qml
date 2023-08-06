import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom

Menu {

    width: 144
    height: 84
    property var model: null
    property var indexMenu: -1
    MenuItem {
        id: menuEditItem
        text: tr.edit
        contentItem: Item {
            anchors.fill: parent
            Text {
                text: menuEditItem.text
                font: menuEditItem.font
                opacity: enabled ? 1.0 : 0.3
                color: ui.colors.light3
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    leftMargin: 16
                }
            }
        }
        background: Rectangle {
            implicitWidth: 144
            implicitHeight: 40
            color: menuEditItem.highlighted ? ui.colors.dark1 : "#292929"
        }
        onTriggered: Popups.update_facility_media(model.get_media(indexMenu))
    }
    MenuSeparator {
        width: 144
        height: 2
        background: Rectangle {
            implicitWidth: 144
            implicitHeight: 1
            color: ui.colors.black
        }

    }

    MenuItem {
        id: menuDeleteItem
        text: tr.unpair
        contentItem: Item {
            anchors.fill: parent
            Text {
                text: menuDeleteItem.text
                font: menuDeleteItem.font
                opacity: enabled ? 1.0 : 0.3
                color: ui.colors.red1
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    leftMargin: 16
                }
            }
        }
        onTriggered: Popups.delete_facility_media(model.get_media(indexMenu))
        background: Rectangle {
            implicitWidth: 144
            implicitHeight: 40
            color: menuDeleteItem.highlighted ? ui.colors.dark1 : "#292929"
        }
    }
    MenuSeparator {
        width: 144
        height: 2
        background: Rectangle {
            implicitWidth: 144
            implicitHeight: 1
            color: ui.colors.black
        }
    }

}