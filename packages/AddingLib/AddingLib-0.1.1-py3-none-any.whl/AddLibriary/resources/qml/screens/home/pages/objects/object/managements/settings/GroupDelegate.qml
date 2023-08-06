import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.GroupNavigation {
    imageSourceLink: group.small_image_link
    groupTitle: group.name
    groupID: !!group ? group.group_id_dec : ""
    deviceCount: !!group ? group.devices_count : ""

    settingsGearMouseArea.onClicked: {
        Popups.group_settings_popup(group)
    }
    mainMouseArea.onClicked: {
        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupView.qml", {
            "group": group
        })
    }
}
