import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    property var scenario: null
    property var selectedButtonIndex: ({
            "3b": 0,
            "0x3b": 0,
            "3c": 0,
            "0x3c": 0,
            "3d": 1,
            "0x3d": 1,
            "3e": 1,
            "0x3e": 1,
        }[!!scenario ? scenario.get_source_alarm_source(device.obj_type, device.device_id) : "3b"])

    property int selectedTriggerType: buttonAction.selectedIndex

    Component.onCompleted: {
        management.filtered_devices_for_scenarios_switches.set_filter(
            isLSTwoGang ? "" : device.device_id
        )
    }

    height: maxStepHeight

    title: tr.scenario_settings
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    Column {
        width: parent.width

        visible: isLSTwoWay && hub.device_type_counter(["44"], ["LIGHT_SWITCH_TWO_WAY"]) > 1

        DS3.SettingsContainer {
            DS3.CommentImportant {
                atomTitle {
                    title: tr.note_two_way_switches_title
                    subtitle: tr.note_two_way_switches_descr
                }
            }
        }

        DS3.Spacing {
            height: 24
        }
    }

    Column {
        width: parent.width

        visible: isLSTwoGang

        DS3.TitleSection {
            text: tr.button_title_scenario
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            id: actionButton

            width: parent.width

            Repeater {
                id: actionButtonModel

                model: !!device.button1_name && !!device.button2_name ? [device.button1_name, device.button2_name] : []

                DS3.SettingsSingleSelection {
                    atomTitle.title: modelData
                    checked: selectedButtonIndex == index
                    switchChecked: () => selectedButtonIndex = index
                }
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.two_buttons_descr_scenario
        }
    }

    DS3.Spacing {
        height: actionButton.visible ? 24 : 0
    }

    DS3.TitleSection {
        text: tr.when_button_title
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
        visible: isLightSwitch
    }

    DS3.SettingsContainer {
        id: buttonAction

        property string selectedIndex: ({
            "21": 0,
            "0x21": 0,
            "22": 1,
            "0x22": 1,
            "3b": 0,
            "0x3b": 0,
            "3c": 1,
            "0x3c": 1,
            "3d": 0,
            "0x3d": 0,
            "3e": 1,
            "0x3e": 1,
        }[!!scenario ? scenario.get_source_alarm_source(device.obj_type, device.device_id) : "21"])

        width: parent.width

        Repeater {
            id: buttonActionModel

            model: isLightSwitch ?
                [tr.scenario_action_ON, tr.scenario_action_OFF]
                :
                [tr.smart_button_short_press, tr.smart_button_long_press]

            DS3.SettingsSingleSelection {
                atomTitle.title: modelData
                checked: index == buttonAction.selectedIndex
                switchChecked: () => buttonAction.selectedIndex = index
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.when_button_descr
        visible: isLightSwitch
    }

    footer: DS3.ButtonBar {
        hasBackground: true
        enabled: isLSTwoGang ? selectedButtonIndex !== -1 : true
        button {
            text: tr.next
            onClicked: setChild("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ScenarioTriggerSelectDevicesStep.qml")
        }
    }
}
