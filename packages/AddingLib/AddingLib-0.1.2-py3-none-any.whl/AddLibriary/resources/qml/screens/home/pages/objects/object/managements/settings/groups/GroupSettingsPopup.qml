import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup

//  If popup should be blocked from editing and closing
    property bool blocked: false
//  The group to display and edit/delete
    property var group: null
//  Constant default spacing
    readonly property var defaultSpacing: 24

// A signal for opening image file dialog within this popup
    signal imageFileDialogOpened

    Connections {
        target: app

        onActionSuccess: popup.close()
    }

    Connections {
        target: imageFileDialog

        onAccepted:  {
            closePolicy = popup.defaultPolicy
            blocked = false
        }

        onRejected:  {
            closePolicy = popup.defaultPolicy
            blocked = false
        }
    }

    Connections {
        target: app

        onNewImageReady: {
            var settings = {}
            settings["url"] = data["path"]
            settings["hub_id"] = hub.hub_id
            settings["group_id"] = group.group_id
            app.hub_management_module.upload_group_photo(settings)
        }
    }

    onImageFileDialogOpened: {
        closePolicy = Popup.NoAutoClose
        blocked = true
    }

    width: 500
    height: 675

    header: DS3.NavBarModal {
        id: groupsSettingsLabel

        isRound: true
        showCloseIcon: !blocked
        headerText: group.name
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            groupNameField.atomInput.text,
            armInvolved.checked,
            disarmInvolved.checked,
            secondStageRequired.checked
        ]
    }

    DS3.Spacing { height: defaultSpacing }

    DS3.PlugImageGroup {
        id: plugImage

        anchors.horizontalCenter: parent.horizontalCenter

        enabled: !blocked
        imageRect.source: group.small_image_link

        uploadSwitchChecked: () => {
            imageFileDialog.target = imageRect
            imageFileDialog.isRounded = true
            imageFileDialog.open()
            imageFileDialogOpened()
            sheetAction.close()
        }
        deleteSwitchChecked: () => {
            var settings = {
                "hub_id" : hub.hub_id,
                "group_id" : group.group_id
            }
            imageRect.source = "WRONG"
            imageRect.imageData = null
            app.hub_management_module.delete_group_photo(settings)
            sheetAction.close()
        }
    }

    DS3.Spacing { height: defaultSpacing }

    DS3.InputSingleLine {
        id: groupNameField

        radius: 12

        atomInput {
            label: tr.name
            enabled: !blocked
            placeholderText: tr.group_name
            text: group.name
            onTextChanged: {
                atomInput.text = util.validator(atomInput.text, 24)
                return
            }
        }
    }

    DS3.Spacing { height: defaultSpacing }

    DS3.SettingsContainer {
        id: groupsContainer

        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        enabled: !blocked

        DS3.SettingsSwitch {
            id: armInvolved

            title: tr.bulkArmInvolved
            checked: group.bulk_arm_involved
        }

        DS3.SettingsSwitch {
            id: disarmInvolved

            title: tr.bulkDisarmInvolved
            checked: group.bulk_disarm_involved
        }

        DS3.SettingsSwitch {
            id: secondStageRequired

            visible: hub.firmware_version_dec >= 209100 && hub.two_stage_arming_state
            title: tr.two_step_arming
            checked: group.second_stage_required
        }
    }

    DS3.Spacing { height: defaultSpacing }

    DS3.SettingsContainer {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.ButtonRow {
            isDanger: true
            text: tr.delete_group
            enabled: !blocked

            onClicked: {
                Popups.group_delete_popup(group)
            }
        }
    }

    DS3.Spacing { height: defaultSpacing }

    footer: DS3.ButtonBar {
        id: buttonBar

        width: parent.width
        height: 80

        anchors.centerIn: parent

        buttonText: tr.save
        hasBackground: true
        button.enabled: !blocked && changesChecker.hasChanges

        button.onClicked: {
            var groupName = groupNameField.atomInput.text.trim()

            if (!groupName) {
                groupNameField.focus = false
                return
            }

            var settings = {
                "name": {"name": groupNameField.atomInput.text.trim()},
                "bulk_arm_involved": armInvolved.checked,
                "bulk_disarm_involved" : disarmInvolved.checked,
                "second_stage_required" : secondStageRequired.checked,
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, group, settings)
        }
    }
}
