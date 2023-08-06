import QtQuick 2.12
import QtQuick.Controls 2.2
import QtWebEngine 1.8

import "qrc:/resources/qml/components/desktop/"

AjaxPopup {
    id: popup
    objectName: "textPopup"
    width: 640
    height: parent.height - 100

    closePolicy: Popup.NoAutoClose
    parent: ApplicationWindow.contentItem

    property string url: ""

    Rectangle {
        width: popup.width
        height: popup.height
        anchors.fill: parent
        color: "#393939"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999
        focus: true

        WebEngineView {
            id: webEngine
            width: parent.width
            height: parent.height - 48
            url: popup.url
        }

        AjaxSaveCancel {
            width: parent.width
            height: 48
            anchors.bottom: parent.bottom
            saveText: tr.accept
            cancelText: tr.decline

            saveArea.onClicked: {
                popup.close()
                client.sync_check_agreement_and_policy()
            }

            cancelArea.onClicked: {
                popup.close()
                client.logout(false)
            }
        }
    }
}