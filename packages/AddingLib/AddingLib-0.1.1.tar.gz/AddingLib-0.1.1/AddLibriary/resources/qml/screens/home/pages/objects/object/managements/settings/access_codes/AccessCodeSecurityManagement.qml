import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


Rectangle {
    property var accessCode: null
    property var changedGroups: ({})
    property var saveSecurityManagementCallback: () => {
        changedGroups = {}
        changesChecker.changeInitialValues()
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.arm_permission_with_group
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            if (buttonBar.enabled) {
                var discard_changes_popup = DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                    title: tr.dont_save_title,
                    text: tr.dont_save_descr,
                    firstButtonText: tr.discard_changes_button,
                    isFirstButtonRed: true,
                    firstButtonCallback: () => {
                        loaderAccessCode.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodeSettingsForOne.qml", {"accessCode": accessCode})
                        isDiscardChanges = false
                    },
                    secondButtonCallback: () => {
                        discard_changes_popup.close()
                    },
                    secondButtonText: tr.back_editing_button,
                    secondButtonIsOutline: true,
                    isVertical: true,
                })
            } else {
                loaderAccessCode.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodeSettingsForOne.qml", {"accessCode": accessCode})
            }
        }
    }

    DS3.ScrollView {
        id: contentScrollView

        width: parent.width

        anchors {
            fill: undefined
            top: navBarModal.bottom
            topMargin: 1
            bottom: buttonBar.top
            bottomMargin: 1
        }

        padding: 24

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: accessCodeNightMode

                checked: accessCode.arming_permissions.includes("ACCESS_CODE_ARMING_PERMISSION_NIGHT_MODE")
                title: tr.perimeter_armed
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            ListView {
                id: accessCodesGroups

                width: parent.width
                height: contentHeight

                interactive: false
                model: management.groups
                spacing: 1
                visible: !!count
                delegate: DS3.GroupSwitch {
                    image.source: group.small_image_link != "WRONG" ? group.small_image_link : ""
                    atomTitle.title: !!group ? group.name : ""
                    atomTitle.subtitle: "ID " + (!!group ? group.group_id_dec : "")
                    descText.text: (
                        !!group && group.devices_count ?
                        tr.devices_count_desktop + ": " + (!!group ? group.devices_count : "") :
                        tr.no_devices_lable
                    )
                    checked: {
                        var isGroupChecked = false
                        accessCode.group_permissions.forEach(function(group_from_access_code) {
                            if (group_from_access_code.group_id == group_id) {
                                isGroupChecked = group_from_access_code.permissions.includes("ACCESS_CODE_GROUP_PERMISSIONS_ARM") ||
                                                 group_from_access_code.permissions.includes("ACCESS_CODE_GROUP_PERMISSIONS_DISARM")
                            }
                        })
                        return isGroupChecked
                    }

                    onToggle: () => {
                        checked = !checked
                        if (group_id in changedGroups) delete changedGroups[group_id]
                        else changedGroups[group_id] = checked
                        changedGroupsChanged()
                    }
                }
            }
        }
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            accessCodeNightMode.checked,
            changedGroups
        ]
    }

    DS3.ButtonBar {
        id: buttonBar

        anchors.bottom: parent.bottom

        enabled: changesChecker.hasChanges
        buttonText: tr.save
        hasBackground: true
        button.onClicked: {
            var settings = {
                "arming_permissions": ["ACCESS_CODE_ARMING_PERMISSION_ARM", "ACCESS_CODE_ARMING_PERMISSION_DISARM"],
                "group_permissions": accessCode.group_permissions,
                "id": accessCode.id
            }
            if (accessCodeNightMode.checked) {
                settings["arming_permissions"].push("ACCESS_CODE_ARMING_PERMISSION_NIGHT_MODE")
            }

            Object.keys(changedGroups).forEach((changedGroupId) => {
                if (changedGroups[changedGroupId]) {
                    settings["group_permissions"].push({
                        "group_id": changedGroupId,
                        "permissions": ["ACCESS_CODE_GROUP_PERMISSIONS_ARM", "ACCESS_CODE_GROUP_PERMISSIONS_DISARM"]
                    })
                } else {
                    settings["group_permissions"] = settings["group_permissions"].filter(accessCodeGroup => accessCodeGroup["group_id"] != changedGroupId)
                }
            })

            DesktopPopups.waitPopup(
                app.rpc.hubAccessCodes.accessCodesSettingsUpdated,
                saveSecurityManagementCallback
            )
            context.updateSettings(settings)
        }

        onEnabledChanged: {
            isDiscardChanges = buttonBar.enabled
        }
    }
}