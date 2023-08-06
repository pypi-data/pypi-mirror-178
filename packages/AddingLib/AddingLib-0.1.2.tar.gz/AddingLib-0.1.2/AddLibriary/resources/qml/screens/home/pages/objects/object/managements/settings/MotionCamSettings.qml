import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            partialArm.checked,
            lightIndication.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            motionSensitivityCombobox.currentIndex,
            alwaysActive.checked,
            imageResolutionCombobox.currentIndex,
            numberPhotosCombobox.currentIndex,
            numberPhotosOnDemandCombobox.currentIndex,
            numberAlarmsWithPhotoCombobox.currentIndex,
            ifMotionSensor.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": lightIndication.checked ? "STANDARD" : "DONT_BLINK_ON_ALARM",
                },
                "sensitivity": motionSensitivityCombobox.currentIndex,
                "always_active": alwaysActive.checked,
                "image_resolution": parseInt(imageResolutionCombobox.currentIndex) + 1,
                "photos_per_alarm": parseInt(numberPhotosCombobox.currentIndex),
                "siren_triggers": ifMotionSensor.checked ? [1] : [],
                "photos_on_demand": numberPhotosOnDemandCombobox.visible ?
                                        parseInt(numberPhotosOnDemandCombobox.currentIndex) + 1 :
                                        parseInt(numberPhotosCombobox.currentIndex),
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.is_arm_alarm_delays_available) {
                settings["common_part"]["alarm_delay_seconds"] = alarmDelaySeconds.value
                settings["common_part"]["arm_delay_seconds"] = armDelaySeconds.value
            }

            if (hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100) {
                settings["common_part"]["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked
            }

            if (hub.firmware_version_dec >= 211100) {
                settings["common_part"]["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                settings["common_part"]["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value
            }

            if (numberAlarmsWithPhotoCombobox.visible) {
                if (numberAlarmsWithPhotoCombobox.currentIndex == 10) {
                    settings["alarm_with_photos_limit_per_arming_session"] = 0
                } else {
                    settings["alarm_with_photos_limit_per_arming_session"] = parseInt(numberAlarmsWithPhotoCombobox.currentIndex) + 1
                }
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
                Settings.ArmDelaySeconds { id: armDelaySeconds }
                Settings.PartialArm { id: partialArm }
                Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
                Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }
                Settings.LightIndication { id: lightIndication }
                Settings.MotionSensitivityCombobox { id: motionSensitivityCombobox }

                DS3.SettingsPickerTitleSecondary {
                    id: imageResolutionCombobox

                    property bool isPopupActivated: false

                    onActivated: {
                        update(index)
                    }

                    Component.onCompleted: {
                        update(currentIndex)
                        isPopupActivated = true
                    }

                    onCurrentIndexChanged: {
                        if (currentIndex > 1 && imageResolutionCombobox.isPopupActivated) {
                            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                title: tr.information,
                                text: tr.image_resolution_warning,
                            })
                        }
                    }

                    function update(index) {
                        var prev_index = numberPhotosCombobox.currentIndex
                        var prev_index_pod = numberPhotosOnDemandCombobox.currentIndex
                        // update models
                        if (index == 2) {  // high-res
                            numberPhotosCombobox.model = [tr.no_photo, 1, 2, 3]
                            numberPhotosOnDemandCombobox.model = [1, 2, 3]
                        } else {
                            numberPhotosCombobox.model = [tr.no_photo, 1, 2, 3, 4, 5]
                            numberPhotosOnDemandCombobox.model = [1, 2, 3, 4, 5]
                        }
                        // update current index for numberPhotosCombobox
                        if (numberPhotosCombobox.model.length <= prev_index) {
                            numberPhotosCombobox.currentIndex = numberPhotosCombobox.model.length - 1
                        } else {
                            numberPhotosCombobox.currentIndex = prev_index
                        }
                        // update current index for numberPhotosOnDemandCombobox
                        if (numberPhotosOnDemandCombobox.model.length <= prev_index_pod) {
                            numberPhotosOnDemandCombobox.currentIndex = numberPhotosOnDemandCombobox.model.length - 1
                        } else {
                            numberPhotosOnDemandCombobox.currentIndex = prev_index_pod
                        }
                    }

                    atomTitle.title: tr.image_resolution
                    model: ["160x120", "320x240", "640x480"]
                    currentIndex: device.image_resolution - 1
                }
                Settings.NumberPhotosCombobox { id: numberPhotosCombobox }
                Settings.NumberAlarmsWithPhotoCombobox { id: numberAlarmsWithPhotoCombobox }
                Settings.NumberPhODCombobox { id: numberPhotosOnDemandCombobox }
                Settings.AlwaysActive { id: alwaysActive }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.TitleSection {
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.alert_with_a_siren
            }

            DS3.SettingsContainer {
                Settings.IfMotionSensor { id: ifMotionSensor }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Parts.ScenariosNav {
                    id: scenario

                    visible: {
                        if (!hub.is_photo_on_demand_compliant) return false
                        if (device.subtype == 'NO_SUBTYPE' && !hub.access_to_slow_pod_allowed) return false
                        if (appUser.company_id != "") return true
                        if (!hub.current_user.scenario_edit_access) return false
                        if (["MASTER", "PRO"].includes(hub.current_user.hub_role)) return true
                        return device.access_to_pod_allowed
                    }

                    onEntered: {
                        if (!deviceName.atomInput.text.trim()) {
                            Popups.text_popup(tr.information, tr.the_name_field_cannot_be_blank)
                            return
                        }

                        var settings = {
                            "common_part": {
                                "name": {"name": deviceName.atomInput.text.trim()},
                                "night_mode_arm": partialArm.checked,
                                "indicator_light_mode": lightIndication.checked ? "STANDARD" : "DONT_BLINK_ON_ALARM",
                            },
                            "sensitivity": motionSensitivityCombobox.currentIndex,
                            "always_active": alwaysActive.checked,
                            "image_resolution": parseInt(imageResolutionCombobox.currentIndex) + 1,
                            "photos_per_alarm": parseInt(numberPhotosCombobox.currentIndex),
                            "siren_triggers": ifMotionSensor.checked ? [1] : [],
                            "photos_on_demand": numberPhotosOnDemandCombobox.visible ?
                                                    parseInt(numberPhotosOnDemandCombobox.currentIndex) + 1 :
                                                    parseInt(numberPhotosCombobox.currentIndex),
                            "_params": {
                                "alt_action_success": true,
                            },
                        }

                        if (roomsCombobox.currentIndex >= 0) {
                            var room = rooms.get_room(roomsCombobox.currentIndex)
                            settings["common_part"]["room_id"] = room.id
                        }

                        if (hub.is_arm_alarm_delays_available) {
                            settings["common_part"]["alarm_delay_seconds"] = alarmDelaySeconds.value
                            settings["common_part"]["arm_delay_seconds"] = armDelaySeconds.value
                        }

                        if (hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100) {
                            settings["common_part"]["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked
                        }

                        if (hub.firmware_version_dec >= 211100) {
                            settings["common_part"]["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                            settings["common_part"]["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value
                        }

                        if (numberAlarmsWithPhotoCombobox.visible) {
                            if (numberAlarmsWithPhotoCombobox.currentIndex == 10) {
                                settings["alarm_with_photos_limit_per_arming_session"] = 0
                            } else {
                                settings["alarm_with_photos_limit_per_arming_session"] = parseInt(numberAlarmsWithPhotoCombobox.currentIndex) + 1
                            }
                        }

                        app.hub_management_module.apply_update(management, device, settings)
                    }
                }
            }

            DS3.Spacing {
                height: 24

                visible: scenario.visible
            }
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {}
                Parts.TestSignalDataLevelNav {}
                Parts.TestZoneNav {}
                Parts.TestSignalLostNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}