import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/hubs/hub/tabs" as Tabs
import "qrc:/resources/qml/screens/home/pages/objects/object/managements" as Management
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/" as Root


Rectangle {
    id: currentHub
    color: ui.colors.black
    anchors.fill: parent

    property var management: {
        return appCompany.pro_hubs_model.current_hub.management
    }
    property var hub: {
        return appCompany.pro_hubs_model.current_hub.management.devices.hub
    }
    property var rooms: {
        return appCompany.pro_hubs_model.current_hub.management.rooms
    }
    property var users: {
        return appCompany.pro_hubs_model.current_hub.management.users
    }
    property var groups: {
        return appCompany.pro_hubs_model.current_hub.management.groups
    }

    property var managementInIncident: false

    // reset power on mtr fire devices
    signal resetPower()

    property var mtr_fire_alarms: {
        return management.devices.mtr_fire_alarms
    }

    property var mtrFireAlarmPopup: null
    property var mtrFireAlarmPopupCount: mtr_fire_alarms.length

    function reset_power() {
        for (var i=0; i < mtr_fire_alarms.length; i++) {
            var device = management.devices.get_by_id(mtr_fire_alarms[i].id)
            app.hub_management_module.device_command(device, 22);
        }
    }

    // ========================= NEW ARCHITECTURE INTEGRATION =========================
    readonly property var hubConfigContext: hubPageLoader.contextTarget.hubConfig

    Root.ContextLoader {
        // TODO: replace whole page with this loader
        id: hubPageLoader

        contextTarget: app.hubsView.chosenHubPage
    }
    // ================================================================================

    onMtr_fire_alarmsChanged: {
        if (currentHub.mtrFireAlarmPopup && mtr_fire_alarms.length === 0) {
            currentHub.mtrFireAlarmPopup.destroy()
            currentHub.mtrFireAlarmPopup = null
        }
        if (currentHub.mtrFireAlarmPopup) return
        if (mtr_fire_alarms.length) {
            currentHub.mtrFireAlarmPopup = Popups.reset_power_for_fire_devices(reset_power, mtr_fire_alarms, management)
            currentHub.mtrFireAlarmPopup.onResetPower.connect(function() {
                currentHub.mtrFireAlarmPopup.destroy()
                currentHub.mtrFireAlarmPopup = null
            })
        }
    }

    RowLayout {
        spacing: 10
        anchors.fill: parent

        Sidebar { id: hubSidebar }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            TopPanel { id: hubInfo }

            Rectangle {
                id: backgroundRect
                width: parent.width
                color: ui.colors.black
                anchors {
                    top: hubInfo.bottom
                    topMargin: 1
                    bottom: parent.bottom
                }

                StackLayout {
                    id: stackLayout
                    anchors.fill: parent
                    currentIndex: hubSidebar.currentIndex

                    Item {
                        Component {
                            id: oldDevices

                            Management.Devices {
                                anchors.fill: parent

                                /* ------------------------------------ */
                                /* desktop tests */
                                accessiblePrefix: "pro_devices"
                                /* ------------------------------------ */
                            }
                        }

                        Component {
                            id: newDevices

                            Root.ContextLoader {
                                contextTarget: app.hubsView.chosenHubPage.devicesTab
                            }
                        }

                        Loader {
                            anchors.fill: parent

                            sourceComponent: __devices_architecture__ ? newDevices : oldDevices
                        }
                    }
                    Management.Rooms {}

                    Tabs.Notifications {}
                    Tabs.HubControl {}
                }
            }
        }
    }

    Connections {
        target: management

        onUserDeleted: {
            if (!appUser) return
            if (!appUser.data) return
            if (!appUser.data.user_info) return
            if (!appUser.data.user_info.cluster_user_id) return
            if (appUser.data.user_info.cluster_user_id != user_id) return

            home.destroyHub()
        }
    }

    Connections {
        target: app.hub_management_module

        onShowRestoreAfterAlarmPopupSignal: {
            Popups.reset_alarm_popup(hub, management)
        }

        onHubIntoMaxPowerTest: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
        }

        onHubIntoScanningMode: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/FibraScanningInterruptPopup.qml", {"hub": hub})
        }
    }

    Component.onCompleted: {
        app.start_stream_hub_events_count()

        app.download_timezones()
    }
}
