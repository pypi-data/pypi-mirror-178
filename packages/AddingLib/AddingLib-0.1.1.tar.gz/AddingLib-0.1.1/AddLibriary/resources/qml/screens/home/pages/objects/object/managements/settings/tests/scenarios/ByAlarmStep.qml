import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    property var scenario: null

    readonly property var folderItemFilterTypeMap: ({
        "0": "",
        "1": "SECURITY",
        "2": "FIRE",
        "3": "LEAKS",
    })
//    [{device_id: {id: "", checked: [], type: ""}}, ...]
    property var alarmSources: management.filtered_devices_for_scenarios.get_all(scenario).reduce((map, item) => {
        map[item.id] = item
        return map
    }, {})
    property var amountOfTriggers: Object.keys(alarmSources).filter(
        (deviceId) => alarmSources[deviceId].checked.length
    ).length

    Component.onDestruction: {
        if (isFastPHOD) { management.filtered_devices_for_scenarios_fast_pod.set_scenario_type_filter("") }
        else if (isPHOD) {management.filtered_devices_for_scenarios_pod.set_scenario_type_filter("") }
        else { management.filtered_devices_for_scenarios.set_scenario_type_filter("") }
    }

    height: maxStepHeight

    title: tr.scenario_type_alarm

    DS3.Spacing {
        height: 1
    }

    DS3.FolderControl {
        id: folderControl

        visible: !isPHOD || isFastPHOD
        model: [
            {text: tr.a911_all, index: 0},
            {text: tr.intrusion_filter, index: 1},
            {text: tr.fire_filter, index: 2},
            {text: tr.leak_filter, index: 3},
        ]

        onCurrentIndexDiffer: (index) => {
            if (isFastPHOD) {
                management.filtered_devices_for_scenarios_fast_pod.set_scenario_type_filter(folderItemFilterTypeMap[index])
                return
            }
            else if (isPHOD ) {
                management.filtered_devices_for_scenarios_pod.set_scenario_type_filter(folderItemFilterTypeMap[index])
                return
            }
            else {
                management.filtered_devices_for_scenarios.set_scenario_type_filter(folderItemFilterTypeMap[index])
                return
            }
        }
    }

    Column {
        visible: devicesListView.list.count == 0

        width: parent.width - 48

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: "qrc:/resources/images/Athena/fibra/NoDevicesForWireTest.svg"
            titleComponent.text: tr.no_devices_of_this_alarm_type
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
        id: devicesListView

        width: parent.width
        height: !list.model.length ? 0 : maxStepHeight - folderControl.height - 1

        list {
            model: {
                if (isFastPHOD) { return management.filtered_devices_for_scenarios_fast_pod }
                if (isPHOD ) { return management.filtered_devices_for_scenarios_pod }
                return management.filtered_devices_for_scenarios
            }
            delegate: DS3.DeviceSelectionSensors {
                id: deviceDelegate

                Connections {
                    target: devicesListView.list

                    onCountChanged: {
                        deviceDelegate.isFirst =
                            deviceDelegate.ListView.previousSection != deviceDelegate.ListView.section
                        deviceDelegate.isLast =
                            deviceDelegate.ListView.nextSection != deviceDelegate.ListView.section
                    }
                }

                isFirst: deviceDelegate.ListView.previousSection != deviceDelegate.ListView.section
                isLast: deviceDelegate.ListView.nextSection != deviceDelegate.ListView.section
                source: {
                    if (device.obj_type == "1d")
                        return Images.get_image(
                            device.obj_type,
                            "Medium",
                            device.input_type,
                            device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm
                        )
                    return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
                }
                title: device.name
                tabs: {
                    const availableAlarms = device.get_alarms_available()
                    return device.get_scenario_alarms().map(alarm => ({
                        icon: alarm.icon,
                        checked: alarmSources[device.id].checked.includes(alarm.alarmId) && availableAlarms.includes(alarm.alarmId),
                        enabled: availableAlarms.includes(alarm.alarmId),
                        sourceIdentifier: alarm.alarmId
                    }))
                }

                onTabsChanged: {
                    alarmSources[device.id].checked = tabs.filter(tab => tab.checked).map(
                        tab => tab.sourceIdentifier
                    )
                    amountOfTriggers = Object.keys(alarmSources).filter(
                        (deviceId) => alarmSources[deviceId].checked.length
                    ).length
                }
            }
            header: Item {
                height: 0
            }
            spacing: 1
            section.property: "room_name"
            section.delegate: Item {

                width: parent.width
                height: sectionItem.height + 24

                DS3.TitleSection {
                    id: sectionItem

                    anchors.bottom: parent.bottom

                    text: section
                    isCaps: true
                    isBgTransparent: true
                    forceTextToLeft: true
                }
            }
        }
    }

    footer: DS3.ButtonBar {
        hasBackground: true
        button {
            text: tr.next
            enabled: !!amountOfTriggers
            onClicked: setChild("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByAlarmSecondStep.qml")
        }
    }
}