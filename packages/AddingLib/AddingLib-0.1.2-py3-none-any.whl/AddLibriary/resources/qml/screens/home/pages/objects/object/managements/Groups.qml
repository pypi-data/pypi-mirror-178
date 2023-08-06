import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    id: groupsDevicesItem

    property var device: null

    onDeviceChanged: {
        if (device == null) {
            deviceLoader.source = ""
            listViewDevices.list.currentIndex = -1
        }
    }

    Connections {
        target: management ? management.devices : null

        onDeleteDevice: {
            if (groupsDevicesItem.device && groupsDevicesItem.device.id == deleted_id) device = null
        }
    }

    Layout.fillWidth: true
    Layout.fillHeight: true

    RowLayout {
        anchors.fill: parent

        spacing: 8

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.ds3.bg.base

            ListViewGroups {
                id: listViewGroups

                anchors.fill: parent

                list {
                    model: management ? management.filtered_groups : null
                    footer: Footer {
                        btn {
                            text: tr.add_group

                            onClicked: {
                                Popups.add_group_popup()
                            }
                        }
                        visible: management && management.filtered_groups && hub && hub.online &&
                            !["ARMED", "NIGHT_MODE"].includes(hub.state) && hub.current_user.device_edit_access &&
                            hub.two_stage_arming_progress_status <= 1
                    }
                }
            }

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: listViewGroups.list.model ? listViewGroups.list.model.length == 0 : true
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.ds3.bg.base

            ListViewDevices {
                id: listViewDevices

                anchors.fill: parent

                list {
                    model: management ? management.filtered_group_devices : null
                    footer: Footer {
                        visible: {
                            if (!hub) return false
                            if (!hub.online) return false
                            if (hub.state == "ARMED" || hub.state == "NIGHT_MODE") return false
                            if (!hub.current_user.device_edit_access) return false
                            if (hub.two_stage_arming_progress_status > 1) return false
                            return true
                        }
                        btn {
                            text: tr.add_device

                            onClicked: {
                                if (!management.filtered_rooms.length) {
                                    Popups.text_popup(tr.please_add_at_least_one_room_first, tr.please_add_at_least_one_room_first_descr)
                                    return
                                }
                                Popups.select_add_device_popup(listViewDevices.list.currentIndex, management, false)
                            }
                        }
                    }

                    onCurrentIndexChanged: {
                        if (!listViewDevices.list.model) return
                        device = listViewDevices.list.model.get(listViewDevices.list.currentIndex)
                        if (device == null) return
                        deviceLoader.setSource(device.device_view, {"device": device})
                    }
                }
            }

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: listViewDevices.list.model ? listViewDevices.list.model.length == 0 : true
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.colors.dark3

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: device == null
            }

            Loader {
                id: deviceLoader
                anchors.fill: parent
            }
        }
    }
}