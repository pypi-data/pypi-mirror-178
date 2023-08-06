import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/" as Custom


ListView {
    id: groupsList

    property bool isAvailable: false
    property var checkedCounter: 0
    property var allChecked: count == checkedCounter
    property var headerTitle

    function toggleAll() {
        for(var child in contentItem.children) {
            if (contentItem.children[child].objectName == "chimesGroupDelegate") {
                contentItem.children[child].checked = !allChecked
            }
        }
        checkedCounter = allChecked ? 0 : count
    }

    function buildGroupStateMap() {
        var groupStateMap = {}
        for(var child in contentItem.children) {
            var groupItem = contentItem.children[child]
            if (contentItem.children[child].objectName == "chimesGroupDelegate")
                groupStateMap[groupItem.group.id] = groupItem.checked
        }
        return groupStateMap
    }

    onCountChanged: {
        if (count == 0) visible = false
        else visible = true
    }

    width: parent.width
    height: contentHeight

    visible: count != 0
    model: management
        ? (isAvailable ? management.filtered_groups_chimes_available : management.filtered_groups_chimes_unavailable)
        : []
    spacing: 16
    interactive: false
    // header and footer are swaped to enable layout direction changing
    verticalLayoutDirection: ListView.BottomToTop

    header: Item {
        width: parent.width
        height: 32
    }
    delegate: AjaxChimesGroupDelegate {
        group: model.group

        Component.onCompleted: {
            if (checked) {
                ListView.view.checkedCounter += 1
            }
        }
    }
    section.property: isAvailable ? "" : "group.chimes_status"
    section.criteria: ViewSection.FirstCharacter
    section.delegate: Item {
        width: groupsList.width
        height: sectionText.height + 32

        Custom.FontText {
            id: sectionText

            width: parent.width - 48

            anchors.centerIn: parent

            text: {
                return {
                    "H": tr.unavailable_groups_for_chimes_info,
                    "N": tr.groups_where_chimes_not_supported_info
                }[section]
            }
            font.pixelSize: 12
            color: ui.colors.light3
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
        }
    }
    footer: AjaxChimesGroupsHeader {
        headerTitle: groupsList.isAvailable ? tr.available_groups_for_chimes_title : tr.unavailable_groups_for_chimes_title
        checkText.visible: groupsList.isAvailable
        checkText.text: allChecked ? tr.uncheck_all : tr.check_all
    }
}
