import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/js/desktop/popups.js" as Popups


Parts.DeviceSettings {
    Parts.LightSwitchAbstractSettings {
        id: lightSwitchTwoGang

        lightSwitchSettingsForChangesChecker: [
            twoGangItem.twoGangPartSettings
        ]
        generateSettings: () => {
            if (!baseLSSettings["light_switch_two_gang"]["button1_name"] || !twoGangItem.twoGangPartSettings["button2_name"]) {
                Popups.text_popup(tr.information, tr.button_name_blank_error)
                return
            }

            var settings = Object.assign({}, baseLSSettings)
            settings["light_switch_two_gang"]["button2_name"] = twoGangItem.twoGangPartSettings["button2_name"]
            settings["light_switch_two_gang"]["settings_channel2"] = twoGangItem.twoGangPartSettings["settings_channel2"]
            settings["light_switch_two_gang"]["shut_off_period_channel2"] = twoGangItem.twoGangPartSettings["shut_off_period_channel2"]

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        twoGangButtonPart: Column {
            property var twoGangPartSettings: {
                var settings = {
                    "button2_name": twoGangButtonName.atomInput.text.trim(),
                    "settings_channel2": [],
                    "shut_off_period_channel2": switch2ShutOffPeriod.time,
                }

                if (switch2ShutOffByTimer.checked) {
                    settings["settings_channel2"].push("SHUT_OFF_MODE_ENABLED")
                }
                if (device.events_by_user_enabled_ch2) {
                    settings["settings_channel2"].push("EVENTS_BY_USER_ENABLED")
                }
                if (device.events_by_scenario_enabled_ch2) {
                    settings["settings_channel2"].push("EVENTS_BY_SCENARIO_ENABLED")
                }

                return settings
            }

            width: parent.width

            DS3.TitleSection {
                id: buttonTitle

                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.right_button_lightswitch_title
            }

            DS3.SettingsContainer {
                id: twoGangButtonContainer

                width: parent.width

                Parts.ButtonName {
                    id: twoGangButtonName

                    buttonName: device.button2_name
                }

                DS3.SettingsSwitch {
                    id: switch2ShutOffByTimer

                    title: tr.shutoff_by_timer_title
                    checked: device.shut_off_mode_enabled_ch2
                }

                Settings.ShutoffTimerLS {
                    id: switch2ShutOffPeriod

                    visible: switch2ShutOffByTimer.checked
                    time: device.shut_off_period_channel2
                }
            }

            DS3.Comment {
                id: textDescription

                width: parent.width

                text: tr.shutoff_by_timer_enabled_descr
            }
        }
    }
}
