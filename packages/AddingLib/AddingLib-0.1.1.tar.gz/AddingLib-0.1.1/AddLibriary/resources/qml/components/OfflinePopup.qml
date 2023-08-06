import QtQuick 2.14
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/" as Custom

AjaxPopup {
    id: popup
    objectName: "offlinePopup"
    width: 320
    height: 200

    parent: ApplicationWindow.contentItem

    modal: true

    closePolicy: Popup.NoAutoClose

    background: Rectangle {
        width: application.width
        height: application.height
        color: ui.colors.black
        x: 0 - parent.x
        y: 0 - parent.y
        opacity: 0.3
    }



    Item {
        width: 320
        height: 130
        anchors.fill: parent

        Custom.FontText {
            id: textOffline
            font.pixelSize: 36
            text: tr.Com_no_connection0 + "..."
            anchors.centerIn: parent
            textFormat: Text.PlainText

            ColorAnimation on color {
                from: ui.colors.red1
                to: ui.colors.red3
                loops: -1
                duration: 2500
                easing.type: Easing.OutInQuad
            }
        }
    }
}