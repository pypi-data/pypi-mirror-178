import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/"
import "qrc:/resources/qml/components/911/" as Custom


Item {
    property var device
    property alias devices: listViewDevices
    property alias groups: listViewGroups

    onDeviceChanged: {
        if (device == null) deviceLoader.source = ""
    }

    Layout.fillHeight: true
    Layout.fillWidth: true

    RowLayout {
        anchors.fill: parent

        spacing: 8

        Rectangle {
            Layout.fillWidth: false
            Layout.preferredWidth: 226
            Layout.fillHeight: true
            color: ui.ds3.bg.base

            ListViewGroups {
                id: listViewGroups

                anchors.fill: parent

                withoutSettingIcon: false
                list {
                    model: management.filtered_groups

                    onCurrentIndexChanged: {
                        deviceLoader.source = ""
                        listViewDevices.list.currentIndex = -1
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.ds3.bg.base

            ListViewDevices {
                id: listViewDevices

                anchors.fill: parent

                withoutSettingIcon: false
                list {
                    model: management.filtered_group_devices
                    footer: Item {}
                    delegate: Rectangle {
                        id: deviceDelegate

                        width: parent.width
                        height: 72

                        color: ui.colors.black

                        Rectangle {
                            width: parent.width
                            height: 72

                            color: ui.colors.dark1

                            Custom.HandMouseArea {
                                onClicked: {
                                    currentIndex =  index
                                    device = listViewDevices.list.model.get(listViewDevices.list.currentIndex)
                                    var pathCameraView = "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/CameraView.qml"
                                    if (device == null || device.device_view === pathCameraView) return
                                    deviceLoader.setSource(device.device_view, {"device": device})
                                    var component = Qt.createComponent(
                                        "qrc:/resources/qml/screens/home/pages/monitoring/incident_tabbar/BackArrow.qml")
                                    var item = deviceLoader.item.children[0].children[0]
                                    component.createObject(item, {"x": 26, "y": 25})
                                }
                            }
                        }

                        Loader {
                            id: loader

                            anchors.fill: parent

                            source: device ? device.delegate : ""
                        }
                    }
                }
            }
            Rectangle {
                anchors.fill: parent

                color: ui.colors.dark3
                visible: {
                    return !(deviceLoader.source == "")
                }

                Loader {
                    id: deviceLoader

                    anchors.fill: parent
                }
            }
        }
    }
}