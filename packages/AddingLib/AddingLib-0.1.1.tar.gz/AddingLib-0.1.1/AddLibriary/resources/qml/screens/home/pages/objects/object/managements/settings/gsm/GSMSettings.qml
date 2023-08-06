import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property var devEnable: true
    property var sideMargin: 24

    anchors.fill: parent

    color: ui.ds3.bg.base

    Connections {
        target: app

        onHubGSMActionSuccess: {
            checkGSMChanges.changeInitialValues()
            if (changesChecker.hasChanges) {
                var settings = {
                    "gsm": {
                        "roaming_enabled": roamingSwitch.checked,
                        "virtual_operator_allowed": ignoreErrorsSwitch.checked,
                        "disable_icmp_before_connecting": disableICMPSwitch.checked,
                    },
                }

                Popups.please_wait_popup()
                app.hub_management_module.apply_update(management, hub, settings)
            }
        }

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            roamingSwitch.checked,
            ignoreErrorsSwitch.checked,
            disableICMPSwitch.checked,
        ]
    }

    DS3.ChangesChecker {
        id: checkGSMChanges

        listeningValues: [
            cellularSwitch.checked
        ]
    }

    DS3.NavBarModal {
        id: gsmSettingsBar

        headerText: tr.gsm
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: contentView

        width: parent.width

        anchors {
            fill: undefined
            top: gsmSettingsBar.bottom
            bottom: saveButton.top
        }

        padding: 24

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.modem_settings
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: cellularSwitch

                title: tr.cellular_data
                checked: hub.gsm_gprs_enabled
                enabled: devEnable
            }

            DS3.SettingsSwitch {
                id: roamingSwitch

                title: tr.roaming
                checked: hub.roaming_enabled
                visible: cellularSwitch.checked
            }

            DS3.SettingsSwitch {
                id: ignoreErrorsSwitch

                enabled: devEnable
                title: tr.ignore_network_registration_error
                checked: hub.virtual_operator_allowed
                visible: cellularSwitch.checked
            }

            DS3.SettingsSwitch {
                id: disableICMPSwitch

                enabled: devEnable
                title: tr.disableICMPBeforeConnecting
                checked: hub.disable_icmp_before_connecting
                visible: cellularSwitch.checked
            }
        }

        DS3.Spacing {
            height: 28
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.sim_cards
            visible: cellularSwitch.checked
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            visible: cellularSwitch.checked

            DS3.SettingsTitleSecondaryNavigation {
                title: "SIM 1"
                subtitle: {
                    if (hub.sim_card_1_number.trim()) {
                        return "+" + hub.sim_card_1_number
                    }
                    return tr.unknown_number
                }

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/gsm/SimCardSettings.qml", {"sim": 0})
                }
            }

            DS3.SettingsTitleSecondaryNavigation {
                title: "SIM 2"
                subtitle: {
                    if (hub.sim_card_2_number.trim()) {
                        return "+" + hub.sim_card_2_number
                    }
                    return tr.unknown_number
                }
                visible: hub.hub_type == "HUB_PLUS" || hub.hub_type == "HUB_2" || hub.hub_type == "HUB_2_4G" || hub.hub_type == "HUB_2_PLUS" || hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS" || hub.hub_type == "HUB_FIBRA"

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/gsm/SimCardSettings.qml", {"sim": 1})
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
        enabled: {
            if (checkGSMChanges.hasChanges) return true
            return changesChecker.hasChanges
        }

        button.onClicked: {
            if (checkGSMChanges.hasChanges) {
                Popups.please_wait_popup()
                app.hub_management_module.turn_gsm(cellularSwitch.checked)
                return
            }

            var settings = {
                "gsm": {
                    "roaming_enabled": roamingSwitch.checked,
                    "virtual_operator_allowed": ignoreErrorsSwitch.checked,
                    "disable_icmp_before_connecting": disableICMPSwitch.checked,
                },
            }

            Popups.please_wait_popup(tr.request_send, 300)
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
