import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings" as AdvancedSettings

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup
//  The group to display and edit/delete
    property var group: null

    Connections {
        target: app

        onActionSuccess: popup.close()
    }

    width: 500
    height: 650


    sideMargins: 0
    header: DS3.NavBarModal {
        id: selectDevicesBar

        isRound: true
        headerText: tr.select_devices
    }

    Item {
        id: selectDevicesScreen

        width: popup.width

        height: popup.height - 80 - 56
        // Filtered devices in one variable
        property var verifying: get_devices()
        // Function to get needed devices
        property var getDevices: get_devices
        // Model for the devices (old logic)
        property var devices_model: {
            if (group == null) {
                if (!appUser.company_id) return appCompany.pro_hubs_model.current_hub.management.filtered_devices_without_groups
                return appCompany.current_facility.management.filtered_devices_without_groups
            } else {
                if (!appUser.company_id) return appCompany.pro_hubs_model.current_hub.management.filtered_devices_excluded_hub_and_group_devices
                return appCompany.current_facility.management.filtered_devices_excluded_hub_and_group_devices
            }
        }
        // function to get needed devices and their data
        function get_devices() {
            var devices = []
            for(var child in devicesView.contentItem.children) {
                let deviceItem = devicesView.contentItem.children[child]
                if (deviceItem.objectName == "delegate") {
                    var dev = devices_model.get(deviceItem.indexRef)
                    var choice = deviceItem.checked
                    var old = deviceItem.old_state
                    devices.push({
                        "device_id": dev.device_id,
                        "choice": choice,
                        "obj_type": dev.obj_type,
                        "group": group,
                        "subtype": device.subtype,
                    })
                }
            }
            return devices
        }

        DS3.ScrollView {
            padding: 24

            DS3.SettingsContainer {
                width: parent.width

                anchors.horizontalCenter: parent.horizontalCenter

                AdvancedSettings.SelectDevicesView {
                    id: devicesView

                    selectDevicesRect: selectDevicesScreen
                    hasGroupData: true
                    getDevices: selectDevicesScreen.getDevices
                    devicesModel: selectDevicesScreen.devices_model
                }
            }
        }
    }


    footer: Item {
        id: saveButton
        width: parent.width
        height: 80

        anchors.centerIn: parent

        clip: true

        DS3.ButtonBar {
            id: buttonBar

            width: parent.width

            buttonText: tr.add_devices_to_group
            hasBackground: true
            enabled: {
                let devicesData = selectDevicesScreen.getDevices()
                return devicesData.filter( el => el["choice"]).length != 0
            }

            button.onClicked: {
                var devicesData = selectDevicesScreen.getDevices()
                var devices = []

                for(let i = 0; i < devicesData.length; i++)
                {
                    if( devicesData[i]["choice"] )
                    {
                        let update_dev = {
                            "type": devicesData[i]["obj_type"],
                            "id": devicesData[i]["device_id"],
                            "group_id": devicesData[i]["group"] ? devicesData[i]["group"].group_id : null
                        }
                        devices.push(update_dev)
                    }
                }
                if (!devices.length) {
                    return
                }

                if (!popup.group) {
                    Popups.select_group_popup(devices)
                    return
                }

                app.hub_management_module.update_objects_settings(devices)
            }
        }
    }
}
