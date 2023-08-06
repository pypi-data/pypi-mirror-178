import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            currentProtectionThreshold.value,
            voltageProtection.checked,
            indicationMode.currentIndex,
            ledBrightness.value,
            channelModeCombobox.currentIndex,
            channelNormalState.currentIndex,
            impulseTimeCombobox.currentIndex
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "type_g": {
                    "indication_mode": indicationMode.currentIndex + 1,
                    "indication_brightness": ledBrightness.value,
                },
                "current_protection_threshold": currentProtectionThreshold.value,
                "voltage_protection_off": !voltageProtection.checked,
                "channel_mode": channelModeCombobox.currentIndex + 1,
                "channel_normal_state": channelNormalState.currentIndex + 1,
                "impulse_duration": impulseTimeCombobox.currentIndex + 1,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.CurrentProtectionThreshold { id: currentProtectionThreshold }
            }

            DS3.Comment {
                id: currentProtectionThresholdComment

                width: parent.width

                text: tr.voltage_protection_descr
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.VoltageProtection {
                    id: voltageProtection

                    checked: !device.voltage_protection_off
                }
            }

            DS3.Comment {
                id: voltageProtectionComment

                width: parent.width

                text: tr.voltage_protection_descr
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.IndicationMode { id: indicationMode }
                Settings.LedBrightnessSlider { id: ledBrightness }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.LockupRelayModeCombobox { id: channelModeCombobox }
                Settings.ChannelNormStateCombobox { id: channelNormalState }
                Settings.LockupRelayTimeCombobox {
                    id: impulseTimeCombobox

                    enabled: hub.online && device.online
                    currentIndex: device.impulse_duration - 1
                    visible: channelModeCombobox.currentText == tr.pulse
                }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.ResetEnergyConsumption { id: resetEnergyConsumption }
            }

            DS3.Comment {
                visible: device.date_of_energy_counter_reset !== "N/A"
                text: {
                    if (device.date_of_energy_counter_reset === "TODAY") return tr.last_reset + ": " + tr.today
                    else return util.insert(tr.settings_days_ago_desktop, [device.date_of_energy_counter_reset,
                                                                            device.number_of_days_of_last_energy_reset])
                }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Parts.ScenariosNav {
                    onEntered: {
                        var settings = {
                            "common_part": {
                                "name": {"name": deviceName.atomInput.text.trim()},
                            },
                            "type_g": {
                                "indication_mode": indicationMode.currentIndex + 1,
                                "indication_brightness": ledBrightness.value,
                            },
                            "current_protection_threshold": currentProtectionThreshold.value,
                            "voltage_protection_off": !voltageProtection.checked,
                            "channel_mode": channelModeCombobox.currentIndex + 1,
                            "channel_normal_state": channelNormalState.currentIndex + 1,
                            "impulse_duration": impulseTimeCombobox.currentIndex + 1,
                            "_params": {
                                "alt_action_success": true,
                            },
                        }

                        if (roomsCombobox.currentIndex >= 0) {
                            var room = rooms.get_room(roomsCombobox.currentIndex)
                            settings["common_part"]["room_id"] = room.id
                        }

                        app.hub_management_module.apply_update(management, device, settings)
                    }
                }
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}