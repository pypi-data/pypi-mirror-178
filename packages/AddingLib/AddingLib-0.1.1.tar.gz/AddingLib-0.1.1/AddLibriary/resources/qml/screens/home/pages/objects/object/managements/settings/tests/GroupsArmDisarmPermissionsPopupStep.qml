import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups


DS3Popups.PopupStep {
    id: permissionsPopup

    height: maxStepHeight

    property var night_mode_selected: device.perimeter_arm
    property var header_selected: util.all_selected_access_card_groups(groups, selected)
    property var groups: management.filtered_groups.get_all_groups()

    property var selectedGroups: {
        let selectedGroupsIDs = device.get_selected_groups().map(el => el.id)
        return groups.filter(el => selectedGroupsIDs.includes(el.id)).sort(function (a, b) {
            if (a.id > b.id) {
                return 1;
            }
            if (a.id < b.id) {
                return -1;
            }
            return 0;
        });
    }

    Connections {
        target: app

        onActionSuccess: {
            goBack()
        }
    }

    sidePadding: 24
    title: tr.arm_permission_with_group

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            deactivation.checked,
            permissionsPopup.selectedGroups,
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.SettingsSwitch {
            id: deactivation

            title: tr.partially_armed
            checked: permissionsPopup.night_mode_selected
            cancelBinding: false

            onSwitched: () => {
                permissionsPopup.night_mode_selected = !permissionsPopup.night_mode_selected
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.TitleSection {
            width: parent.width

            forceTextToLeft: true
            text: tr.group_mode_title
            hasButton: true
            buttonText: header_selected ? tr.uncheck_all : tr.check_all

            onButtonClicked: () => {
                if (header_selected) {
                    permissionsPopup.selectedGroups = []
                } else {
                    permissionsPopup.selectedGroups = permissionsPopup.groups
                }
                header_selected = !header_selected
            }
        }

        Repeater {
            width: parent.width

            model: permissionsPopup.groups

            delegate: DS3.GroupMultiSelection {
                id: currentGroup

                selected: permissionsPopup.selectedGroups == null ?
                    true :
                    permissionsPopup.selectedGroups.some(group => group.id == modelData.id)

                image.source: modelData.small_image_link != "WRONG" ? modelData.small_image_link : ""
                atomTitle.title: !!modelData ? modelData.name : ""
                atomTitle.subtitle: "ID " + (!!modelData ? modelData.id : "")
                descText.text: (
                    !!modelData && modelData.devices_count ?
                    tr.devices_count_desktop + ": " + (!!modelData ? modelData.devices_count : "") :
                    tr.no_devices_lable
                )
                status: !!modelData && modelData.devices_count ? ui.ds3.status.DEFAULT : ui.ds3.status.WARNING
                onSelectedCallback: () => {
                    if (!selected) {
                        permissionsPopup.selectedGroups.push(modelData)
                        permissionsPopup.selectedGroups = permissionsPopup.selectedGroups.sort(function (a, b) {
                            if (a.id > b.id) {
                                return 1;
                            }
                            if (a.id < b.id) {
                                return -1;
                            }
                            return 0;
                        });
                    } else {
                        permissionsPopup.selectedGroups = permissionsPopup.selectedGroups.filter(group => group.id != modelData.id)
                    }
                    permissionsPopup.selectedGroupsChanged()
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        button.text: tr.save
        enabled: changesChecker.hasChanges
        hasBackground: true

        button.onClicked: {
            Popups.please_wait_popup()
            app.hub_management_module.save_access_card_groups(device, night_mode_selected, selectedGroups, groups)
        }
    }
}
