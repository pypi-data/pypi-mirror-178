import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "addFastResponseTeamPopup"
    width: 328
    height: parent.height - 144 < 800 ? parent.height - 144 : 800
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    property var editMode: true
    property var currentObject: null

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
        radius: 10

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_add_crew
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            id: bodyItem
            width: parent.width
            clip: true
            anchors {
                top: header.bottom
                topMargin: 8
                bottom: parent.bottom
            }

            Loader {
                id: bodyLoader
                anchors.fill: parent
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }

    Component.onCompleted: {
        bodyLoader.setSource("qrc:/resources/qml/screens/home/pages/company/gbr/EditInfoComponent.qml", {"addTeam": true})
    }
}
