import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/"


Rectangle {
    id: equipment
    color: "transparent"

    property var hub: {
        return incident.management.devices.hub
    }
    property var management: {
        return incident.management
    }
    property var rooms: {
        return incident.management.rooms
    }
    property var users: {
        return incident.management.users
    }
    property var groups: {
        return incident.management.groups
    }
    property var currentTab: "DEVICES"

    property var managementInIncident: true

    onHubChanged: if (!!hub && !incident.is_stream_incident_obj_hub_permissions_changes)
        app.incident_module.start_stream_incident_object_hub_permissions_changes(incident)

    ColumnLayout {
        anchors.fill: parent
        spacing: 1
        Item {
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            RowLayout {
                id: tabRow
                spacing: 6
                height: 32
                width: parent.width
                anchors {
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: -2
                }

                anchors {
                    left: parent.left
                    leftMargin: 16
                }

//                property var currentTab: roomsTab
                property var indexTabs: 0
                PanelTab {
                    id: devicesTab
                    text: tr.devices
                    selected: currentTab == "DEVICES"

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            currentTab = "DEVICES"
                            tabRow.indexTabs = 0
                        }
                    }
                }

                PanelTab {
                    id: roomsTab
                    text: tr.rooms
                    selected: currentTab == "ROOMS"

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            currentTab = "ROOMS"
                            tabRow.indexTabs = 1
                        }
                    }
                }

                PanelTab {
                    id: groupsTab
                    text: tr.group_mode_title
                    selected: currentTab == "GROUPS"

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            currentTab = "GROUPS"
                            tabRow.indexTabs = 2
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                }
            }
        }

        Rectangle {
            id: backgroundRect
            color: ui.colors.black
            Layout.fillWidth: true
            Layout.fillHeight: true
            StackLayout {
                id: stackLayout
                width: parent.width
                height: parent.height
                currentIndex: tabRow.indexTabs

                Devices {
                    devices.list.footer: Item {}
                    devices.withoutSettingIcon: true
                }
                RoomsIncident {
                    rooms.withoutSettingIcon: true
                }
                GroupsIncident {
                    groups.withoutSettingIcon: true
                }
            }
        }
        Rectangle {
            color: ui.colors.dark2
            Layout.fillWidth: true
            Layout.preferredHeight: 32

            Custom.Triangle {
                rotation: tabBarIsOpened ? 180 : 0
                scale: 0.8
                anchors.centerIn: parent
            }

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabBarIsOpened = !tabBarIsOpened
                }
            }
        }
    }

    Connections {
        target: app.hub_management_module

        onShowRestoreAfterAlarmPopupSignal: {
            if (!fromIncident) return

            Popups.reset_alarm_popup(hub, management)
        }
    }

    Component.onCompleted: {
        app.incident_module.start_stream_incident_object_hub_changes(incident)
    }
}