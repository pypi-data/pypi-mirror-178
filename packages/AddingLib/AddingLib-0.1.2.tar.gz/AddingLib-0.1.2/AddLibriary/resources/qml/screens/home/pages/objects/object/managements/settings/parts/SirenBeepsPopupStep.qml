import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3Popups.PopupStep {
    property bool hubCapability: hub.firmware_version_dec > 211100

    // OLD
    property bool beepOnArmDisarm: device.act_on_arming
    property bool beepOnDelay: device.beep_on_delay

    // NEW
    property bool beepWADV2: device.beep_on_arm_disarm_v2.includes("BEEP_ON_ARM") || device.beep_on_arm_disarm_v2.includes("BEEP_ON_DISARM")
    property bool beepWADNV2: device.beep_on_arm_disarm_v2.includes("BEEP_ON_NIGHT_ARM") || device.beep_on_arm_disarm_v2.includes("BEEP_ON_NIGHT_DISARM")
    property bool beepOnArmDelay: device.beep_on_delay_v2.includes("BEEP_ON_ARM_DELAY")
    property bool beepOnDisarmDelay: device.beep_on_delay_v2.includes("BEEP_ON_DISARM_DELAY")
    property bool beepOnExitDelayInNightMode: device.beep_on_delay_v2.includes("BEEP_ON_NIGHT_ARM_DELAY")
    property bool beepOnEntryDelayInNightMode: device.beep_on_delay_v2.includes("BEEP_ON_NIGHT_DISARM_DELAY")
    property bool chimesEnabled: device.chimes_enabled

    height: maxStepHeight
    
    title: tr.beeps
    sidePadding: 24
    mainView {
        padding: 24
        contentSpacing: 24
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            beepWhenArmingDisarmingV2Switch.checked,
            beepWhenArmingDisarmingNightV2Switch.checked,
            beepWhenArmingDisarmingSwitch.checked,
            beepOnDisarmDelaySwitch.checked,
            beepOnArmDelaySwitch.checked,
            beepOnEntryDelayInNightModeSwitch.checked,
            beepOnExitDelayInNightModeSwitch.checked,
            beepOnDelaySwitch.checked,
            chimesPlaySwitch.checked,
            notifyVolumeCombobox.currentIndex
        ]
    }

    Column {
        width: parent.width

        DS3.TitleSection {
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
            text: tr.beep_when_arming_disarming_title
        }

        DS3.SettingsContainer {
            visible: hubCapability

            DS3.SettingsSwitch {
                id: beepWhenArmingDisarmingV2Switch

                visible: hubCapability
                enabled: hub.online && device.online
                title: tr.beep_when_arming_disarming
                checked: beepWADV2
                cancelBinding: false
            }

            DS3.SettingsSwitch {
                id: beepWhenArmingDisarmingNightV2Switch

                visible: hubCapability
                enabled: hub.online && device.online
                title: tr.beep_when_arming_disarming_in_night_mode
                checked: beepWADNV2
                cancelBinding: false
            }
        }

        DS3.SettingsContainer {
            visible: !hubCapability

            DS3.SettingsSwitch {
                id: beepWhenArmingDisarmingSwitch

                enabled: hub.online && device.online
                title: tr.beep_when_arming_disarming
                checked: beepOnArmDisarm
                cancelBinding: false
            }
        }

        DS3.Comment {
            text: tr.beep_when_arming_disarming_info
        }
    }

// ------------------------------------------------- Beep on Delays ----------------------------------------------------

    Column {
        width: parent.width

        DS3.TitleSection {
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
            text: tr.beep_on_delay_title
        }

        DS3.SettingsContainer {
            visible: hubCapability && device.beep_on_delay_available

            DS3.SettingsSwitch {
                id: beepOnDisarmDelaySwitch

                enabled: hub.online && device.online
                title: tr.beep_on_entry_delay
                checked: beepOnDisarmDelay
                cancelBinding: false
            }

            DS3.SettingsSwitch {
                id: beepOnArmDelaySwitch

                enabled: hub.online && device.online
                title: tr.beep_on_exit_delay
                checked: beepOnArmDelay
                cancelBinding: false
            }

            DS3.SettingsSwitch {
                id: beepOnEntryDelayInNightModeSwitch

                enabled: hub.online && device.online
                title: tr.beep_on_entry_delay_in_night_mode
                checked: beepOnEntryDelayInNightMode
                cancelBinding: false
            }

            DS3.SettingsSwitch {
                id: beepOnExitDelayInNightModeSwitch

                enabled: hub.online && device.online
                title: tr.beep_on_exit_delay_in_night_mode
                checked: beepOnExitDelayInNightMode
                cancelBinding: false
            }
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: beepOnDelaySwitch

                visible: !hubCapability && device.beep_on_delay_available
                enabled: hub.online && device.online
                title: tr.beep_on_delay
                checked: beepOnDelay
                cancelBinding: false
            }
        }

        DS3.Comment {
            visible: device.beep_on_delay_available
            text: tr.beep_on_delay_info
        }
    }

// --------------------------------------------------- Chimes ----------------------------------------------------------

    Column {
        id: chimesPlay

        width: parent.width

        visible: hub.chimes_available && device.chime_play_available

        DS3.TitleSection {
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
            visible: chimesPlay.visible
            text: tr.beep_when_disarmed_title
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: chimesPlaySwitch

                title: tr.chime_play
                enabled: devEnable
                cancelBinding: false
                checked: chimesEnabled
            }
        }

        DS3.Comment {
            text: tr.chime_play_info
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.CommentImportant {
                atomTitle {
                    title: tr.chime_activation_settings
                    subtitle: tr.chime_activation_siren_info
                }
            }
        }
    }

// ------------------------------------------------- Beep Volume -------------------------------------------------------

    DS3.SettingsContainer {
        DS3.SettingsPickerTitleSecondary {
            id: notifyVolumeCombobox

            visible: (device.obj_type != "27" && (hubCapability && (
                    beepWhenArmingDisarmingV2Switch.checked
                    || beepWhenArmingDisarmingNightV2Switch.checked
                    || beepOnArmDelaySwitch.checked
                    || beepOnDisarmDelaySwitch.checked
                    || beepOnExitDelayInNightModeSwitch.checked
                    || beepOnEntryDelayInNightModeSwitch.checked
                ) || !hubCapability && (
                    beepWhenArmingDisarmingSwitch.checked
                    || beepOnDelaySwitch.checked
                ) || chimesPlaySwitch.checked
            ))
            model: [tr.volume_min, tr.volume_mid, tr.volume_max]
            atomTitle.title: tr.event_volume
            currentIndex: {
                if (device.obj_type == "43") return device.events_volume // KPC
                return ({29: 0, 18: 1, 1: 2})[device.events_volume] || 0
            }
        }
    }

    footer: DS3.ButtonBar {
        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            var settings = {}
            
            if (hubCapability) {
                if (device.obj_type == "43") { // KPC
                    settings["act_on_arming_v2"] = []

                    if (beepWhenArmingDisarmingV2Switch.checked) { settings["act_on_arming_v2"].push(...["BEEP_ON_ARM", "BEEP_ON_DISARM"]) }
                    if (beepWhenArmingDisarmingNightV2Switch.checked) { settings["act_on_arming_v2"].push(...["BEEP_ON_NIGHT_ARM", "BEEP_ON_NIGHT_DISARM"]) }

                } else {
                    settings["beep_on_arm_disarm_v2"] = []

                    if (beepWhenArmingDisarmingV2Switch.checked) { settings["beep_on_arm_disarm_v2"].push(...["BEEP_ON_ARM", "BEEP_ON_DISARM"]) }
                    if (beepWhenArmingDisarmingNightV2Switch.checked) { settings["beep_on_arm_disarm_v2"].push(...["BEEP_ON_NIGHT_ARM", "BEEP_ON_NIGHT_DISARM"]) }
                }

                settings["beep_on_delay_v2"] = []
                if (beepOnArmDelaySwitch.checked) {settings["beep_on_delay_v2"].push("BEEP_ON_ARM_DELAY")}
                if (beepOnDisarmDelaySwitch.checked) {settings["beep_on_delay_v2"].push("BEEP_ON_DISARM_DELAY")}
                if (beepOnExitDelayInNightModeSwitch.checked) {settings["beep_on_delay_v2"].push("BEEP_ON_NIGHT_ARM_DELAY")}
                if (beepOnEntryDelayInNightModeSwitch.checked) {settings["beep_on_delay_v2"].push("BEEP_ON_NIGHT_DISARM_DELAY")}
            }
            else {
                if (device.obj_type == "43") settings["act_on_arming"] = beepWhenArmingDisarmingSwitch.checked // KPC
                else settings["beep_on_arm_disarm"] = beepWhenArmingDisarmingSwitch.checked

                settings["beep_on_delay"] = beepOnDelaySwitch.checked
            }

            if (notifyVolumeCombobox.visible) {
                if (device.obj_type == "43") {
                    settings["siren_events_volume"] = parseInt(notifyVolumeCombobox.currentIndex)
                } else {
                    var volume_associated = {0: 32, 1: 29, 2: 18, 3: 1}
                    settings["beep_volume_level"] = volume_associated[notifyVolumeCombobox.currentIndex + 1]
                }
            }

            if (device.chime_play_available) {
                settings["chimes_enabled"] = chimesPlaySwitch.checked
            }

            DesktopPopups.waitPopup(app.actionSuccess, changesChecker.changeInitialValues)
            app.hub_management_module.apply_update(management, device, settings)
        }
    }
}