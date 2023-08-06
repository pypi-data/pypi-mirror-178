import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups


AjaxPopup {
    id: popup

    width: 360
    height: {
        if (content.height + 100 + 96 > application.height) {
            return maxPopupHeight
        }
        return content.height + 50 + 96
    }

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Item {
        id: s

        width: popup.width
        height: popup.height

        Rectangle {
            id: rightRect

            width: 360
            height: parent.height

            anchors.right: parent.right
            visible: popup.width != 360

            color: "#0f0f0f"
            border.width: 1
            border.color: "#1f1f1f"
        }

        Column {
            id: content

            AjaxChimesGroupsSelection {
                id: groupsSelectionBlock
            }

            AjaxChimesDoesNotWork {
                id: chimesDoesNotWorkBlock

                visible: !groupsSelectionBlock.visible
            }
        }
    }

    Connections {
        target: app
        onActionSuccess: {
            popup.close()
        }
    }

    Connections {
        target: management.devices.hub
        onGroups_enabledChanged: {
            if (!management.devices.hub.groups_enabled && management.devices.hub.chimes_status != "HALF_READY") popup.close()
        }
    }
}