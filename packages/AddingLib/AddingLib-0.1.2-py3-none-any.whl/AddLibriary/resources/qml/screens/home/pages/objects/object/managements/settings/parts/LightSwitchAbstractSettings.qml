import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/js/desktop/popups.js" as Popups


Parts.CommonSettings {
//  To create part of two gang light switch
    property Component twoGangButtonPart: null
//  Reference to the custom two gang light switch item
    readonly property alias twoGangItem: twoGangPartLoader.item
//  Base Light Switch settings
    property var baseLSSettings: {
        var subtypeLower = device.subtype.toLowerCase()

        var settings = {
            "common_part": {
                "name": {"name": deviceName.atomInput.text.trim()},
            },
            "settings_switches": [],
        }

        if (roomsCombobox.currentIndex >= 0) {
            var room = rooms.get_room(roomsCombobox.currentIndex)
            settings["common_part"]["room_id"] = room.id
        }

        if (lockSwitchButton.checked) {
            settings["settings_switches"].push("CHILD_LOCK_ENABLED")
        }
        if (backlight.checked) {
            settings["settings_switches"].push("LED_INDICATOR_ENABLED")
        }
        settings["settings_switches"].push("CURRENT_THRESHOLD_ENABLED")
        settings["settings_switches"].push("STATE_MEMORY_ENABLED")
        settings["panel_color"] = currentColor.deviceColor

        settings[subtypeLower] = {
            "button1_name": buttonName.atomInput.text.trim(),
            "settings_channel1": [],
            "shut_off_period_channel1": switch1ShutOffPeriod.time,
        }

        if (switch1ShutOffByTimer.checked) {
            settings[subtypeLower]["settings_channel1"].push("SHUT_OFF_MODE_ENABLED")
        }
        if (device.events_by_user_enabled_ch1) {
            settings[subtypeLower]["settings_channel1"].push("EVENTS_BY_USER_ENABLED")
        }
        if (device.events_by_scenario_enabled_ch1) {
            settings[subtypeLower]["settings_channel1"].push("EVENTS_BY_SCENARIO_ENABLED")
        }

        return settings
    }
//  Abstract values to be used in real components for changes checking
    property var lightSwitchSettingsForChangesChecker: []
    settingsForChangesChecker: [
        lockSwitchButton.checked,
        backlight.checked,
        switch1ShutOffByTimer.checked,
        buttonName.atomInput.text,
        switch1ShutOffPeriod.time,
        currentColor.deviceColor,
        ...lightSwitchSettingsForChangesChecker
    ]

    generateSettings: () => {
        if (!buttonName.atomInput.text.trim()) {
           Popups.text_popup(tr.information, tr.button_name_blank_error)
           return
        }

        var settings = Object.assign({}, baseLSSettings)

        // Temporary solution for backward compatibility
        settings["_refactored"] = true

        return settings
    }

    deviceImageComponent: Item {}

    Column {
        width: parent.width

        enabled: devEnable

        DS3.DeviceNavigationSmall {
            id: currentColor

            width: parent.width

            deviceType: device.obj_type
            deviceColor: device.panel_color
            deviceSubtype: device.subtype
            atomTitle.title: device.color_name
            atomTitle.subtitle: tr.lightswitch_select_color
            isFirst: true
            isLast: true
            color: ui.ds3.bg.highest

            onActionArrowControlClicked: {
                setChild("qrc:/resources/qml/screens/home/pages/objects/object/popups/SelectColorStep.qml",
                 {
                    "device": device,
                    "selectedColor": deviceColor,
                 })
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                title: tr.notifications

                onEntered: {
                    setChild(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/LSNotifications.qml"
                    )
                }
            }

            DS3.SettingsSwitch {
                id: backlight

                title: tr.backlight_lightswitch
                checked: device.led_indication_enabled
            }

            DS3.SettingsSwitch {
                id: lockSwitchButton

                title: tr.lock_switch_buttons_title
                checked: device.child_lock_enabled
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.lock_switch_buttons_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
            text: device.subtype == "LIGHT_SWITCH_TWO_GANG" ?
                tr.left_button_lightswitch_title :
                tr.button_setings_lightswitch_title
        }

        DS3.SettingsContainer {
            Parts.ButtonName {
                id: buttonName

                buttonName: device.button1_name
            }

            DS3.SettingsSwitch {
                id: switch1ShutOffByTimer


                title: tr.shutoff_by_timer_title
                checked: device.shut_off_mode_enabled_ch1
            }

            Settings.ShutoffTimerLS {
                id: switch1ShutOffPeriod

                visible: switch1ShutOffByTimer.checked
                time: device.shut_off_period_channel1
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.shutoff_by_timer_enabled_descr
        }

        DS3.Spacing {
            height: 24
        }

        Loader {
            id: twoGangPartLoader

            width: parent.width

            sourceComponent: twoGangButtonPart
        }

        DS3.Spacing {
            height: !!twoGangButtonPart ? 24 : 0
        }

        DS3.SettingsContainer {
            ScenariosNav {}
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            TestSignalLevelNav {}
            ManualNav {}
            BypassButtonNav {}
        }
    }
}