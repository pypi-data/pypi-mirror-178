import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsNavigationTitlePrimary {
    id: testFireNav

    signal testFireStarted

    Connections {
        target: testFireNav

        onTestFireStarted: {
            Popups.text_popup(
                tr.test_about_start,
                device.obj_type == "4d" ? tr.test_about_start_interconnect_on : util.insert(tr.test_about_start_fire_descr, [hub.frame_length])
            )
        }
    }

    visible: device.test_fire_available
    title: tr.fireprotect_self_test
    icon: "qrc:/resources/images/Athena/settings_icons/DeviceTestSettings-L"

    onEntered: {
        if (device.obj_type == "4d" && device.is_any_alarm) {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.test_unavailable_title,
                text: tr.test_unavailable_description,
            })
        } else {
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/TestFireStep.qml"
            )
        }
    }

}