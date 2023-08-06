import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups


DS3Popups.PopupStep {
    sidePadding: 24

    property var tmpDeactivation: {
        // ON, OFF for Wire Input

        return {
            "OFF": 0,
            "ON": 1,
            "NO_BYPASS_MODE_INFO": 0,
            "ENGINEER_BYPASS_OFF": 0,
            "ENGINEER_BYPASS_ON": 1,
            "TAMPER_BYPASS_ON": 2,
            }[device.bypass_mode]
    }

    Connections {
        target: app.hub_management_module

        onBypassActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    height: maxStepHeight
    width: parent.width

    title: tr.bypass_mode

    manualIconCallback: () => {
        var link = app.hub_management_module.get_manual_link_bypass()
        Qt.openUrlExternally(link)
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            tmpDeactivation
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        id: temporaryDeactivation

        enabled: hub && hub.online && (device.assigned_extender_name == "" || device.is_assigned_extender_online)

        Repeater {
            width: parent.width

            model: device.has_tamper ? [tr.no, tr.bypass_on, tr.bypass_tamper_on] : [tr.no, tr.bypass_on]

            DS3.SettingsSingleSelection {
                atomTitle.title: modelData
                checked: tmpDeactivation == index
                switchChecked: () => {
                    let bypass_description = device.obj_type == "44" ? tr.lightswitch_is_bypassed_descr : tr.device_is_bypassed_description
                    if (index == 1) Popups.text_popup(tr.device_is_bypassed, bypass_description)
                    if (index == 2) Popups.text_popup(tr.warning, tr.bypass_tamper_on_description)
                    tmpDeactivation = index
                }
            }
        }
    }

    DS3.Spacing {
        height: 4
    }

    DS3.Text {
        width: parent.width

        color: ui.ds3.figure.secondary
        style: ui.ds3.text.body.MRegular
        text: device.obj_type == "44" ? tr.lightswitch_temporary_deactivation : tr.bypass_info
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        button.text: tr.save
        enabled: changesChecker.hasChanges
        hasBackground: true

        button.onClicked: {
            var bypass_signals = [19, 20, 21]

            Popups.please_wait_popup()
            app.hub_management_module.device_command(device, bypass_signals[tmpDeactivation])
        }
    }
}
