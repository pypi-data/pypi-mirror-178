
import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/popups"
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    property var text: null
    property var sideMargin: 24
    property var security_text: tr.open

    Connections {
        target: app.hub_management_module
        onSelectWifiNetworkSuccess: {
            popup.close()
            app.hub_management_module.get_wifi_networks()
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            if (wifiPassword.visible) return [wifiName.atomInput.text, wifiPassword.atomInput.text]
           return [wifiName.atomInput.text]
        }
    }

    DS3.NavBarModal {
        id: wifiNetworlAdvancedBar

        headerText: tr.other_network
        showBackArrow: true
        isRound: false
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/WifiSettings.qml")
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: wifiNetworlAdvancedBar.bottom
            bottom: connectButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: wifiName

                atomInput {
                    label: tr.name
                    placeholderText: tr.network_name
                    validator: RegExpValidator { regExp: ui.regexes.SSID }
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: wifiProtectionVersion

                model: [tr.open, tr.wep, tr.wpa, tr.wpa_2, tr.wpa_wpa2]
                atomTitle.title: tr.security
                currentIndex: 0
            }

            DS3.InputPassword {
                id: wifiPassword

                atomInput.placeholderText: tr.password
                visible: wifiProtectionVersion.currentIndex != 0
            }
        }

       DS3.Spacing {
           height: 24
       }

       DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: wifiComboBox

                property int current: {
                    if (hub.wifi_dhcp) {
                        return 0
                    } else {
                        return 1
                    }
                }

                model: ["DHCP", tr.static]
                atomTitle.title: tr.configure_ipv4
                currentIndex: current

                onCurrentIndexChanged: {
                    wifiComboBox.current = currentIndex
                    ipAddressField.atomInput.text = hub.wifi_ip
                    maskField.atomInput.text = hub.wifi_mask
                    routerField.atomInput.text = hub.wifi_gate
                    dnsField.atomInput.text = hub.wifi_dns
                }
            }

           DS3.InputSingleLine {
               id: ipAddressField

               visible: wifiComboBox.current == 1
               atomInput {
                   label: tr.ip_address
                   text: hub.wifi_ip
                   placeholderText: "192.168.0.100"
                   validator: RegExpValidator { regExp: ui.regexes.ip }
               }
           }

           DS3.InputSingleLine {
               id: maskField

               visible: wifiComboBox.current == 1
               atomInput {
                   label: tr.subnet_mask
                   text: hub.wifi_mask
                   placeholderText: "255.255.255.0"
                   validator: RegExpValidator { regExp: ui.regexes.ip }
               }
           }

           DS3.InputSingleLine {
               id: routerField

               visible: wifiComboBox.current == 1
               atomInput {
                   label: tr.gateway
                   text: hub.wifi_gate
                   placeholderText: "192.168.0.1"
                   validator: RegExpValidator { regExp: ui.regexes.ip }
               }
           }

           DS3.InputSingleLine {
               id: dnsField

               visible: wifiComboBox.current == 1
               atomInput {
                   label: "DNS"
                   text: hub.wifi_dns
                   placeholderText: "192.168.0.1"
                   validator: RegExpValidator { regExp: ui.regexes.ip }
               }
           }
        }
    }

    DS3.ButtonBar {
        id: connectButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.connect
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            function rollback() {
                ipAddressField.atomInput.text = hub.wifi_ip
                maskField.atomInput.text = hub.wifi_mask
                routerField.atomInput.text = hub.wifi_gate
                dnsField.atomInput.text = hub.wifi_dns
            }

            if (!ipAddressField.isValid || !maskField.isValid || !dnsField.isValid || !routerField.isValid) {
                PopupsDesk.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.error,
                        text: tr.OperationError_AXHubNetworkSettingsOperation_0B_05,
                        secondButtonCallback: rollback,
                        firstButtonText: tr.i_will_check,
                        secondButtonText: tr.rollback_changes,
                        isSecondButtonRed: true,
                        isVertical: true
                    })
                return
            }
            var settings = {}
            settings["ssid_name"] = wifiName.atomInput.text
            if (wifiProtectionVersion.subtitle != tr.open) {
                settings["password"] = wifiPassword.atomInput.text
            }
            else{
                settings["password"] = ""
            }
            settings["enc_type"] = wifiProtectionVersion.currentIndex + 1
            settings["dhcp"] = wifiComboBox.current == 0
            settings["wifi_ip"] = ipAddressField.atomInput.text
            settings["wifi_mask"] = maskField.atomInput.text
            settings["wifi_gate"] = routerField.atomInput.text
            settings["wifi_dns"] = dnsField.atomInput.text
            PopupsDesk.please_wait_popup()
            app.hub_management_module.select_wifi_network_advanced(settings)
        }
    }
}