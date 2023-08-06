import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: object_root
    color: ui.colors.black

    property var management: {
        return appCompany.current_facility ? appCompany.current_facility.management : null
    }

    property var hub: {
        return appCompany.current_facility && appCompany.current_facility.management ? appCompany.current_facility.management.devices.hub : null
    }

    property var managementInIncident: false
    property bool hubLoaded: false

    // reset power on mtr fire devices
    signal resetPower()

    property var mtr_fire_alarms: {
        if (management) return management.devices.mtr_fire_alarms
    }

    property var mtrFireAlarmPopup: null
    property var mtrFireAlarmPopupCount: {
        if (mtr_fire_alarms) return mtr_fire_alarms.length
    }

    function reset_power() {
        if (mtr_fire_alarms) return
        for (var i=0; i < mtr_fire_alarms.length; i++) {
            var device = management.devices.get_by_id(mtr_fire_alarms[i].id)
            app.hub_management_module.device_command(device, 22);
        }
    }

    onHubChanged: {
        if (!!hub && !hubLoaded) {
            hub.set_default_permissions()
            app.get_default_hub_permissions()
            hubLoaded = true
        }
    }

    onMtr_fire_alarmsChanged: {
        if (object_root.mtrFireAlarmPopup || !mtr_fire_alarms) return
        if (mtr_fire_alarms.length) {
            object_root.mtrFireAlarmPopup = Popups.reset_power_for_fire_devices(reset_power, mtr_fire_alarms, management)
            object_root.mtrFireAlarmPopup.onResetPower.connect(function() {
                object_root.mtrFireAlarmPopup.destroy()
                object_root.mtrFireAlarmPopup = null
            })
        }
    }

    Timer {
        id: aclTimer

        interval: management.facility_expiration_time * 1000 - Date.now()

        onIntervalChanged: {
            aclTimer.stop()
            if (interval > 0) aclTimer.start()
        }

        onTriggered: {
            management.facility_permissions_expired()
        }
    }

    ColumnLayout {
        id: layout
        anchors.fill: parent
        spacing: 1

        Info {}
        SystemState {}
        Tabs {}
    }

    Loader {
        id: editObjectLoader
        anchors.fill: parent

        onSourceChanged: {
            layout.enabled = !layout.enabled
        }
    }

    Connections {
        target: app.facility_module

        onFacilityApproved: {
            objectsSidebar.reloadModel()
            currentObjectIndex = -2
        }

        onDeleteFacilitySignal: {
            if (facility_id == appCompany.current_facility.id) {
                currentObjectIndex = -1
            }
        }

        onInstallationServiceRemoved: {
            currentObjectIndex = -1
            objectsSidebar.reloadModel()
        }
    }

    Connections {
        target: app.hub_management_module

        onShowRestoreAfterAlarmPopupSignal: {
            if (fromIncident) return

            Popups.reset_alarm_popup(hub, management)
        }

        onHubIntoMaxPowerTest: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
        }

        onHubIntoScanningMode: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/FibraScanningInterruptPopup.qml", {"hub": hub})
        }
    }

    Connections {
        target: app.bindings_module

        onMonitoringApplicationRejectSuccess: {
            objectsSidebar.reloadModel()
            currentObjectIndex = -1
        }
    }

    Component.onCompleted: {
        if (!!facility.id) {
            app.start_stream_facility_permissions()
            app.start_stream_facility_changes()
        }

        app.download_timezones()
    }
}
