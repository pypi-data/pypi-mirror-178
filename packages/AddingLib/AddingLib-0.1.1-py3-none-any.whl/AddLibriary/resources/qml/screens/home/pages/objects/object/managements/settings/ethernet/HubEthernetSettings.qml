import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: ethernetSettings

    property var devEnable: true
    property var sideMargin: 24
    property bool isHubDeviceNetworkCommandSupported: {
        if (hub.hub_type == 'HUB') return false
        return hub.firmware_version_dec >= 213000 || (hub.firmware_version_dec >= 212128 && hub.firmware_version_dec <= 212175 )
    }

    function rollback() {
        ethernetComboBox.currentIndex = hub.eth_dhcp ? 0 : 1
        ipAddressField.atomInput.text = hub.eth_ip
        ipAddressField.checkValid()
        maskField.atomInput.text = hub.eth_mask
        maskField.checkValid()
        routerField.atomInput.text = hub.eth_gate
        routerField.checkValid()
        dnsField.atomInput.text = hub.eth_dns
        dnsField.checkValid()
    }

    Connections {
        target: app

        onDeviceNetworkCommandSuccess: {
            ethernetComboBox.currentIndex = ethernetComboBox.current
            changesChecker.changeInitialValues()
        }

        onActionSuccess: {
            ethernetComboBox.currentIndex = ethernetComboBox.current
            changesChecker.changeInitialValues()
        }

        onSetEthernetFailed: {
            Popups.popupByPath(
                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                {
                    title: tr.error,
                    text: tr.failed_to_disable_current_communication_channel0,
                    firstButtonText: tr.i_will_check,
                }
            )
        }

        onDeviceNetworkCommandError: {
            Popups.popupByPath(
                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                {
                    title: tr.error,
                    text: tr.Netw_set_fail0,
                    firstButtonText: tr.i_will_check,
                    secondButtonText: tr.rollback_changes,
                    isVertical: true,
                    secondButtonCallback: rollback
                }
           )
       }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            isHubDeviceNetworkCommandSupported ? null : connectedViaEthernet.checked,
            ethernetComboBox.current,
            ipAddressField.atomInput.text,
            maskField.atomInput.text,
            routerField.atomInput.text,
            dnsField.atomInput.text
        ]
    }

    DS3.NavBarModal {
        id: ethernetSettingsBar

        headerText: tr.ethernet_settings
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: ethernetSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: connectedViaEthernet

                title: tr.connection_via_ethernet
                checked: hub.eth_enabled
                enabled: devEnable
                cancelBinding: false

                onSwitched: () => {    // new endpoint for new hubs. Coming soon
                    if (isHubDeviceNetworkCommandSupported) {
                        settings["channel"] = "ETHERNET"
                        settings["state"] = connectedViaEthernet.checked ? "OFF" : "ON" // it reversed, cause we change it's state
                        settings["command_type"] = "update_device_network_channel_state"
                        app.hub_management_module.device_network_command(hub, settings)
                        Popups.please_wait_popup(tr.request_send, 180)
                    } else {
                        checked = !checked
                    }
                }
           }
       }

       DS3.Spacing {
           height: sideMargin
       }

        DS3.SettingsContainer {
            id: combobox

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: connectedViaEthernet.checked && device.eth_enabled

            DS3.SettingsPickerTitleSecondary {
                id: ethernetComboBox

                property int current: device.eth_dhcp ? 0 : 1

                model: [tr.dhcp, tr.static]
                atomTitle.title: tr.connection_type_ethernet
                enabled: devEnable
                currentIndex: current

                onCurrentIndexChanged: {
                    ethernetComboBox.current = currentIndex
                    ipAddressField.atomInput.text = hub.eth_ip
                    maskField.atomInput.text = hub.eth_mask
                    routerField.atomInput.text = hub.eth_gate
                    dnsField.atomInput.text = hub.eth_dns
                }
            }
        }

        DS3.Spacing {
            height: sideMargin
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: ethernetComboBox.current == 1  && connectedViaEthernet.checked

            DS3.InputSingleLine {
                id: ipAddressField

                width: parent.width

                atomInput {
                    label: tr.ip_address
                    text: hub.eth_ip
                    placeholderText: "0.0.0.0"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: maskField

                width: parent.width

                atomInput {
                    label: tr.subnet_mask
                    text: hub.eth_mask
                    placeholderText: "255.255.255.0"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: routerField

                width: parent.width

                atomInput {
                    label: tr.gateway
                    text: hub.eth_gate
                    placeholderText: "192.168.0.1"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: dnsField

                width: parent.width

                atomInput {
                    label: "DNS"
                    text: hub.eth_dns
                    placeholderText: "192.168.0.1"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            if (!ipAddressField.isValid || !maskField.isValid || !dnsField.isValid || !routerField.isValid) {
                Popups.popupByPath(
                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.Netw_set_fail0,
                        text: tr.check_data_correct_or_rollback,
                        isVertical: true,
                        firstButtonText: tr.i_will_check,
                        secondButtonText: tr.rollback_changes,
                        secondButtonCallback: ethernetSettings.rollback,
                        isSecondButtonRed: true,
                    }
                )
                return
            }
            var settings = {}
             // new endpoint for new hubs
            if (isHubDeviceNetworkCommandSupported) {
                settings["dhcp"] = ethernetComboBox.current == 0
                settings["eth_ip"] = ipAddressField.atomInput.text
                settings["eth_mask"] = maskField.atomInput.text
                settings["eth_gate"] = routerField.atomInput.text
                settings["dns"] = dnsField.atomInput.text
                settings["command_type"] = "update_device_ethernet_settings"
                app.hub_management_module.device_network_command(device, settings)
                Popups.please_wait_popup(tr.updating_ethernet_settings, 180)
            } else {
                settings["eth_enabled"] = connectedViaEthernet.checked
                settings["dhcp"] = ethernetComboBox.current == 0
                settings["eth_ip"] = ipAddressField.atomInput.text
                settings["eth_mask"] = maskField.atomInput.text
                settings["eth_gate"] = routerField.atomInput.text
                settings["eth_dns"] = dnsField.atomInput.text
                app.hub_management_module.update_ethernet_settings(hub.id, settings)
                Popups.please_wait_popup(tr.updating_ethernet_settings, 180)
            }
       }
   }
}