import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: trashFooter
    width: parent.width
    height: visible ? 72 : 0
    color: ui.colors.dark2
    visible: selectedCount

    property var selectedCount: 0

    signal countSelected()

    onCountSelected: {
        if (objectsSidebar.currentTab.mode != "trash") {
            trashFooter.selectedCount = 0
            return
        }

        var count = 0
        for (var i = 0; i < objectsTable.model.length; i++) {
            if (objectsTable.itemAtIndex(i).selected) count += 1
        }

        trashFooter.selectedCount = count
    }

    Custom.FontText {
        id: selectedText
        text: util.insert(tr.objects_selected, [trashFooter.selectedCount])
        color: ui.colors.light3
        width: 120
        font.pixelSize: 14
        height: parent.height
        wrapMode: Text.WordWrap
        elide: Text.ElideRight
        textFormat: Text.PlainText
        maximumLineCount: 1
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignLeft
        anchors {
            left: parent.left
            leftMargin: 56
        }
    }

    Item {
        id: deselectButtonItem
        width: parent.width / 4 - 36
        height: parent.height
        anchors {
            left: parent.left
            leftMargin: 184
        }

        Custom.Button {
            id: deselectButton
            width: parent.width
            text: tr.deselect_objects
            color: ui.colors.white
            transparent: true
            anchors.centerIn: parent

            onClicked: {
                for (var i = 0; i < objectsTable.model.length; i++) {
                    objectsTable.itemAtIndex(i).selected = false
                }
                trashFooter.selectedCount = 0
            }
        }
    }

    Item {
        id: restoreButtonItem
        width: parent.width / 4 - 36
        height: parent.height
        anchors {
            right: deleteButtonItem.left
            rightMargin: 8
        }

        Custom.Button {
            id: restoreButton
            width: parent.width
            text: tr.restore_objects
            loading_background_color: "transparent"
            anchors.centerIn: parent

            anim {
                anchors.verticalCenterOffset: 0
            }

            onClicked: {
                restoreButton.loading = true

                var item = null
                var hubIds = []

                for (var i = 0; i < objectsTable.model.length; i++) {
                    item = objectsTable.itemAtIndex(i)
                    if (item.selected && item.hubId) {
                        hubIds.push(item.hubId)
                    }
                }

                app.facility_module.restore_facilities(hubIds)
            }
        }
    }

    Item {
        id: deleteButtonItem
        width: parent.width / 4 - 36
        height: parent.height
        anchors {
            right: parent.right
            rightMargin: 64
        }

        Custom.Button {
            id: deleteButton
            width: parent.width
            text: tr.delete_now
            color: ui.colors.red1
            transparent: true
            loading_background_color: "transparent"
            anchors.centerIn: parent

            anim {
                color: ui.colors.red1
                anchors.verticalCenterOffset: 0
            }

            onClicked: {
                deleteButton.loading = true

                var item = null
                var hubIds = []

                for (var i = 0; i < objectsTable.model.length; i++) {
                    item = objectsTable.itemAtIndex(i)
                    if (item.selected && item.hubId) {
                        hubIds.push(item.hubId)
                    }
                }

                app.facility_module.remove_facilities(hubIds)
            }
        }
    }

    Connections {
        target: objectsSidebar

        onReloadModel: {
            trashFooter.selectedCount = 0
        }

        onCurrentTabChanged: {
            trashFooter.selectedCount = 0
        }
    }

    Connections {
        target: app.facility_module

        onCancelChannel911RemovalSuccess: {
            restoreButton.loading = false
            objectsSidebar.reloadModel()
        }

        onCancelChannel911RemovalFailed: {
            restoreButton.loading = false
            objectsSidebar.reloadModel()
        }

        onRemoveChannel911Success: {
            deleteButton.loading = false
            objectsSidebar.reloadModel()
        }

        onRemoveChannel911Failed: {
            deleteButton.loading = false
            objectsSidebar.reloadModel()
        }
    }
}