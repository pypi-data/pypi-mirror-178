import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        property var savedBrightness: null

        Component.onCompleted: {
            savedBrightness = Math.log2(device.brightness)
        }

        settingsForChangesChecker: [
            brightnessCombobox.currentIndex,
            ifPanic.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "brightness": brightnessCombobox.currentIndex == 2 ? 4 : brightnessCombobox.currentIndex + 1,
                "siren_triggers": ifPanic.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Connections {
            target: app
            onActionSuccess: {
                if (brightnessCombobox.currentIndex != savedBrightness) {
                    application.informationPopup(tr.press_doublebutton_apply_settings)
                }
            }
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.BrightnessCombobox { id: brightnessCombobox }
        }

        DS3.Spacing {
            height: 24
        }

        Settings.AlertWithSiren {}
        DS3.SettingsContainer {
            enabled: devEnable

            Settings.IfPanic {
                id: ifPanic

                title: tr.if_button_is_pressed
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
