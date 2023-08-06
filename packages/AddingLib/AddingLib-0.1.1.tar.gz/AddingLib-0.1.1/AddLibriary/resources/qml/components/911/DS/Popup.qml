import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS" as DS


// Popup that contains cross button and any information placed inside column
Popup {
    id: popup

//  Title of the popup
    property alias title: titleItem.text
//  Weather to destruct component after closing. Preferrably do not change
    property bool destructOnClose: true
//  Visibility of cross button
    property bool hasCrossButton: true
//  Margins around the content
    property var contentMargins: 32

//  Components that should be placed inside content container
    default property alias content: contentContainer.data

    width: 300
    height: popupContainer.height

    anchors.centerIn: parent

    parent: ApplicationWindow.contentItem
    modal: true
    focus: true
    padding: 0
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }
    background: Rectangle {
        color: ui.backgrounds.overlay
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    onAboutToShow: {
    }

    onAboutToHide: {
    }

    onClosed: {
        if (destructOnClose) {
             popup.destroy()
        }
    }

    Rectangle {
        id: popupContainer

        width: parent.width
        height: titleItem.height + contentContainer.height + 64

        color: ui.backgrounds.base
        radius: 8

        DS.TextBodyLRegular {
            id: titleItem

            width: parent.width - 2 * 56

            anchors {
                top: parent.top
                margins: 32
                horizontalCenter: parent.horizontalCenter
            }

            horizontalAlignment: Text.AlignHCenter

            Binding on height {
                when: !titleItem.text
                value: 0
            }
        }

        Column {
            id: contentContainer

            anchors {
                left: parent.left
                right: parent.right
                top: titleItem.bottom
                margins: contentMargins
                topMargin: 4
            }
        }

        DS.ButtonRound {
            anchors {
                top: parent.top
                right: parent.right
                margins: 16
            }

            style: ui.controls.cross
            side: 32
            visible: hasCrossButton

            onClicked: popup.close()
        }
    }

    Component.onDestruction: {
        popup.close()
        modal = false
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            popup.close()
        }
    }
}
