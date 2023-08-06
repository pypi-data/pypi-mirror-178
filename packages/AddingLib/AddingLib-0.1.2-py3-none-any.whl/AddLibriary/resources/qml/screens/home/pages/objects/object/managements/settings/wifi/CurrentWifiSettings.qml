import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {

    property var wifis: null
    property var devEnable: true
    property var sideMargin: 24

    Connections {
        target: app.hub_management_module

        onForgetWifiSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/WifiSettings.qml", {"wifis": wifis})
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            wifiComboBox.currentIndex,
            ipAddressField.atomInput.text,
            maskField.atomInput.text,
            routerField.atomInput.text,
            dnsField.atomInput.text
        ]
    }

    DS3.NavBarModal {
        id: networkSettingsBar

        headerText: tr.network_settings
        showBackArrow: true
        isRound: false
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/WifiSettings.qml", {"wifis": wifis})
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: networkSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: wifiComboBox

                property int current: !hub.wifi_dhcp

                model: ["DHCP", tr.static]
                atomTitle.title: "Wi-Fi"
                enabled: devEnable
                currentIndex: current

                onCurrentIndexChanged: {
                    wifiComboBox.current = currentIndex
                    ipAddressField.atomInput.text = hub.wifi_ip
                    maskField.atomInput.text = hub.wifi_mask
                    routerField.atomInput.text = hub.wifi_gate
                    dnsField.atomInput.text = hub.wifi_dns
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: ipAddressField

                enabled: (wifiComboBox.current == 1) && devEnable
                atomInput {
                    label: tr.ip_address
                    text: hub.wifi_ip
                    placeholderText: "192.168.0.100"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: maskField

                enabled: (wifiComboBox.current == 1) && devEnable
                atomInput {
                    label: tr.subnet_mask
                    text: hub.wifi_mask
                    placeholderText: "255.255.255.0"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: routerField

                enabled: (wifiComboBox.current == 1) && devEnable
                atomInput {
                    label: tr.gateway
                    text: hub.wifi_gate
                    placeholderText: "192.168.0.1"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.InputSingleLine {
                id: dnsField

                enabled: (wifiComboBox.current == 1) && devEnable
                atomInput {
                    label: "DNS"
                    text: hub.wifi_dns
                    placeholderText: "192.168.0.1"
                    validator: RegExpValidator { regExp: ui.regexes.ip }
                }
            }

            DS3.ButtonRow {
                id: forget

                enabled: devEnable
                text: tr.forget_this_network

                onClicked: {
                    Popups.please_wait_popup()
                    app.hub_management_module.forget_wifi_network()
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
            function rollback() {
                ipAddressField.atomInput.text = hub.wifi_ip
                maskField.atomInput.text = hub.wifi_mask
                routerField.atomInput.text = hub.wifi_gate
                dnsField.atomInput.text = hub.wifi_dns
            }

           if (!ipAddressField.isValid || !maskField.isValid || !dnsField.isValid || !routerField.isValid) {
                Popups.popupByPath(
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
            settings["dhcp"] = wifiComboBox.current == 0
            settings["wifi_ip"] = ipAddressField.atomInput.text
            settings["wifi_mask"] = maskField.atomInput.text
            settings["wifi_gate"] = routerField.atomInput.text
            settings["wifi_dns"] = dnsField.atomInput.text

            Popups.waitPopup(app.actionSuccess, changesChecker.changeInitialValues())
            app.hub_management_module.save_hub_wifi_settings(settings)
        }
    }
}