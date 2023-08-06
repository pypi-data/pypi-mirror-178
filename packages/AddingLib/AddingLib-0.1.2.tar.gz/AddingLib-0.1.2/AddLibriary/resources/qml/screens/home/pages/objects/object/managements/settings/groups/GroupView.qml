import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: topLevel

//  The group to display and edit/delete
    property var group: null
// current index to track which folder is selected
    property int currentIndex: 0
// Constants
//  Link to go back to GroupsSettings
    readonly property string backLink: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupsSettings.qml"
//  Links to go to GroupDevicesView and GroupUsersView (Views connected to the folders Devices and Users)
    readonly property var folderLinks: [
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupDevicesView.qml",
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupUsersView.qml"
    ]

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: groupNameItem

        anchors.top: parent.top

        isRound: false
        headerText: group.name
        showCloseIcon: false
        showBackArrow: true

        onBackAreaClicked: {
            loader.setSource(backLink)
        }
    }

    Rectangle {
        id: upperBlackRect

        width: parent.width
        height: 1

        anchors.top: groupNameItem.bottom

        color: ui.ds3.bg.low
    }

    DS3.FolderControl {
        id: folderControl

        anchors {
            top: upperBlackRect.bottom
            left: parent.left
        }

        onCurrentIndexDiffer: {
            currentIndex = index
            folderControl.currentIndex = index
            groupLoader.source = folderLinks[currentIndex]
        }

        model:  [
            { text: tr.devices, index: 0 },
            { text: tr.users, index: 1 }
        ]
    }

    Rectangle {
        id: lowerBlackRect

        width: parent.width
        height: 1

        anchors.top: folderControl.bottom

        color: ui.ds3.bg.low
    }

    Item {
        width: parent.width

        anchors.top: lowerBlackRect.bottom
        anchors.bottom: parent.bottom

        Loader {
            id: groupLoader

            anchors.fill: parent

            source: folderLinks[0]
        }
    }
}
