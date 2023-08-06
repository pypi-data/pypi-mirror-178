import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups


Item {
    width: parent.width
    height: 100
    property var text: tr.unpair_device
    property alias deleteButton: deleteButton
    property bool is_hub: false

    AjaxButton {
        id: deleteButton
        anchors.centerIn: parent
        text: parent.text
        color: ui.colors.light1
        opacity: enabled ? 1.0 : 0.5

        onClicked: {
            if (is_hub) return
            Popups.delete_device_popup(device)
        }
    }
}