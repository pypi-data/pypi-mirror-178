import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

Popup {
    id: topLevel

    parent: ApplicationWindow.contentItem

    anchors.centerIn: parent

    modal: true
    focus: true

    property var destructOnClose: true

    padding: 0

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }

    background: Rectangle {
        color: "black"
        opacity: 0.2
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
             topLevel.destroy()
        }
    }

    Component.onDestruction: {
        topLevel.close()
        modal = false
    }

    Connections {
        target: application
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            topLevel.close()
        }
    }
}
