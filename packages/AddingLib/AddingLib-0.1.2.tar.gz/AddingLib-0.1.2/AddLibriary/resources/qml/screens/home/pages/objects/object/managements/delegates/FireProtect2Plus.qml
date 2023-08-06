import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


FireProtect2 {
    interconnectButtonVisible: device.is_mute_enabled && !interconnectDelayButtonVisible && !criticalCOButton.visible
    interconnectDelayButtonVisible: !criticalCOButton.visible && device.is_interconnect_delay_available
    criticalButtonVisible: device.critical_co_alarm == "1"

    DS3.ButtonMini {
        id: criticalCOButton

        anchors {
            right: parent.right
            rightMargin: 16
            bottom: parent.bottom
            bottomMargin: 4
        }

        visible: criticalButtonVisible

        opacity: enabled ? 1.0 : 0.3
        // wtf, no interconnect access info (company installer case)
        enabled: !!hub && hub.online && !!device && device.online && !device.is_bypassed && !(!!appUser && appUser.company_id && !hub.current_user.device_edit_access)
        color: ui.ds3.figure.attention
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

        onClicked: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
            {sections: [
                {
                    "title": tr.critical_co_level_title,
                    "description": tr.critical_co_level_description,
                }
            ]}
        )
    }
}