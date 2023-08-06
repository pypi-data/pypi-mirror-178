import QtQuick 2.12
//import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups

DS3Popups.PopupStep {

    property bool hasSecondButton: device.subtype == "LIGHT_SWITCH_TWO_GANG"

//  Footer button click callback. By, default send apply update command.
    property var saveButtonClickCallback: () => {
        var subtypeLower = device.subtype.toLowerCase()

        var settings = {}
        settings[subtypeLower] = {}

        var settings_channel1 = {
            "SHUT_OFF_MODE_ENABLED": device.shut_off_mode_enabled_ch1,
            "EVENTS_BY_USER_ENABLED": leftButtonSwitch.checked,
            "EVENTS_BY_SCENARIO_ENABLED": leftButtonScenarioSwitch.checked
        }
        settings[subtypeLower]["settings_channel1"] = Object.keys(settings_channel1).filter(k => settings_channel1[k])

        if (hasSecondButton) {
            var settings_channel2 = {
                "SHUT_OFF_MODE_ENABLED": device.shut_off_mode_enabled_ch2,
                "EVENTS_BY_USER_ENABLED": rightButtonSwitch.checked,
                "EVENTS_BY_SCENARIO_ENABLED": rightButtonScenarioSwitch.checked
            }
            settings[subtypeLower]["settings_channel2"] = Object.keys(settings_channel2).filter(k => settings_channel2[k])
        }

        Popups.please_wait_popup()
        app.hub_management_module.apply_update(management, device, settings)
        return true
    }

    height: maxStepHeight
    width: parent.width

    sidePadding: 24

    title: tr.notifications

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            leftButtonSwitch.checked,
            leftButtonScenarioSwitch.checked,
            rightButtonSwitch.checked,
            rightButtonScenarioSwitch.checked
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleUniversal {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.notifications_lightswitch_title
    }

    DS3.Spacing {
        height: 24
    }

    // ----------------- button one (left) ---------------------------

    DS3.TitleSection {
        text: device.button1_name
        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
    }

    DS3.SettingsContainer {

        width: parent.width

        DS3.SettingsSwitch {
            id: leftButtonSwitch

            checked: device.events_by_user_enabled_ch1
            title: tr.when_turned_on_off_title
        }
    }

    DS3.Comment {
        width: parent.width

        text: leftButtonSwitch.checked ?
            tr.when_turned_on_off_descr_enabled :
            tr.when_turned_on_off_descr_disabled
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {

        width: parent.width

        DS3.SettingsSwitch {
            id: leftButtonScenarioSwitch

            checked: device.events_by_scenario_enabled_ch1
            title: tr.when_scenario_executed_title
        }
    }

    DS3.Comment {
        width: parent.width

        text: leftButtonScenarioSwitch.checked ?
            tr.when_scenario_executed_descr_enabled :
            tr.when_scenario_executed_descr_disabled
    }

    DS3.Spacing {
        height: 24
    }

    // ----------------- button two (right) ---------------------------
    Column {
        width: parent.width

        visible: hasSecondButton

        DS3.TitleSection {
            text: device.button2_name || ""
            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
        }

        DS3.SettingsContainer {

            width: parent.width

            DS3.SettingsSwitch {
                id: rightButtonSwitch

                checked: device.events_by_user_enabled_ch2
                title: tr.when_turned_on_off_title
            }
        }

        DS3.Comment {
            width: parent.width

            text: rightButtonSwitch.checked ?
                tr.when_turned_on_off_descr_enabled :
                tr.when_turned_on_off_descr_disabled
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {

            width: parent.width

            DS3.SettingsSwitch {
                id: rightButtonScenarioSwitch

                checked: device.events_by_scenario_enabled_ch2
                title: tr.when_scenario_executed_title
            }
        }

        DS3.Comment {
            width: parent.width

            text: rightButtonScenarioSwitch.checked ?
                tr.when_scenario_executed_descr_enabled :
                tr.when_scenario_executed_descr_disabled
        }

        DS3.Spacing {
            height: 24
        }
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        hasBackground: true
        button.text: tr.save
        enabled: changesChecker.hasChanges

        button.onClicked: {
            if (saveButtonClickCallback()) {
                close()
            }
        }
    }
}