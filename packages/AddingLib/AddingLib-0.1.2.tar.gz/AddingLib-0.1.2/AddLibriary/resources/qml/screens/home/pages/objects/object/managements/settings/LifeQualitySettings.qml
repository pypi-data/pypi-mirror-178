import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            co2Indication.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }
            settings["co2_indication"] = co2Indication.checked ? "CO2_INDICATION_ON" : "CO2_INDICATION_OFF"

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                title: tr.notifications

                onEntered: setChild(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/LifeQualityNotifications.qml"
                )
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            isBgTransparent: true
            isCaps: true
            forceTextToLeft: true
            text: tr.air_monitor_settings
        }

        DS3.SettingsContainer {
            width: parent.width

            enabled: devEnable

            Parts.TemperatureRangeNav {}
            Parts.HumidityRangeNav {}
            Parts.CO2LevelNav {}
        }

        DS3.Comment {
            width: parent.width

            text: tr.air_monitor_settings_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            isBgTransparent: true
            isCaps: true
            forceTextToLeft: true
            text: tr.lq_led_indication
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.CO2LEDIndication {
                id: co2Indication
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.blink_co_high_level_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            enabled: devEnable

            Parts.Scenarios2Nav {}
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            enabled: devEnable

            Parts.TestSignalLevelNav {}
            Parts.CO2SensorCalibrationNav {}
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}
