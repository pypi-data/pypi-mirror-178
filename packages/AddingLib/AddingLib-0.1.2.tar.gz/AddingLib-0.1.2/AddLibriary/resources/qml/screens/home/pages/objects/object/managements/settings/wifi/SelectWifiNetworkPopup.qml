
import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
//import "qrc:/resources/qml/screens/hub/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk


AjaxPopup {
    id: popup
    width: 360
    height: 185

    modal: true
    focus: true

    property var wifi: null

    Rectangle {
        width: 360
        height: 185
        color: "#252525"

        Text {
            id: infoLabel
            text: util.insert(tr.connect_hub_to_a_wi_fi_network, [hub.name, wifi.ssid_name])
            width: parent.width - 24
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 12
            opacity: 0.5

            anchors {
                top: parent.top
                topMargin: 34
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSettingsTextField {
            id: wifiPassword

            miniText: tr.password
            field.text: ""
            field.echoMode: TextInput.Password

            width: popup.width - 32

            anchors {
                top: infoLabel.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }
        }

        MouseArea {
            width: parent.width
            height: 48
            anchors.bottom: parent.bottom

            Rectangle {
                height: 1
                width: parent.width
                opacity: 0.1
                color: ui.colors.light1
                anchors.top: parent.top
            }

            Text {
                anchors.centerIn: parent
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.green1
                text: tr.next
            }

            onClicked: {
                PopupsDesk.please_wait_popup()
                app.hub_management_module.select_wifi_network(wifi.ssid_name, wifiPassword.field.text, wifi.enc_type)
            }
        }
    }

    Connections {
        target: app.hub_management_module
        onSelectWifiNetworkSuccess: {
            popup.close()
            app.hub_management_module.get_wifi_networks()
        }
    }
}