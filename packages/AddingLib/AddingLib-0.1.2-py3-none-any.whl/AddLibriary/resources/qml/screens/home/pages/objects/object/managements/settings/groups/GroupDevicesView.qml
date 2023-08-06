import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: groupDevicesView

    height: parent.height
    width: parent.width

    color: ui.ds3.bg.base

    Component.onCompleted: {
        management.filtered_devices_excluded_hub_and_with_group_devices.set_filter(group.group_id)
        addDeviceGroupButton.enabled = management.filtered_devices_excluded_hub_and_group_devices.length != 0
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: groupDevicesView.top
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.InfoContainer {
            id: emptyDevicesScreen

            width: parent.width

            imageType: DS3.InfoContainer.ImageType.PlugImage
            descComponent.text: devicesRepeater.count == 0 && !addDeviceGroupButton.enabled ? tr.add_first_device_in_room : tr.add_device_new_group_descr
            z: 2
            imageSource: "qrc:/resources/images/Athena/common_icons/GroupNoDevicesIcon.svg"
            visible: devicesRepeater.count == 0
        }

        Column {
            width: parent.width

            spacing: 1

            Repeater {
                id: devicesRepeater

                width: parent.width

                model: management.filtered_devices_excluded_hub_and_with_group_devices

                onCountChanged: {
                    management.filtered_devices_excluded_hub_and_group_devices.set_filter(group.group_id)
                    addDeviceGroupButton.enabled = management.filtered_devices_excluded_hub_and_group_devices.length != 0
                }

                DS3.SettingsContainerItem {
                    width: parent.width
                    height: childrenRect.height

                    isFirst: index == 0
                    isLast: index == devicesRepeater.count - 1

                    Item {
                        width: parent.width
                        height: 104

                        Loader {
                            id: groupLoader

                            width: parent.width
                            height: parent.height

                            source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/DeviceDelegate.qml"
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: {
                if (addDeviceGroupButton.visible) {
                    if (emptyDevicesScreen.visible) {
                        return 48
                    }
                    return 24
                }
                return 0
            }
        }

        DS3.ButtonOutlined {
            id: addDeviceGroupButton

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            enabled: management.filtered_devices_excluded_hub_and_group_devices.length != 0
            text: tr.select_devices

            onClicked: {
                Popups.select_devices_popup(group)
            }
        }
    }
}
