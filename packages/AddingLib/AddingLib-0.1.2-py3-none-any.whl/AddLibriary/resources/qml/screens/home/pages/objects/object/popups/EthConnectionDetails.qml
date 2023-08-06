import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: popup

    property var devEnable: true
    property var sideMargin: 24

    anchors.centerIn: parent

    width: 500

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        id: connecionDetails

        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.InputSingleLine {
            id: ipAddressField

            atomInput {
                label: tr.ip_address
                text: device.eth_ip || tr.no_data_full
                readOnly: true
                validator: RegExpValidator { regExp: ui.regexes.ip }
                required: false
            }
            rightIcon.source: ''
        }

        DS3.InputSingleLine {
            id: maskField

            atomInput {
                label: tr.subnet_mask
                text: device.eth_mask || tr.no_data_full
                readOnly: true
                validator: RegExpValidator { regExp: ui.regexes.ip }
                required: false
            }
            rightIcon.source: ''
        }

        DS3.InputSingleLine {
            id: routerField

            atomInput {
                label: tr.gateway
                text: device.eth_gate || tr.no_data_full
                readOnly: true
                validator: RegExpValidator { regExp: ui.regexes.ip }
                required: false
            }
            rightIcon.source: ''
        }

        DS3.InputSingleLine {
            id: dnsField

            visible: device.obj_type != "46"

            atomInput {
                label: tr.dns
                text: device.eth_dns || tr.no_data_full
                readOnly: true
                validator: RegExpValidator { regExp: ui.regexes.ip }
                required: false
            }
            rightIcon.source: ''
        }
    }

    DS3.Spacing {
        height: mac.visible ? 24 : 0
    }

    DS3.SettingsContainer {
        id: mac

        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        visible: !! device.eth_mac

        DS3.InfoTitleButtonIcon {
            textOnCopy: tr.mac_add_copied
            atomTitle {
                title: tr.mac_address
                subtitle: device.eth_mac
            }
            leftIcon.source: "qrc:/resources/images/Athena/common_icons/Hardware-M"
            buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"

            onRightControlClicked: {
                util.set_clipboard_text(device.eth_mac)
            }
        }
    }
}