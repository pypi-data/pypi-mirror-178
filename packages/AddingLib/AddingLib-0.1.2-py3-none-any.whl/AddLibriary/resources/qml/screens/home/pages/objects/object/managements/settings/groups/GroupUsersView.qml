import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: groupDevicesView

    height: parent.height
    width: parent.width

    color: ui.ds3.bg.base

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: groupDevicesView.top
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24


        DS3.SettingsContainer {
            id: groupsContainer

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            clip: true

            Repeater {
                width: groupsContainer.width
                height: contentHeight

                model: management.filtered_pro_and_users
                clip: true

                Item {
                    width: groupsContainer.width
                    height: 96

                    DS3.UserSwitch {
                        height: 96

                        imageSource: !!user.small_image_link && user.small_image_link != "WRONG" ? user.small_image_link : ""
                        atomTitle {
                            title: user.name
                            subtitle: user.email
                        }
                        role: {
                            if (!user || !user.hub_role) return ""
                            let roleMap = {
                                "USER": tr.user,
                                "MASTER" : tr.admin,
                                "PRO" : tr.pro
                            }
                            return roleMap[user.hub_role] || ""
                        }
                        enabled: {
                            if (user.hub_role != "USER" && checked) {
                                return false
                            }
                            return true
                        }
                        hasPrivacyOfficerBadge: user.privacy_access_settings == true && hub.show_privacy_officer_badge
                        checked: !!user.normalized_group_permissions[group.group_id]

                        onSwitched: {
                            let groupsPermissions = user.create_new_group_permissions(group.group_id, !checked)
                            app.hub_management_module.apply_update(management, user, {"group_permissions": groupsPermissions})
                        }
                    }
                }
            }
        }
    }
}
