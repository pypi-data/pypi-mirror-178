import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups


DS3Popups.PopupStep {
    id: rex2EthernetSettingsPopupStep

    function rollback() {
        ipAddressField.atomInput.text = device.eth_ip
        ipAddressField.checkValid()
        maskField.atomInput.text = device.eth_mask
        maskField.checkValid()
        routerField.atomInput.text = device.eth_gate
        routerField.checkValid()
        ethernetComboBox.current = device.eth_dhcp ? 0 : 1
        ethernetComboBox.currentIndex = ethernetComboBox.current
    }

    Connections {
        target: hub

        onDataChanged: {
            device.dataChanged()
        }
    }

    Connections {
        target: app

        onDeviceNetworkCommandSuccess: {
            changesChecker.changeInitialValues()
        }

        onDeviceNetworkCommandError: {
            Popups.popupByPath(
                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                {
                    title: tr.Netw_set_fail0,
                    text: tr.Netw_set_fail_rex_descr,
                    firstButtonText: tr.i_will_check,
                    secondButtonText: tr.rollback_changes,
                    isSecondButtonRed: true,
                    isVertical: true,
                    secondButtonCallback: rollback
                }
            )
        }
    }

    height: maxStepHeight

    sidePadding: 24
    title: tr.ethernet_settings

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            ethernetComboBox.current,
            ipAddressField.atomInput.text,
            maskField.atomInput.text,
            routerField.atomInput.text,
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        DS3.SettingsSwitch {
            id: connectedViaEthernet

            onSwitched: () => {

                // LAST CHANNEL CAN NOT BE DROPPED POPUP
                if (connectedViaEthernet.checked && !device.rf_connection_ok) {
                    Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                        {
                            title: tr.failed_to_disable_last_com_channel_ethernet_title,
                            text: tr.failed_to_disable_last_com_channel_ethernet_descr,
                            firstButtonText: tr.i_will_check,
                        }
                    )
                } else {
                    settings["channel"] = "ETHERNET"
                    settings["state"] = connectedViaEthernet.checked ? "OFF" : "ON" // it reversed, cause we change it's state
                    settings["command_type"] = "update_device_network_channel_state"
                    app.hub_management_module.device_network_command(device, settings)
                    Popups.please_wait_popup(tr.request_send, 180)
                }
            }

            title: tr.connection_via_ethernet
            checked: device.eth_enabled
            cancelBinding: false
        }
    }

    DS3.Spacing {
        height: combobox.visible ?  24 : 0
    }

    DS3.SettingsContainer {
        id: combobox

        visible: connectedViaEthernet.checked && device.eth_enabled

        DS3.SettingsPickerTitleSecondary {
            id: ethernetComboBox

            property int current: device.eth_dhcp ? 0 : 1

            model: [tr.dhcp, tr.static]
            atomTitle.title: tr.connection_type_ethernet
            currentIndex: current

            onCurrentIndexChanged: {
                ethernetComboBox.current = currentIndex
                ipAddressField.atomInput.text = device.eth_ip
                maskField.atomInput.text = device.eth_mask
                routerField.atomInput.text = device.eth_gate
            }
        }
    }

    DS3.Spacing {
        height: connecionDetails.visible ? 24 : 0
    }

    DS3.SettingsContainer {
        id: connecionDetails

        visible: connectedViaEthernet.checked && ethernetComboBox.current == 1

        DS3.InputSingleLine {
            id: ipAddressField

            atomInput {
                label: tr.ip_address
                text: device.eth_ip
                placeholderText: "0.0.0.0"
                validator: RegExpValidator { regExp: ui.regexes.ip }
            }
        }

        DS3.InputSingleLine {
            id: maskField

            atomInput {
                label: tr.subnet_mask
                text: device.eth_mask
                placeholderText: "255.255.255.0"
                validator: RegExpValidator { regExp: ui.regexes.ip }
            }
        }

        DS3.InputSingleLine {
            id: routerField

            atomInput {
                label: tr.gateway
                text: device.eth_gate
                placeholderText: "192.168.0.1"
                validator: RegExpValidator { regExp: ui.regexes.ip }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
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

    footer: DS3.ButtonBar {
        id: saveButton

        enabled: device.eth_enabled && changesChecker.hasChanges
        buttonText: tr.save
        hasBackground: true

        button.onClicked: {
            if (!ipAddressField.isValid || !maskField.isValid ||!routerField.isValid) {
                // WRONG INPUT
                var popup = Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.Netw_set_fail0,
                        text: tr.check_data_correct_or_rollback,
                        firstButtonText: tr.i_will_check,
                        secondButtonText: tr.rollback_changes,
                        secondButtonCallback: rollback,
                        isVertical: true,
                        isSecondButtonRed: true,
                    }
                )
            } else {
                // SEND SETTINGS
                var settings = {}
                settings["dhcp"] = ethernetComboBox.current == 0
                settings["eth_ip"] = ipAddressField.atomInput.text
                settings["eth_mask"] = maskField.atomInput.text
                settings["eth_gate"] = routerField.atomInput.text
                settings["command_type"] = "update_device_ethernet_settings"
                app.hub_management_module.device_network_command(device, settings)
                Popups.please_wait_popup(tr.updating_ethernet_settings_rex, 180)
            }
        }
    }
}