import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    id: roomsDevicesItem

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
            if (roomsDevicesItem.device && roomsDevicesItem.device.id == deleted_id) device = null
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

            ListViewRooms {
                id: listViewRooms

                anchors.fill: parent

                list {
                    model: management ? management.filtered_rooms : null
                    footer: Footer {
                        visible: hub && hub.online && !["ARMED", "NIGHT_MODE"].includes(hub.state) &&
                            hub.current_user.device_edit_access && hub.two_stage_arming_progress_status <= 1
                        btn.onClicked: {
                            Popups.add_room_popup()
                        }
                    }
                }
            }

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: listViewRooms.list.model ? listViewRooms.list.model.length == 0 : true
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
                    model: management ? management.filtered_room_devices : null
                    footer: Footer {
                        visible: management && management.filtered_rooms && hub && hub.online &&
                            !["ARMED", "NIGHT_MODE"].includes(hub.state) && hub.current_user.device_edit_access &&
                            hub.two_stage_arming_progress_status <= 1
                        btn {
                            text: tr.add_device

                            onClicked: {
                                if (!management.filtered_rooms.length) {
                                    Popups.text_popup(tr.please_add_at_least_one_room_first, tr.please_add_at_least_one_room_first_descr)
                                    return
                                }
                                Popups.select_add_device_popup(listViewRooms.list.currentIndex, management, false)
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