import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/utils.js" as Utils


// Figma name: Info.TitlePrimary.ButtonIcon, Info.TitleSecondary.ButtonIcon
DS3.InfoTitle {
    // The following members are inherited from MasterInfo
    //  status: var ( ui.ds3.status )
    //  leftIcon: alias
    //  atomTitle: alias
    //  stateEnabled: bool
    //  statusColor: readonly var

// Enum with state behavior for the ButtonIcon
    enum StateBehavior {
        Inherited,      // default
        AlwaysEnabled,
        AlwaysDisabled
    }

//  Settings state behavior for the control
    property var stateBehavoir: DS3.InfoTitleButtonIcon.StateBehavior.Inherited
//  Text on popup when copied
    property var textOnCopy
//  Text on popup when copied
    property alias buttonIcon: buttonIconControl
//  Is control enabled
    readonly property bool isControlEnabled: {
        if (stateBehavoir == DS3.InfoTitleButtonIcon.StateBehavior.AlwaysDisabled) return false
        return stateEnabled || stateBehavoir == DS3.InfoTitleButtonIcon.StateBehavior.AlwaysEnabled
    }


//  On right button clicked
    signal rightControlClicked

    atomTitle {
        anchors.right: buttonIconControl.left

        titleColor: status == ui.ds3.status.DEFAULT ? ui.ds3.figure.base : statusColor
    }

    DS3.ButtonIcon {
        id: buttonIconControl

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
        opacity: isControlEnabled ? 1 : 0.3
        enabled: isControlEnabled

        onClicked: {
            if (buttonIcon.source == "qrc:/resources/images/Athena/common_icons/Copy-M.svg") {
                popupCopy.open()
                util.set_clipboard_text(atomTitle.subtitle)
            }
            rightControlClicked()
        }
    }

    DS3Popups.PopupCopy {
        id: popupCopy

        text: textOnCopy ? textOnCopy : (atomTitle.title + ' ' + tr.copied)
    }
}
