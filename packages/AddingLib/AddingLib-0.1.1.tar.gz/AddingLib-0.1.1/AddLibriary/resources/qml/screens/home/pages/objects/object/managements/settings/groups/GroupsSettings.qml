import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: groupsSettings

//  Constant side margin
    readonly property var sideMargin: 24
//  Constant default spacing
    readonly property var defaultSpacing: 24

    height: parent.height
    width: parent.width

    color: ui.ds3.bg.base
    radius: 12

    DS3.NavBarModal {
        id: groupsSettingsBar

        anchors.top: parent.top

        isRound: false
        headerText: tr.group_mode_title
        showCloseIcon: false
    }

    Rectangle {
        id: lowerBlackRect

        width: parent.width
        height: 1

        anchors.top: groupsSettingsBar.bottom

        color: ui.ds3.bg.low
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: lowerBlackRect.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24

        EmptyGroupsScreen {
            id: emptyGroupsScreen

            width: parent.width

            visible: management.groups.length == 0
            z: 2
        }

        DS3.SettingsSwitch {
            id: activateToggle

            radius: 12
            title: hub.groups_enabled ? tr.deactivate_group_mode :  tr.activate_group_mode
            checked: hub.groups_enabled
            visible: !emptyGroupsScreen.visible
            cancelBinding: false
            enabled: {
                if (["YAVIR", "YAVIR_PLUS"].includes(hub.hub_type) && hub.groups_enabled) {
                    return false
                }
                return !groupModeWarning.visible
            }

            onSwitched: () => {
                if (!groupModeWarning.visible) {
                    app.hub_management_module.change_group_mode(hub.id, !hub.groups_enabled)
                    Popups.please_wait_popup(tr.request_send, 30, [checkedChanged, app.actionFailed])
                }
            }
        }

        DS3.Text {
            id: groupModeWarning

            width: parent.width

            color: ui.ds3.figure.attention
            text: tr.to_activate_group_mode_you_must_distribute_all_devices_between_groups
            style: ui.ds3.text.body.MRegular
            visible: management.filtered_devices_without_groups.length > 0 && groupsRepeater.count > 0
        }

        DS3.Spacing { height: defaultSpacing }

        DS3.SettingsContainer {
            id: groupsContainer

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            clip: true
            visible: !emptyGroupsScreen.visible

            Repeater {
                id: groupsRepeater

                onCountChanged : {
                    groupModeWarning.visible = management.filtered_devices_without_groups.length > 0 && groupsRepeater.count > 0
                }

                width: groupsContainer.width
                height: contentHeight

                model: management.groups
                clip: true


                DS3.GroupNavigation {
                    imageSourceLink: group.small_image_link
                    groupTitle: group.name
                    groupID: !!group ? group.group_id_dec : ""
                    deviceCount: !!group ? group.devices_count : ""

                    settingsGearClicked: () => {
                        Popups.group_settings_popup(group)
                    }
                    groupRegularClicked: () => {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupView.qml", {
                            "group": group
                        })
                    }
                }
            }
        }

        DS3.Spacing { height: emptyGroupsScreen.visible ? 0 : defaultSpacing }

        DS3.ButtonOutlined {
            id: addGroupButton

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            buttonIconSource: "qrc:/resources/images/desktop/icons/ic-plus.svg"
            text: tr.add_group

            onClicked: Popups.add_group_popup()
        }
    }
}
