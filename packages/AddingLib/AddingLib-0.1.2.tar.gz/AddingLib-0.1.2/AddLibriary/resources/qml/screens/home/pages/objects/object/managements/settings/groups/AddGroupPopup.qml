import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup
//  Boolean value to determine if popup should be blocked from editing and closing
    property bool blocked: false
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

    onImageFileDialogOpened: {
        closePolicy = Popup.NoAutoClose
        blocked = true
    }

    width: 500
    height: 500

    header: DS3.NavBarModal {
        isRound: true
        showCloseIcon: !blocked
        headerText: tr.add_group_title
    }

    DS3.Spacing { height: defaultSpacing }

    DS3.PlugImageGroup {
        id: plugImage

        anchors.horizontalCenter: parent.horizontalCenter

        enabled: !blocked

        uploadSwitchChecked: () => {
            imageFileDialog.target = imageRect
            imageFileDialog.isRounded = true
            imageFileDialog.open()
            imageFileDialogOpened()
            sheetAction.close()
        }
        deleteSwitchChecked: () => {
            imageRect.source = "WRONG"
            imageRect.imageData = null
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

            onTextChanged: {
                atomInput.text = util.validator(atomInput.text, 24)
                return
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.the_name_can_contain_letters
    }

    DS3.Spacing { height: defaultSpacing }

    footer: DS3.ButtonBar {
        id: buttonBar

        width: parent.width
        height: 80

        anchors.centerIn: parent

        buttonText: tr.save
        hasBackground: true
        button.enabled: !blocked

        button.onClicked: {
            var groupName = groupNameField.atomInput.text.trim()

            if (!groupName) {
                groupNameField.focus = false
                Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                return
            }

            Popups.please_wait_popup()
            app.hub_management_module.add_group(hub, groupName)
        }
    }
}
