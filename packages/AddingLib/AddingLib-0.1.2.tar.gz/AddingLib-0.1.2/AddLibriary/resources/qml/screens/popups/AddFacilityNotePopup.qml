import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "addFacilityNotePopup"
    width: 360
//    height: parent.height - 144 < 800 ? parent.height - 144 : 800
    height: 528

    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

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
        radius: 8

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 100
            radius: parent.radius
            title: tr.a911_new_note
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            width: parent.width - 32
            height: parent.height - header.height
            clip: true
            anchors {
                bottom: parent.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Loader {
                id: bodyLoader
                anchors.fill: parent
            }
        }
    }

    Component.onCompleted: {
        bodyLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/EditNote.qml", {"addNote": true})
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }
}