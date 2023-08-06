import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    width: parent.width
    height: 100
    property var text: tr.unpair_device
    property alias deleteButton: deleteButton
    property bool is_hub: false
    property bool is_access_card: false


    AjaxButton {
        id: deleteButton

        text: parent.text
        color: "white"

        anchors.centerIn: parent

        onClicked: {
            if (is_hub) return
            if (is_access_card) return
            Popups.delete_device_popup(hub.hub_id, device, management)
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: "delete_device_" + device.id + "_button"
        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            deleteButton.clicked(true)
        }
        /* ---------------------------------------------------- */
    }
}