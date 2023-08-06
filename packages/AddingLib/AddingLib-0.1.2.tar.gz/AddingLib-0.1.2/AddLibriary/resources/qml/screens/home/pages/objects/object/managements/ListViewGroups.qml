import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ListView {
    id: groups

    property var withoutSettingIcon: false
    property var reindexNeeded: true

    Connections {
        target: groups.list.model

        onLengthChanged: {
            groups.list.currentIndexChanged()
        }
    }

    Connections {
        target: management

        onResetCurrentIndexes: {
            if (!groups.reindexNeeded) return

            groups.reindexNeeded = false
            groups.list.currentIndex = groups.list.model.length > 0 ? 0 : -1
        }
    }

    contentPadding: 0
    list {
        spacing: 1
        delegate: GroupsDelegate {
            settingsVisible: !withoutSettingIcon
        }
    }
}