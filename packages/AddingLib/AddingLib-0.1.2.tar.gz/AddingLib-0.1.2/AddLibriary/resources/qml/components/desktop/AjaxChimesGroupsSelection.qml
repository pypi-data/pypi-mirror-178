import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"


Rectangle {
    width: 360
    height: parent.height

    anchors.left: parent.left

    visible: management.devices.hub.groups_enabled
    color: ui.colors.dark3

    AjaxPopupCloseHeader {
        id: closeItem
        label: tr.chime_activation
    }

    View {
        id: groupsSelection

        width: parent.width

        anchors {
            top: closeItem.bottom
            bottom: saveCancel.top
        }

        Column {
            width: parent.width

            AjaxChimesActivationDescription { id: chimesActivationDescription }

            Column {
                width: parent.width

                AjaxChimesListView {
                    id: availableGroupsList

                    isAvailable: true
                }

                AjaxChimesListView {
                    id: unavailableGroupsList

                    isAvailable: false

                    visible: AjaxChimesGroupsSelection
                }
            }
        }
    }

    AjaxSaveCancel {
        id: saveCancel

        width: parent.width
        height: 48

        anchors.bottom: parent.bottom

        saveArea.onClicked: {
            Popups.please_wait_popup()
            var availableGroupsStateMap = availableGroupsList.buildGroupStateMap()
            var unavailableGroupsStateMap = unavailableGroupsList.buildGroupStateMap()
            if (typeof incident_item == "undefined") app.chimes_module.groups_chimes_action(availableGroupsStateMap, unavailableGroupsStateMap)
            else app.chimes_module.groups_chimes_action(availableGroupsStateMap, unavailableGroupsStateMap, incident_item)
        }

        cancelArea.onClicked: {
            popup.close()
        }
    }
}
