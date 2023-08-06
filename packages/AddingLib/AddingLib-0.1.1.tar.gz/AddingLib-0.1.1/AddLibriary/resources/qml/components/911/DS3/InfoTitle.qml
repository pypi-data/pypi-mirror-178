import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


// Figma name: Info.TitlePrimary, Info.TitleSecondary
DS3.MasterInfo {
    // The following members are inherited from MasterInfo
    //  status: var ( ui.ds3.status )
    //  leftIcon: alias
    //  atomTitle: alias
    //  stateEnabled: bool
    //  statusColor: readonly var

    color: ui.ds3.bg.highest
}
