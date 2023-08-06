import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: simCardSettings

    property var sim: null
    property var change_balance_number: false
    property var devEnable: true
    property var sideMargin: 24

    signal reBalanceAnswer(string balanceText)

    Component.onCompleted: {
        app.hub_management_module.balanceAnswer.connect(reBalanceAnswer)
    }

    Connections {
        target: app

        onAltActionSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/gsm/GSMSettings.qml")
        }
    }

    Connections {
        target: simCardSettings

        onReBalanceAnswer: {
            balanceLabel.text = balanceText
        }
    }

    Connections {
        target: app.hub_management_module

        onBalanceRequest: {
            app.hub_management_module.gsm_get_sim_card_balance(hub.id, sim)
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            apnField.atomInput.text,
            apnUserField.atomInput.text,
            passwordField.atomInput.text,
        ]
    }

    DS3.NavBarModal {
        id: gsmSettingsBar

        headerText: sim ? "SIM2" : "SIM1"
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/gsm/GSMSettings.qml")
        }
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
        enabled: devEnable

        DS3.SettingsContainer {
            width: parent.width

            DS3.InputSingleLine {
                id: apnField

                atomInput {
                    label: tr.apn
                    text: sim ? hub.gsm_apn_2 : hub.gsm_apn
                    required: false
                    maxByteLength: 63
                }
            }

            DS3.InputSingleLine {
                id: apnUserField

                atomInput {
                    label: tr.username
                    text: sim ? hub.gsm_apn_username_2 : hub.gsm_apn_username
                    required: false
                    maxByteLength: 24
                }
            }

            DS3.InputPassword {
                id: passwordField

                atomInput {
                    label: tr.password
                    text: sim ? hub.gsm_apn_password_2 : hub.gsm_apn_password
                    required: false
                    maxByteLength: 24
                }
            }
        }

        DS3.Spacing {
            height: 28
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.mobile_traffic
            visible: hub.firmware_version_dec >= 207000
        }

        DS3.Spacing {
            height: incomingInfo.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            visible: hub.firmware_version_dec >= 207000

            DS3.InfoTitle {
                id: incomingInfo

                width: parent.width

                Connections {
                    target: hub

                    onDataChanged: {
                        if (!sim) {
                            incomingInfo.atomTitle.subtitle = hub.gsm_traffic_rx + " KB"
                            return
                        }
                        incomingInfo.atomTitle.subtitle = hub.gsm_traffic_rx_2 + " KB"
                    }
                }

                atomTitle {
                    title: tr.incoming
                    subtitle: {
                        if (!sim) return hub.gsm_traffic_rx + " KB"
                        return hub.gsm_traffic_rx_2 + " KB"
                    }
                }
            }

            DS3.InfoTitle {
                id: outcomingInfo

                Connections {
                    target: hub

                    onDataChanged: {
                        if (!sim) {
                            outcomingInfo.atomTitle.subtitle = hub.gsm_traffic_tx + " KB"
                            return
                        }
                        outcomingInfo.atomTitle.subtitle = hub.gsm_traffic_tx_2 + " KB"
                    }
                }

                atomTitle{
                    title: tr.outgoing
                    subtitle: {
                        if (!sim) return hub.gsm_traffic_tx + " KB"
                        return hub.gsm_traffic_tx_2 + " KB"
                    }
                }
            }

            DS3.ButtonRow {
                text: tr.reset_statistics

                onClicked: {
                    Popups.please_wait_popup()
                    app.hub_management_module.gsm_reset_statistic(hub.id, sim)
                }
            }
        }

        DS3.Spacing {
            height: incomingInfo.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: hub.firmware_version_dec >= 207000
            text: {
                var template = tr.last_reset + ": "
                var dateValue = ""
                if (!sim) {
                    dateValue = hub.last_traffic_reset_linux_time_SIM1
                } else {
                    dateValue = hub.last_traffic_reset_linux_time_SIM2
                }
                if (dateValue == "never") dateValue = tr.never
                return template + dateValue
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            text: tr.check_balance
            visible: balanceNumberField.visible
        }

        DS3.Spacing {
            height: balanceNumberField.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.InputSingleLine {
                id: balanceNumberField

                atomInput {
                    label: tr.ussd
                    maximumLength: 20
                    placeholderText: sim == 1 ? hub.gsm_balance_number_2 : hub.gsm_balance_number
                    validator: RegExpValidator { regExp: /^[0-9\*\#]+$/ }
                    required: false
                }
                visible: hub.firmware_version_dec >= 207000

                Connections {
                    target: balanceNumberField.atomInput

                    onTextChanged: {
                        change_balance_number = true
                    }
                }
            }

            DS3.ButtonRow {
                text: tr.check_balance
                enabled: balanceNumberField.atomInput.text && devEnable

                onClicked: {
                    var numberSim = sim == 1 ? hub.gsm_balance_number_2 : hub.gsm_balance_number

                    Popups.please_wait_popup()

                    if (numberSim != balanceNumberField.atomInput.text) {
                        var settings = {}
                        settings["gsm_sim_card_index"] = sim
                        settings["gsm_balance_number"] = balanceNumberField.atomInput.text

                        app.hub_management_module.gsm_update_sim_card_balance_number_with_check(hub.id, settings)
                    } else {
                        app.hub_management_module.gsm_get_sim_card_balance(hub.id, sim)
                    }
                }
            }
        }

        DS3.Spacing {
            height: balanceNumberField.visible ? 4 : 0
        }

        DS3.Text {
            id: balanceLabel

            width: parent.width

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: balanceNumberField.visible
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
            var settings = {}
            settings["gsm_apn"] = apnField.atomInput.text
            settings["gsm_apn_username"] = apnUserField.atomInput.text
            settings["gsm_apn_password"] = passwordField.atomInput.text
            settings["gsm_sim_card_index"] = sim
            settings["gsm_balance_number"] = balanceNumberField.atomInput.text

            Popups.please_wait_popup(tr.request_send, 300)

            if (change_balance_number) {
                app.hub_management_module.gsm_update_sim_card_balance_number(hub.id, settings)
                change_balance_number = false
            }
            else {
                app.hub_management_module.gsm_update_sim_card_settings(hub.id, settings)
            }
        }
    }
}


