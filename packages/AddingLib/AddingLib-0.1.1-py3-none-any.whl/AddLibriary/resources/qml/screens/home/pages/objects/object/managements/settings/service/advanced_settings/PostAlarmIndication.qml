import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: postAlaramIndicatorSettings

    property var verifying: management.filtered_devices_for_post_alarm_indication.confirming().sort()
    property var sideMargin: 24

    Connections {
        target: app

        property string loaderSource: {
            if (serviceSettings.isWizard) {
                if (hub.hub_type == "YAVIR_PLUS") {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml"
                } else {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/RestoreAfterAlarm.qml"
                }
            } else {
                return ""
            }
        }

        onAltActionSuccess: {
            advancedSettingsLoader.setSource(loaderSource)
        }
    }

    Component.onCompleted: {
        if (serviceSettings.isWizard && lastScreen == 3) {
            confirmedAlarmSwitch.checked = true
            unconfirmedAlarmSwitch.checked = true
            tamperOpeningSwitch.checked = true
            lastScreen += 1
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            hubTamperSwitch.checked,
            appAlarmButtonSwitch.checked,
            confirmedAlarmSwitch.checked,
            unconfirmedAlarmSwitch.checked,
            tamperOpeningSwitch.checked,
            postAlaramIndicatorSettings.verifying,
        ]
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    Loader {
        id: selectDeviceLoader

        anchors.fill: parent
        source: ""
        z: 3
    }

    DS3.NavBarModal {
        id: postAlaramIndicatorBar

        headerText: tr.sirens
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/DevicesAutoBypass.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: postAlaramIndicatorBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: tr.alert_with_a_siren
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: switchesGroup.visible
        }

        DS3.Spacing {
            height: switchesGroup.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            id: switchesGroup

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: !serviceSettings.isWizard

            DS3.SettingsSwitch {
                id: hubTamperSwitch

                enabled: devEnable
                title: tr.if_lid_is_open_hub_or_detector
                checked: hub.panic_siren_on_any_tamper
            }

            DS3.SettingsSwitch {
                id: appAlarmButtonSwitch

                enabled: devEnable
                title: tr.if_panic_button_is_pressed_app
                checked: hub.panic_siren_on_panic_button
            }
        }

        DS3.Spacing {
            height: switchesGroup.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.post_alarm_indication_settings
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100
        }

        DS3.Spacing {
            height: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100 ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100

            DS3.SettingsSwitch {
                id: confirmedAlarmSwitch

                enabled: devEnable
                title: tr.confirmed_alarm
                checked: hub.postAlarmIndicationRule.includes("CONFIRMED_ALARM")
            }

            DS3.SettingsSwitch {
                id: unconfirmedAlarmSwitch

                enabled: devEnable
                title: tr.unconfirmed_alarm
                checked: hub.postAlarmIndicationRule.includes("UNCONFIRMED_ALARM")
            }

            DS3.SettingsSwitch {
                id: tamperOpeningSwitch

                enabled: devEnable
                title: tr.tamper_for_post_alarm
                checked: hub.postAlarmIndicationRule.includes("TEMPER_ALARM")
            }
        }

        DS3.Spacing {
            height: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100 ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.post_alarm_indication_tip
            color: ui.ds3.figure.secondary
            visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100
        }

        DS3.Spacing {
            height: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100 ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100

            DS3.SettingsNavigationTitlePrimary {
                id: postAlarmIndication

                title: tr.select_devices
                subtitle: {
                    let verifyingDevices = postAlaramIndicatorSettings.verifying
                    let count = 0
                    for (var i = 0; i < verifyingDevices.length; i++) {
                        if (verifyingDevices[i][2] == true) {
                            count += 1
                        }
                    }
                    return count ? count : ""
                }

                onEntered: {
                    let data = {
                        "verifying": postAlaramIndicatorSettings.verifying,
                        "devices_model": management.filtered_siren_like_devices_for_post_alarm_indication,
                        "empty_text": tr.no_sirens_for_post_alarm_indication,
                        "parentRect": postAlaramIndicatorSettings
                    };
                    selectDeviceLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SelectDevices.qml", data)
                }
            }
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        hasStepper: serviceSettings.isWizard
        stepAmount: hub.hub_type == "YAVIR_PLUS" ? 7 : 10
        currentStep: 4

        button.onClicked: {
            Popups.please_wait_popup()

            function getResultSelectDevices(arr1, arr2) {
                let result = arr1.filter((elem) => arr2.every((sub) => (elem[1] != sub[1] || elem[2] != sub[2])))
                return result
            }

            var data = []

            var settings = {"type": "21", "id": hub.hub_id}

            // Old settings
            settings["panic_siren_on_any_tamper"] = hubTamperSwitch.checked
            settings["panic_siren_on_panic_button"] = appAlarmButtonSwitch.checked

            let postAlarmIndicationRule = []

            if (unconfirmedAlarmSwitch.checked) postAlarmIndicationRule.push("UNCONFIRMED_ALARM")
            if (confirmedAlarmSwitch.checked) postAlarmIndicationRule.push("CONFIRMED_ALARM")
            if (tamperOpeningSwitch.checked) postAlarmIndicationRule.push("TEMPER_ALARM")

            settings["postAlarmIndicationRule"] = postAlarmIndicationRule

            data.push(settings)

            // save indication devices

            var selectedDevices = getResultSelectDevices(postAlaramIndicatorSettings.verifying, management.filtered_devices_for_post_alarm_indication.confirming())

            for (let dev of selectedDevices) {
                let device_info = {}

                device_info["type"] = dev[0]
                device_info["id"] = dev[1]
                device_info["post_alarm_indication_enabled"] = dev[2]

                data.push(device_info)
            }

            app.hub_management_module.update_objects_settings(data, {"emit_alt_signal": true})
        }
    }
}
