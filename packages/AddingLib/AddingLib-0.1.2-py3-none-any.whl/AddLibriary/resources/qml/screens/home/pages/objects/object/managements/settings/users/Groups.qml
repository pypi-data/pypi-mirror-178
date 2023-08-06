import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups"


import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    id: rect

    property var user: null
    property var sideMargin: 24

    anchors.fill: parent
    color: ui.backgrounds.base

    DS3.NavBarModal {
        id: groupsSettingsBar

        headerText: tr.groups_setup_title
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {'user': user})
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: groupsSettingsBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            List {
                id: groupList

                width: parent.width
                height: contentHeight

                spacing: 1
                model: management.filtered_groups

                delegate: DS3.GroupSwitch {
                    image.source: group.small_image_link != "WRONG" ? group.small_image_link : ""
                    atomTitle {
                        title: !!group ? group.name : ""
                        subtitle: "ID " + (!!group ? group.group_id_dec : "")
                    }
                    descText.text: (
                        !!group && group.devices_count ?
                        tr.devices_count_desktop + ": " + (!!group ? group.devices_count : "") :
                        tr.no_devices_lable
                    )
                    status: !!group && group.devices_count ? ui.ds3.status.DEFAULT : ui.ds3.status.WARNING
                    checked: !!user.normalized_group_permissions[group.group_id]
                    enabled: !(user.hub_role != "USER" && checked)

                    onToggle: () => {
                        var groupsPermissions = user.create_new_group_permissions(group.group_id, !checked)
                        app.hub_management_module.apply_update(management, user, {"group_permissions": groupsPermissions})
                    }
                }
            }
        }
    }
}
