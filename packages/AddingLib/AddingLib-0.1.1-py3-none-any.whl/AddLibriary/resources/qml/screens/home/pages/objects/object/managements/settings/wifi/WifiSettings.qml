import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: rect

    property var wifis: null
    property var devEnable: true
    property var sideMargin: 24

    Component.onCompleted: {
        if (hub.wifi_enabled) {
            Popups.please_wait_popup()
            app.hub_management_module.get_wifi_networks()
        }
    }

    Connections {
        target: app.hub_management_module

        onWifiNetworks: {
            wifiList.model = wifiLists
            wifis = wifiLists
        }

    }

    Connections {
        target: app

        onHubWifiActionSuccess: {
            changesChecker.changeInitialValues()
            if (wifiEnabledSwitch.checked) {
                Popups.please_wait_popup()
            }
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            wifiEnabledSwitch.checked
        ]
    }

    DS3.NavBarModal {
        id: wifiSettingsBar

        headerText: "Wi-Fi"
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: contentView

        width: parent.width

        anchors {
            fill: undefined
            top: wifiSettingsBar.bottom
            bottom: saveButton.top
        }

        padding: 24

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: wifiEnabledSwitch

                title: "Wi-Fi"
                checked: hub.wifi_enabled
            }
        }

        DS3.Spacing {
            height: 24

            visible: activeNetwork.visible
        }

        DS3.TitleSection {
            text: tr.active_network
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
            visible: activeNetwork.visible
        }

        DS3.SettingsContainer {
            DS3.SettingsWiFi {
                id: activeNetwork

                visible: {
                    if (!hub.wifi_ssid) return false
                    return wifiEnabledSwitch.checked
                }
                title: hub.wifi_ssid
                wifiLevel: hub.wifi_signal_strength
                isLocked: ["NONE", "WEP"].includes(hub.wifi_security_protocol)
                onEntered: loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/CurrentWifiSettings.qml", {"wifis": wifis})
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            text: tr.available_networks
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
            visible: wifiEnabledSwitch.checked
        }

        DS3.Spacing {
            height: wifiEnabledSwitch.checked ? 4 : 0
        }

        DS3.SettingsContainer {
            ListView {
                id: wifiList

                width: parent.width
                height: childrenRect.height

                visible: wifiEnabledSwitch.checked
                enabled: devEnable
                clip: true
                spacing: 1

                interactive: false
                boundsBehavior: Flickable.StopAtBounds

                model: wifis

                delegate: DS3.SettingsWiFi {
                    title: modelData.ssid_name
                    wifiLevel: modelData.signal_level
                    isLocked: [3, 4, 5].includes(modelData.enc_type)
                    onEntered: {
                        if (modelData.enc_type == 0 || modelData.enc_type == 1) {
                            Popups.please_wait_popup()
                            app.hub_management_module.select_wifi_network(modelData.ssid_name, "", 1)
                            return
                        }
                        Popups.popupByPath(
                            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                            {
                                title: tr.information,
                                text: util.insert(tr.enter_password_for_connect_hub_to_a_wifi_network, [hub.name, modelData.ssid_name]),
                                firstButtonText: tr.connect,
                                secondButtonText: tr.cancel,
                                inputValueHandler: (wifiPassword) => {
                                    Popups.please_wait_popup()
                                    app.hub_management_module.select_wifi_network(modelData.ssid_name, wifiPassword, modelData.enc_type)
                                },
                                isInput: true,
                                "inputField.isPasswordField": true,
                                isVertical: true
                            })
                    }
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                title: tr.other_network
                visible: wifiEnabledSwitch.checked

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/SelectWifiNetworkAdvancedPopup.qml")
                }
            }
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            wifiEnabledSwitch.checked ? app.hub_management_module.turn_wifi(1) : app.hub_management_module.turn_wifi(2)
            Popups.please_wait_popup()
        }
    }
}


