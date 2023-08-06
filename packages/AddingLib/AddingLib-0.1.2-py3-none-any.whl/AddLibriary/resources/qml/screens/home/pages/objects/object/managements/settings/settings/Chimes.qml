import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups



DS3.SettingsTitleSecondaryNavigation {
    id: chimesItem

    property var isMainSensorChecked: ["04", "11", "1d", "64"].includes(device.obj_type) ? false : mainSensor.checked
    property var isChimesSettingsOpen: false
    property var chimeTriggers: device.chime_triggers
    property var chimeSignal: device.chime_signal
    property bool visibilityCondition: true
    property bool isBistable: false
    property var isExternalContactChecked: {
        if(["0F", "6F"].includes(device.obj_type)) { return externalContact.checked && extraContactTypeCombobox.currentIndex != 1} // DPP DPPF
        if(device.obj_type == "11") { return typeExternalContactCombobox.currentIndex == 0} // transmitter
        return externalContact.checked
    }
    property bool isOn: {
        if (isMainSensorChecked && chimesItem.chimeTriggers.includes("CHIME_REED")) return true
        if (device.obj_type === "1d" && chimesItem.chimeTriggers.includes("CHIME_EXTRA_CONTACT_S2")) return true
        if (isExternalContactChecked && chimesItem.chimeTriggers.includes("CHIME_EXTRA_CONTACT")) return true
        return false
    }

    visible: hub.chimes_available && visibilityCondition
    enabled: devEnable
    title: tr.chimes_title
    subtitle: isOn ? tr.on : tr.off

    onEntered: {
        if (saveButtonClickCallback(false)) { // save device setting under hood.
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/advanced_settings/ChimesSettingsPopupStep.qml",
                {"chimesItem": chimesItem}
            )
        }
    }
}