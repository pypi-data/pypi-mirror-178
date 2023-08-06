import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk

Menu {
    id: contextMenu

    property bool groupsEnabled: hub && hub.groups_enabled
    property int groupsEnabledPopupHeight: 270 + 64 * Math.min(Math.ceil(groups.length/3), 5)
    /*  = basePopupHeight + GridViewCellHeight * Math.min(Math.ceil(groups.length/GroupsPerLine), MaxLinesOfGroups) */

    width: groupsEnabled ? 700 : 196
    rightMargin: groupsEnabled ? 200 : 0
    topMargin: groupsEnabled ? 128 : 0
    background: Rectangle {
        color: "transparent"
    }

    Rectangle {
        height: groupsEnabled ? contextMenu.groupsEnabledPopupHeight : 190

        color: ui.colors.dark2
        radius: 8

        GroupMode{}
        NoGroupMode{}
    }
}