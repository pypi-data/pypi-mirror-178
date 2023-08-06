import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    property var sideMargin: 24

    Connections {
        target: app

        onActionSuccess: {
            advancedSettingsLoader.setSource("")
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            let changes_list = [syncFireProtectAlarmField.checked]
            if (ignoreFirstAlarmSwitch.visible) changes_list.push(ignoreFirstAlarmSwitch.checked)
            if (syncFireProtectAlarmField.checked) {
                changes_list.push(delayBeforeAlarm.checked, interconnectMode.checked)
                if (delayBeforeAlarm.checked) {
                    changes_list.push(delayBeforeAlarmSlider.value)
                }
            }
            return changes_list
        }
    }

    DS3.NavBarModal {
        id: fireDetectorsBar

        headerText: tr.fire_detectors
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            advancedSettingsLoader.setSource("")
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: fireDetectorsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: syncFireProtectAlarmField

                enabled: devEnable
                title: tr.interconnected_smoke_alarms
                checked: hub.fire_interconnected
                visible: hub.firmware_version_dec >= 201000
                cancelBinding: false

                onSwitched: () => {
                    if (hub.hub_type == "HUB_2_PLUS" && hub.frame_length > 72) {
                        Popups.enable_interconnect_warning_popup(72)
                        return
                    }
                    if (hub.hub_type != "HUB_2_PLUS" && hub.frame_length > 48) {
                        Popups.enable_interconnect_warning_popup(48)
                        return
                    }
                    checked = !checked
                }
            }
        }

        DS3.Spacing {
            height: syncFireProtectAlarmField.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.interconnected_smoke_alarms_hint
            color: ui.ds3.figure.secondary
            visible: syncFireProtectAlarmField.visible
        }

        DS3.Spacing {
            height: syncFireProtectAlarmField.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: delayBeforeAlarm

                enabled: devEnable
                title: tr.interconnect_delay_activate
                checked: hub.interconnect_delay_timeout
                visible: hub.firmware_version_dec >= 209100 && syncFireProtectAlarmField.checked
            }
        }

        DS3.Spacing {
            height: delayBeforeAlarm.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: delayBeforeAlarmSlider

                enabled: devEnable
                value: hub.interconnect_delay_timeout / 60
                title: tr.interconnect_delay_timer
                from: 1
                to: 5
                stepSize: 1
                suffix: tr.min
                visible: delayBeforeAlarm.visible && delayBeforeAlarm.checked
            }
        }

        DS3.Spacing {
            height: delayBeforeAlarmSlider.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.interconnect_delay_timer_info
            color: ui.ds3.figure.secondary
            visible: delayBeforeAlarmSlider.visible
        }

        DS3.Spacing {
            height: delayBeforeAlarmSlider.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: interconnectMode

                enabled: devEnable
                title: tr.apartment_building
                checked: hub.interconnect_modes.includes(1)
                visible: hub.firmware_version_dec >= 211121 && syncFireProtectAlarmField.checked && hub.groups_enabled
            }
        }

        DS3.Spacing {
            height: interconnectMode.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: {
                var locale = tr.get_locale()
                var link = "https://support.ajax.systems/" + locale + "/residential-fire-alarms/"

                return util.hyperlink(tr.apartment_building_info + "<br/>{0}" + tr.learn_more + "{1}", link)
            }
            color: ui.ds3.figure.secondary
            visible: interconnectMode.visible
        }

        DS3.Spacing {
            height: interconnectMode.visible ? 24 : 0
        }

        DS3.Text {
            id: warningText

            width: parent.width

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            text: tr.jeweller_warning_for_hub_2_plus_delay
            visible: hub.hub_type == "HUB_2_PLUS" && hub.frame_length > 48 && syncFireProtectAlarmField.checked
        }

        DS3.Spacing {
            height: warningText.visible ? 4 : 0
        }

        Column {
            width: parent.width

            visible: hub.firmware_version_dec >= 201000 && (!__fp2_features__ || hub.device_type_counter(["01", "09"]) > 0)

            DS3.SettingsContainer {
                width: parent.width

                anchors.horizontalCenter: parent.horizontalCenter

                DS3.SettingsSwitch {
                    id: ignoreFirstAlarmSwitch

                    enabled: devEnable
                    title: tr.fire_2_alarm
                    checked: hub.hub_fire_double_impulses
                }
            }

            DS3.Spacing {
                height: 4
            }

            DS3.Text {
                width: parent.width

                style: ui.ds3.text.body.MRegular
                text: tr.fire_2_alarm_hint
                color: ui.ds3.figure.secondary
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
        enabled: devEnable && changesChecker.hasChanges

        button.onClicked: {
            var settings = {
                "fire_alarm": {
                    "trigger_on_all_sensors": syncFireProtectAlarmField.checked,
                    "double_impulses": ignoreFirstAlarmSwitch.checked,
                },
                "interconnection": {
                    "interconnect_modes": interconnectMode.checked ? [1] : [],
                },
            }

            if (syncFireProtectAlarmField.checked) {
                settings["interconnection"]["interconnect_delay_timeout"] = 0
                if (delayBeforeAlarm.checked) {
                    settings["interconnection"]["interconnect_delay_timeout"] = delayBeforeAlarmSlider.value * 60
                }
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
