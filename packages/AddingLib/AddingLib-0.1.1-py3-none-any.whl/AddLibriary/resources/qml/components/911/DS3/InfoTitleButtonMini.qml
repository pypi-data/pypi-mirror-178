import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


// Figma name: Info.TitlePrimary.ButtonMini, Info.TitleSecondary.ButtonMini
DS3.InfoTitle {
    // The following members are inherited from MasterInfo
    //  status: var ( ui.ds3.status )
    //  leftIcon: alias
    //  atomTitle: alias
    //  stateEnabled: bool
    //  statusColor: readonly var

// Enum with state behavior for the ButtonMini
    enum StateBehavior {
        Inherited,      // default
        AlwaysEnabled,
        AlwaysDisabled
    }

//  Settings state behavior for the control
    property var stateBehavoir: DS3.InfoTitleButtonMini.StateBehavior.Inherited
//  ButtonMini component
    property alias buttonMini: buttonMiniControl
//  Is control enabled
    readonly property bool isControlEnabled: {
        if (stateBehavoir == DS3.InfoTitleButtonMini.StateBehavior.AlwaysDisabled) return false
        return stateEnabled || stateBehavoir == DS3.InfoTitleButtonMini.StateBehavior.AlwaysEnabled
    }

//  On right button clicked
    signal rightControlClicked

    atomTitle {
        anchors.right: buttonMiniControl.left

        titleColor: {
            if (!!atomTitle.subtitle) return ui.ds3.figure.secondary
            if (status == ui.ds3.status.DEFAULT) {
                return enabled ? ui.ds3.figure[atomTitle.isPrimary ? "base" : "secondary"] : ui.ds3.figure.nonessential
            } else {
                return statusColor
            }
        }
    }

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        source: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"
        opacity: isControlEnabled ? 1 : 0.3
        enabled: isControlEnabled
        color: status == ui.ds3.status.DEFAULT ? ui.ds3.figure.interactive : statusColor

        onClicked: rightControlClicked()
    }
}
