import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    id: devicesItem

    property var device: null
    property alias devices: devicesListView

    /* ------------------------------------------------ */
    /* desktop tests */
    property var accessiblePrefix: ""
    /* ------------------------------------------------ */

    onDeviceChanged: {
        if (device == null) {
            deviceLoader.source = ""
            devicesListView.resetMtrDevicesIndex()
            devicesListView.list.currentIndex = -1
        }
    }

    Connections {
        target: app

        onPhotoOnDemandSuccess: {
            Popups.text_popup(tr.information, util.insert(tr.photo_on_demand_info, [data.name, data.room_name]))
        }
    }

    Connections {
        target: management ? management.devices : null

        onDeleteDevice: {
            if (devicesItem.device && devicesItem.device.id == deleted_id) {
                device = null
            }
        }
    }

    Connections {
        target: application

        onAddFibraDevicePopup: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDevicePopup.qml", {"hub": hub, "roomIndex": roomIndex})
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

            ListViewDevices {
                id: devicesListView

                anchors.fill: parent

                colorMagic: true
                withoutSettingIcon: false
                list {
                    model: management ? management.filtered_devices : null
                    footer: Footer {
                        btn {
                            text: tr.add_device

                            onClicked: {
                                if (!management.filtered_rooms.length) {
                                    Popups.text_popup(
                                        tr.please_add_at_least_one_room_first,
                                        tr.please_add_at_least_one_room_first_descr
                                    )
                                    return
                                }
                                Popups.select_add_device_popup(null, management, true)
                            }
                        }
                        visible: hub && hub.online && hub.state != "ARMED" && hub.state != "NIGHT_MODE" &&
                            hub.current_user.device_edit_access && hub.two_stage_arming_progress_status <= 1

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        accessibleButtonName: devicesItem.accessiblePrefix + "_add_button"
                        /* ------------------------------------------------ */
                    }

                    onCurrentIndexChanged: {
                        if (!devicesListView.list.model) return
                        device = devicesListView.list.model.get(devicesListView.list.currentIndex)
                        if (device == null) return
                        deviceLoader.setSource(device.device_view, {"device": device})
                    }
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                accessiblePrefix: devicesItem.accessiblePrefix
                /* ------------------------------------------------ */
            }

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: devicesListView.list.model ? devicesListView.list.model.length == 0 : true
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.ds3.bg.base

            Custom.EmptySpaceLogo {
                size: parent.width / 2
                visible: device == null
            }

            Loader {
                id: deviceLoader

                anchors.fill: parent

                onSourceChanged: {
                    deviceLoader.onSourceChanged.connect(deviceLoader.widthChanged)
                }

                onWidthChanged: {
                    if (deviceLoader.item == null) return

                    if (deviceLoader.item.marginView) {
                        if (width >= 499) {
                            deviceLoader.item.marginView = width - 500 + 64
                        } else if (width <= 266) {
                            deviceLoader.item.marginView = 16
                        } else if (width > 266 && width < 499) {
                            deviceLoader.item.marginView = 64
                        }
                    }
                }
            }
        }
    }
}
