import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: hubSidebar
    color: ui.colors.black
    Layout.fillHeight: true
    Layout.minimumWidth: 334
    Layout.maximumWidth: 334

    property var currentTab: "DEVICES"

    property var currentIndex: {
        if (currentTab == "DEVICES") return 0
        if (currentTab == "ROOMS") return 1
        if (currentTab == "NOTIFICATIONS") return 2
        if (currentTab == "CONTROL") return 3
    }

    Connections {
        target: home

        onOpenOnNotificationsTabChanged: {
            if (home.openOnNotificationsTab == hub.hub_id && hubSidebar.currentTab != "NOTIFICATIONS") {
                notificationsTabArea.selectArea.clicked(true)
            }
        }
    }

    Component.onCompleted: {
        if (home.openOnNotificationsTab == hub.hub_id && hubSidebar.currentTab != "NOTIFICATIONS") {
            notificationsTabArea.selectArea.clicked(true)
        }
    }

    Connections {
        target: app.hub_management_module

        onReloadProNotifications: {
            if (hubSidebar.currentTab == "NOTIFICATIONS") {
                app.hub_management_module.get_hub_events(hub.hub_id, 0)
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Custom.RoundedRect {
            color: ui.colors.dark3
            radius: 10
            bottomRightCorner: hubSidebar.currentTab == "DEVICES"
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 64
            Layout.maximumHeight: 64

            Image {
                id: backToHubsIcon

                sourceSize.width: 24
                sourceSize.height: 24
                source: "qrc:/resources/images/icons/back-arrow.svg"
                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                Custom.HandMouseArea {
                    id: backToHubsArea

                    onClicked: {
                        application.debug("pro -> hubs -> hub -> back to all hubs")

                        home.destroyHub()
                    }

                    /* ------------------------------------------------ */
                    /* desktop tests */
                    Accessible.name: "hub_back_button"
                    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + backToHubsIcon.source + "</button>"
                    Accessible.role: Accessible.Button
                    Accessible.checkable: visible && enabled
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        backToHubsArea.clicked(true)
                    }
                    /* ------------------------------------------------ */
                }
            }
        }

        Custom.RoundedRect {
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: true
            enabled: visible
            color: hubSidebar.currentTab == "DEVICES" ? ui.colors.black : ui.colors.dark1
            radius: 10
            bottomRightCorner: hubSidebar.currentTab == "ROOMS"

            SidebarItem {
                anchors.fill: parent
                text: {
                    var temp = tr.devices
                    return temp.charAt(0).toUpperCase() + temp.slice(1)
                }
                selected: hubSidebar.currentTab == "DEVICES"
                source: "qrc:/resources/images/pro/tabs/a-devices.svg"

                selectArea.onClicked: {
                    application.debug("pro -> hubs -> hub -> devices tab")
                    hubSidebar.currentTab = "DEVICES"
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "devices_tab_icon"
                accessibleIconDescription: source

                accessibleTextName: "devices_tab_text"
                accessibleTextDescription: text

                accessibleAreaName: "devices_tab_area"
                accessibleAreaDescription: "click on devices_tab"
                /* -------------------------------------------------------- */
            }
        }

        Custom.RoundedRect {
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: true
            enabled: visible
            color: hubSidebar.currentTab == "ROOMS" ? ui.colors.black : ui.colors.dark1
            radius: 10
            topRightCorner: hubSidebar.currentTab == "DEVICES"
            bottomRightCorner: hubSidebar.currentTab == "NOTIFICATIONS"

            SidebarItem {
                anchors.fill: parent
                text: {
                    var temp = tr.rooms
                    return temp.charAt(0).toUpperCase() + temp.slice(1)
                }
                selected: hubSidebar.currentTab == "ROOMS"
                source: "qrc:/resources/images/pro/tabs/a-room.svg"

                selectArea.onClicked: {
                    application.debug("pro -> hubs -> hub -> rooms tab")
                    hubSidebar.currentTab = "ROOMS"
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "rooms_tab_icon"
                accessibleIconDescription: source

                accessibleTextName: "rooms_tab_text"
                accessibleTextDescription: text

                accessibleAreaName: "rooms_tab_area"
                accessibleAreaDescription: "click on rooms_tab"
                /* -------------------------------------------------------- */
            }
        }

        Custom.RoundedRect {
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: true
            enabled: visible
            color: hubSidebar.currentTab == "NOTIFICATIONS" ? ui.colors.black : ui.colors.dark1
            radius: 10
            topRightCorner: hubSidebar.currentTab == "ROOMS"
            bottomRightCorner: hubSidebar.currentTab == "CONTROL"

            SidebarItem {
                id: notificationsTabArea
                anchors.fill: parent
                text: {
                    var temp = tr.notifications
                    return temp.charAt(0).toUpperCase() + temp.slice(1)
                }
                selected: hubSidebar.currentTab == "NOTIFICATIONS"
                source: "qrc:/resources/images/pro/tabs/a-notifications.svg"

                selectArea.onClicked: {
                    application.debug("pro -> hubs -> hub -> notifications tab")
                    hubSidebar.currentTab = "NOTIFICATIONS"

                    app.hub_management_module.get_hub_events(hub.hub_id, 0)

                    app.start_stream_hub_events()
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "notifications_tab_icon"
                accessibleIconDescription: source

                accessibleTextName: "notifications_tab_text"
                accessibleTextDescription: text

                accessibleAreaName: "notifications_tab_area"
                accessibleAreaDescription: "click on notifications_tab"
                /* -------------------------------------------------------- */
            }

            Rectangle {
                width: eventsCountText.width + 20
                height: 30

                radius: 8
                color: ui.colors.red1
                visible: hub.events_count > 0

                anchors {
                    right: parent.right
                    rightMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    id: eventsCountText

                    text: hub.events_count
                    color: ui.colors.black

                    width: contentWidth
                    height: parent.height
                    anchors.centerIn: parent

                    maximumLineCount: 1
                    font.pixelSize: 16
                    wrapMode: Text.NoWrap
                    textFormat: Text.PlainText
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

        Custom.RoundedRect {
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: true
            enabled: visible
            color: hubSidebar.currentTab == "CONTROL" ? ui.colors.black : ui.colors.dark1
            radius: 10
            topRightCorner: hubSidebar.currentTab == "NOTIFICATIONS"

            SidebarItem {
                anchors.fill: parent
                text: {
                    var temp = tr.remote
                    return temp.charAt(0).toUpperCase() + temp.slice(1)
                }
                selected: hubSidebar.currentTab == "CONTROL"
                source: "qrc:/resources/images/pro/tabs/a-control.svg"

                selectArea.onClicked: {
                    application.debug("pro -> hubs -> hub -> control tab")
                    hubSidebar.currentTab = "CONTROL"
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_tab_icon"
                accessibleIconDescription: source

                accessibleTextName: "control_tab_text"
                accessibleTextDescription: text

                accessibleAreaName: "control_tab_area"
                accessibleAreaDescription: "click on control_tab"
                /* -------------------------------------------------------- */
            }
        }

        Custom.RoundedRect {
            color: ui.colors.dark3
            radius: 10
            topRightCorner: hubSidebar.currentTab == "CONTROL"
            Layout.alignment: Qt.AlignBottom
            Layout.fillHeight: true
            Layout.minimumWidth: parent.width
        }
    }
}