import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    property var scenario: null
    property var alarmSources: ({})
    property int amountOfTriggers: Object.keys(alarmSources).length

    Component.onCompleted: management.filtered_devices_for_scenarios.set_scenario_type_filter("TEMPERATURE")
    Component.onDestruction: management.filtered_devices_for_scenarios.set_scenario_type_filter("")

    height: maxStepHeight

    title: tr.select_devices

    Column {
        visible: devicesView.list.count == 0

        width: parent.width

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: "qrc:/resources/images/Athena/fibra/NoDevicesForWireTest.svg"
            titleComponent.text: tr.no_devices_scenario_temperature_title
            descComponent.text: tr.no_devices_scenario_temperature_title_descr
        }
    }

    Column {
        width: parent.width - 48

        anchors.horizontalCenter: parent.horizontalCenter

        visible: isLSTwoWay && hub.device_type_counter(["44"], ["LIGHT_SWITCH_TWO_WAY"]) > 1 && devicesListView.list.count != 0

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.CommentImportant {
                atomTitle {
                    title: tr.note_two_way_switches_title
                    subtitle: tr.note_two_way_switches_descr
                }
            }
        }
    }

    DS3.ListView {
        id: devicesView

        width: parent.width
        height: list.count > 0 ? maxStepHeight : 0

        list {
            model: management.filtered_devices_for_scenarios
            delegate: DS3.DeviceSelectionMulti {
                id: deviceDelegate

                width: parent.width

                Component.onCompleted: if (!!scenario && scenario.is_checked_threshold(device.id)) {
                    alarmSources[device.id] = {"device": device}
                    alarmSourcesChanged()
                }

                isLast: deviceDelegate.ListView.nextSection != deviceDelegate.ListView.section
                color: ui.ds3.bg.highest
                imageSource: {
                    if (device.obj_type == "1d")
                        return Images.get_image(
                            device.obj_type,
                            "Medium",
                            device.input_type,
                            device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm
                        )
                    return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
                }
                atomTitle.title: device.name
                checked: !!alarmSources[device.id]

                clickedArea.onClicked: {
                    if (!checked) {
                        alarmSources[device.id] = {"device": device}
                    } else {
                        delete alarmSources[device.id]
                    }
                    alarmSourcesChanged()
                }
            }
            header: Item { height: 0 }
            spacing: 1
            section.property: "room_name"
            section.delegate: Column {
                width: parent.width

                objectName: "section"

                DS3.Spacing {
                    height: 24
                }

                DS3.TitleSection {
                    id: sectionTitle

                    property bool allDevicesSelected: Array.from(Array(devicesView.list.model.length).keys()).filter(
                        index => {
                            const device = devicesView.list.model.get(index)
                            return device.room_name == section
                        }
                    ).every(
                        index => {
                            const device = devicesView.list.model.get(index)
                            return !!alarmSources[device.id]
                        }
                    )

                    width: parent.width

                    forceTextToLeft: true
                    text: section
                    hasButton: true
                    buttonText: allDevicesSelected ? tr.cancel : tr.check_all
                    isTopRounded: true

                    onButtonClicked: () => {
                        if (buttonText == tr.cancel) {
                            alarmSources = Object.entries(alarmSources).filter(
                                ([key, value]) => value.device.room_name != section
                            ).reduce(
                                (newAlarmSources, [id, item]) => Object.assign(
                                    newAlarmSources, { [id]: item }
                                ), {}
                            )
                        } else {
                            Array.from(Array(devicesView.list.model.length).keys()).filter(
                                index => {
                                    const device = devicesView.list.model.get(index)
                                    return device.room_name == section
                                }
                            ).forEach(
                                (index) => {
                                    const device = devicesView.list.model.get(index)
                                    alarmSources[device.id] = {"device": device}
                                }
                            )
                            alarmSourcesChanged()
                        }
                    }
                }

                DS3.Spacing {
                    width: parent.width
                }
            }
        }
    }

    footer: DS3.ButtonBar {
        visible: devicesView.list.count > 0
        hasBackground: true
        button {
            text: tr.next
            enabled: !!amountOfTriggers
            onClicked: setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByTemperatureSecondStep.qml"
            )
        }
    }
}
