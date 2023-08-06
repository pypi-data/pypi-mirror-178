import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    property var device

    property var selectedDevices: []

    height: maxStepHeight

    title: tr.select_devices

    DS3.ListView {
        id: devicesListView

        width: parent.width
        height: maxStepHeight

        list {
            model: management.filtered_devices_for_scenarios_switches
            delegate: DS3.DeviceSelectionMulti {
                id: deviceDelegate

                width: parent.width

                atomTitle.title: device.name
                imageSource: Images.get_image(device.obj_type, "Small", device.color, "0", device.subtype)
                checked: selectedDevices.some(dev => dev.id == device.id)
                clickedArea.onClicked: {
                    if (!checked)
                        selectedDevices.push(device)
                    else
                        selectedDevices = selectedDevices.filter(dev => dev.id != device.id)
                    selectedDevicesChanged()
                }
                isFirst: deviceDelegate.ListView.previousSection != deviceDelegate.ListView.section
                isLast: deviceDelegate.ListView.nextSection != deviceDelegate.ListView.section

                Component.onCompleted: {
                    if (scenario && scenario.get_checked_target(device.obj_type, device.device_id).length) {
                        selectedDevices.push(device)
                        selectedDevicesChanged()
                    }
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
        enabled: !!selectedDevices.length
        hasBackground: true
        button {
            text: tr.next
            onClicked: setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ScenarioButtonActionSettingsStep.qml"
            )
        }
    }
}
