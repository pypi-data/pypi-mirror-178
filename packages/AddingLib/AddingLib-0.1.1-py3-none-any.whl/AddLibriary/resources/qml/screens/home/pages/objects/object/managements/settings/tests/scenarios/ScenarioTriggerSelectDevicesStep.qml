import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep { // TODO onChecked include device to selectedDevices and finish with last screen, fix 160 row
    property var selectedDevices: ({})

    property var currentDevice: device

    property var triggerLSButtonName: isLightSwitch ? ["", "button1", "button2"][selectedButtonIndex + 1] : -1

    height: maxStepHeight

    title: tr.select_devices
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/common_icons/IntrusionDevices.Illustration.svg"
        titleComponent.text: tr.no_automation_devices_scenario_title
        descComponent.text: tr.no_automation_devices_scenario_descr
        visible: management.filtered_devices_for_scenarios_switches.length == 0
    }

    DS3.SettingsContainer {
        width: parent.width

        ListView {
            id: devicesView

            width: parent.width
            height: contentHeight

            clip: true
            cacheBuffer: 20000

            spacing: 1
            model: management.filtered_devices_for_scenarios_switches
            interactive: false
            section.property: "room_name"
            section.delegate: Column {
                width: parent.width

                objectName: "section"

                DS3.TitleSection {
                    id: sectionTitle

                    property bool allDevicesSelected: Array.from(Array(devicesView.model.length).keys()).filter(
                        index => {
                            const device = devicesView.model.get(index)
                            return device.room_name == section
                        }
                    ).every(
                        index => {
                            const device = devicesView.model.get(index)
                            return !!selectedDevices[device.id] && (
                                device.subtype != "LIGHT_SWITCH_TWO_GANG"
                                || selectedDevices[device.id].selected_buttons.length == 2
                                || (
                                    selectedDevices[device.id].selected_buttons.length == 1
                                    && !!triggerLSButtonName
                                    && !selectedDevices[device.id].selected_buttons.includes(triggerLSButtonName)
                                )
                            )
                        }
                    )

                    width: parent.width

                    forceTextToLeft: true
                    text: section
                    hasButton: true
                    buttonText: allDevicesSelected ? tr.cancel : tr.check_all

                    onButtonClicked: () => {
                        if (buttonText == tr.cancel) {
                            selectedDevices = Object.entries(selectedDevices).filter(
                                ([key, value]) => value.device.room_name != section
                            ).reduce(
                                (newSelectedDevices, [id, item]) => Object.assign(
                                    newSelectedDevices, { [id]: item }
                                ), {}
                            )
                        } else {
                            Array.from(Array(devicesView.model.length).keys()).filter(
                                index => {
                                    const device = devicesView.model.get(index)
                                    return device.room_name == section
                                }
                            ).forEach(
                                (index) => {
                                    const device = devicesView.model.get(index)
                                    selectedDevices[device.id] = {"device": device}
                                    if (device.class_name == "light_switch") {
                                        selectedDevices[device.id]["selected_buttons"] = []
                                        if (currentDevice.id != device.id || selectedButtonIndex != 0) {
                                            selectedDevices[device.id].selected_buttons.push("button1")
                                        }
                                        if (device.subtype == "LIGHT_SWITCH_TWO_GANG" && (currentDevice.id != device.id || selectedButtonIndex != 1))
                                            selectedDevices[device.id].selected_buttons.push("button2")
                                    }
                                }
                            )
                            selectedDevicesChanged()
                        }
                    }
                }

                DS3.Spacing {
                    width: parent.width
                }
            }

            delegate: Loader {
                id: delegateLoader

                property bool isLightSwitch: device.class_name == "light_switch"

                width: parent.width
                height: item.height

                source: isLightSwitch ?
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/SwitchTargetDelegate.qml" :
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/DefaultTargetDelegate.qml"
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        enabled: Object.keys(selectedDevices).length
        visible: management.filtered_devices_for_scenarios_switches.length != 0
        hasBackground: true
        button {
            text: tr.next
            onClicked: setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ScenarioTriggerActionSettingsStep.qml"
            )
        }
    }
}