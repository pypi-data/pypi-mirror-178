import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

Parts.DeviceSettings {
    property var output_number: null

    DS3Popups.PopupStep {
        sidePadding: 24
        title: device.info_name

        DS3.DeviceHeaderInfo {
            imagePath: Images.bridgeOutputs(device._get_alarm_type(output_number), "Large")
        }

        DS3.SettingsContainer {
            Settings.VHFBridgeOutputAlarmTypeCombobox { id: alarmType }
            Settings.ConnectionTypeCombobox { id: connectionType }
        }

        footer: DS3.ButtonBar {
            width: parent.width

            enabled: devEnable
            hasBackground: true
            button.text: tr.save

            button.onClicked: {
                var settings = {
                    "channels_trip": [],
                }

                settings["event_ch" + output_number] = alarmType.currentIndex

                for (var out = 0; out < 8; out++) {
                    settings["channels_trip"].push({
                        "channel_id": out,
                        "connection_type": out == output_number - 1 ?
                            connectionType.currentIndex + 1 :
                            device._get_int_connection_type(out),
                    })
                }

                Popups.please_wait_popup()
                app.hub_management_module.apply_update(management, device, settings)
                close()
            }
        }
    }
}