import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Parts.DeviceSettings {
    Parts.CommonSettings {
        id: commonSettings

        property var savedButtonMode: null
        property var savedBrightness: null
        property var savedFalsePressFilter: null

        Component.onCompleted: {
            savedButtonMode = device.button_mode - 1
            savedFalsePressFilter = device.false_press_filter - 1
            savedBrightness = Math.log2(device.brightness)
        }

        settingsForChangesChecker: [
            buttonModeCombobox.currentIndex,
            brightnessCombobox.currentIndex,
            alarmTypeCombobox.currentIndex,
            falsePressFilterCombobox.currentIndex,
            ifPanic.checked,
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "button_mode": buttonModeCombobox.currentIndex + 1,
                "brightness": brightnessCombobox.currentIndex == 2 ? 4 : brightnessCombobox.currentIndex + 1,
                "false_press_filter": falsePressFilterCombobox.currentIndex + 1,
                "siren_triggers": ifPanic.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (device.custom_alarm_available && buttonModeCombobox.currentIndex == 0) {
                settings["custom_alarm_type"] = alarmTypeCombobox.currentIndex < 5 ?
                    alarmTypeCombobox.currentIndex + 1 :
                    alarmTypeCombobox.currentIndex + 2
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Connections {
            target: app

            onActionSuccess: {
                if (
                    (falsePressFilterCombobox.currentIndex != savedFalsePressFilter)
                    || (brightnessCombobox.currentIndex != savedBrightness)
                    || (buttonModeCombobox.currentIndex != savedButtonMode)
                ) {
                    application.informationPopup({
                        0: tr.press_button_apply_settings,
                        1: tr.long_press_button_apply_settings,
                        2: tr.double_press_button_apply_setting
                    }[savedFalsePressFilter])
                }
            }
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.ButtonModeCombobox { id: buttonModeCombobox }
            Settings.AlarmTypeCombobox { id: alarmTypeCombobox }
            Settings.BrightnessCombobox { id: brightnessCombobox }
            Settings.FalsePressFilter {
                id: falsePressFilterCombobox

                visible: buttonModeCombobox.currentIndex != 1
            }
        }

        DS3.Spacing {
            height: 24

            visible: ifPanic.visible
        }

        Settings.AlertWithSiren {
            visible: ifPanic.visible
        }
        DS3.SettingsContainer {
            enabled: devEnable

            Settings.IfPanic {
                id: ifPanic

                title: tr.if_button_is_pressed
                visible: buttonModeCombobox.currentIndex == 0
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Parts.ScenariosNav {
                enabled: devEnable

                onEntered: {
                    saveButtonClickCallback(false)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}
